from django.urls import path
from . import views
urlpatterns=[
    path('index/',views.index),
    path('home/',views.index),
    path('about/',views.about),
    path('product/',views.product),
    path('myorder/',views.myorder),
    path('enquiry/',views.enquiry),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('mens/',views.mens),
    path('womens/',views.womens),
    path('viewproduct/',views.viewproduct),
    path('signout/',views.signout),
    path('kids/',views.kids),
    path('profile/',views.myprofile),
    path('myordr/',views.myordr),
    path('mycart/',views.mycart),
    path('viewproduct/',views.viewproduct),
    path('showcart/',views.showcart),
    path('cpdetail/',views.cpdetail),
    path('',views.index),
]