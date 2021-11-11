from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
import requests
from .models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()
response = requests.get("https://api.nomics.com/v1/currencies/ticker?key=a4edc8e0bf84324e111593d559850c8c6f29cfac&ids=BTC,ETH,ADA,DOGE&interval=1d,30d&convert=SGD")
cryptoprices = response.json()

# Create your views here.
def index(request):

    if request.method == "POST":
        print('hi')
        form = transactionform(request.POST)
        if form.is_valid():
            coin = form.cleaned_data['coin']
            transactiontype = form.cleaned_data['transactiontype']
            price = form.cleaned_data['price']
            tokenqty = form.cleaned_data['tokenqty']
            date = form.cleaned_data['date']
            totalprice = price * tokenqty
            transactionfee = 0.01*totalprice
            transaction = Transaction(coin=coin, transactiontype=transactiontype, price=price, tokenqty=tokenqty,
                                      date=date, user=request.user, totalprice=totalprice, transactionfee=transactionfee)
            transaction.save()
            return render(request, 'crypto/index.html', {
                "transactions": Transaction.objects.filter(user=request.user)})

    return render(request, 'crypto/index.html', {
        "transactions": Transaction.objects.filter(user=request.user)})

def createtransaction(request):
    return render(request, "crypto/createtransaction.html",{
        'form': transactionform
    })

def coinanalysis(request, coin):
    boughtfor = 0
    tokenbought = 0
    soldfor = 0
    tokensold = 0
    totaltransactionfees = 0
    # GET THE TRANSACTION OF ONLY THE USER OF THE CURRENT SESSION
    transactions = Transaction.objects.filter(user=request.user)
    for transaction in transactions:
        if transaction.coin == coin:
            totaltransactionfees += transaction.transactionfee
            if transaction.transactiontype == "Buy":
                boughtfor += transaction.price * transaction.tokenqty
                tokenbought += transaction.tokenqty
            else:
                soldfor += transaction.price * transaction.tokenqty
                tokensold += transaction.tokenqty

            for crypto in cryptoprices:
                if crypto['id'] == coin:
                    currentprice = crypto["price"]
    tokenstransacted = tokensold
    tokensholding = tokenbought - tokensold
    avgpricebought = boughtfor / tokenbought
    totalbought = boughtfor
    if tokensold > 0:
        avgpricesold = soldfor / tokensold
        totalsold = soldfor
    else:
        avgpricesold = 0
        totalsold = 0

    if tokenbought == tokensold:
        realisedprofit = (avgpricesold - avgpricebought) * tokenbought
    else:
        realisedprofit = 0

    tokenvalueifsold = float(tokensholding) * float(currentprice)
    totalprofitifsoldatcurrentprice = tokenvalueifsold + soldfor - boughtfor - totaltransactionfees

    analysis = {'id': coin, "tokenstransacted": tokenstransacted,
                            "tokensholding": tokensholding,
                            "avgpricebought": avgpricebought, "avgpricesold": avgpricesold,
                            "realisedprofit": realisedprofit,
                            "totalbought": totalbought, "totalsold": totalsold,
                            "totalprofitifsoldatcurrentprice": totalprofitifsoldatcurrentprice,
                            "totaltransactionfees": totaltransactionfees}


    return render(request, "crypto/analysis.html", {
        'analysis': analysis,
        'transactions': Transaction.objects.filter(user=request.user, coin=coin)
    })

def custom(request):
    if request.method == "POST":
        coin = request.POST["coin"]
        return HttpResponseRedirect(f"/coinanalysis/{coin}")
    else:
        return render(request, "crypto/custom.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("crypto:index"))
        else:
            return render(request, "crypto/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "crypto/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("crypto:login"))

def register(request):
    if request.method == "POST":
        # Register and create new user
        username = request.POST["username"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        if username is not None and password is not None:
            if password == confirmpassword:
                User.objects.create_user(username, '', password)
                return HttpResponseRedirect(reverse("crypto:login"))
    return render(request, "crypto/register.html")


# Form for keying in transaction details
class transactionform(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['coin', 'transactiontype', 'price', 'tokenqty', 'date']