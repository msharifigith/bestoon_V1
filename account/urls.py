from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, login_view, logout_view, activate, user_panel, hom_viwe, show_sit, show_news, \
    forget_password, About , Home
from django.urls import include

app_name = 'account'
urlpatterns = [

    path('', Home.as_view(), name='home_viwe'),
    path('onlin-price', show_sit, name='show_price'),
    path('show-news', show_news, name='show_news'),
    path('sing-up/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('panel/', user_panel, name='user_panel'),
    path('forget-password/', forget_password, name='forget'),
    path('About/', About.as_view(), name='About'),
    path('Home/', Home.as_view(), name='Home'),
]
