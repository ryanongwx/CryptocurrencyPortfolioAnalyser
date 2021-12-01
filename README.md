# CryptocurrencyPortfolioAnalyser

The Cryptocurrency Portfolio Analyser is hosted here: https://crypto-analyser.herokuapp.com/

The concept behind the creation of this cryptocurrency portfolio analyser was to implement a user-friendly interface in order to evaluate my cryptocurrency portfolio. 

The app that I am currently using to trade crypto is Coinhako. If any of you are users of the app, you should be familiar with the fact that the app does not show any analysis of the amount of profit or loss you have made on the trades. It only displays your current holdings along with the value of your holdings and a list of the past transactions that you have made. As such, I created this user interface using Python’s Django framework in order to be able to track the details and make some calculations that I focus on and want to find out when I look at my current crypto portfolio. This is a simple automation such that it makes the calculations automated and simply presents me with the data upon updating my portfolio.

I made use of the Django framework as I wanted it to be a seamless interface with a well designed backend. The web element of Django allowed me to host it on Heroku which provided me with the ability to access my crypto analyser through the internet on any device. Additionally, Django provides User models and effective database management. The User model allows for different users to create different accounts and customise the crypto portfolio according to their portfolio and hence would be able to enjoy the evaluations and calculations made by my analyser. Online database management allowed me to easily store information from the transactions that users have made.

For live cryptocurrency prices, I made use of the Nomics cryptocurrency API in order to retrieve the live prices of the tokens in order to make effective evaluations and calculation of the profit and loss of your portfolio.
