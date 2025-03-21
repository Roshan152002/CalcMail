from django.urls import path
from . import views

urlpatterns=[
    path('',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('operations/',views.addition,name='add'),
    path('sendEmails/',views.send_results_email,name='sendEmails'),
]