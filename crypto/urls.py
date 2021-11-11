from django.urls import path

from . import views
app_name = 'crypto'

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('createtransaction', views.createtransaction, name='createtransaction'),
    path('custom', views.custom, name='custom'),
    path('coinanalysis/<str:coin>', views.coinanalysis, name='coinanalysis'),
]