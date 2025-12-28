from django.urls import path, include
from .views import *
from account.views import edit_user_info, password_change

app_name = 'web'
urlpatterns = [

    # base.html
    path('test/', Home_page.as_view(), name='home'),
    # web_income
    path('income/all', income_views_all.as_view(), name='income_all'),
    path('income/edit/<int:pk>', income_edit, name='income_edit'),
    path('income/new', income_add, name='income_add'),
    # path('income/search/', income_views_search.as_view()),
    path('income/delete/<int:pk>', income_delete, name='income_delete'),
    path('income/post/<int:pk>', post_income, name='income_post'),
    path('income/share/<int:pk>', income_share_post, name='income_share'),
    path('income/addfeatured/<int:pk>', income_featured, name='income_featured'),


    # web_out
    path('out/all', out_views_all.as_view(), name='out_all'),
    path('out/edit/<int:pk>', out_edit, name='out_edit'),
    path('out/new', out_add, name='out_add'),
    path('out/search/', out_views_search.as_view()),
    path('out/delete/<int:pk>', out_delete, name='out_delete'),
    path('out/post/<int:pk>', post_out, name='out_post'),
    path('out/share/<int:pk>', out_share_post, name='out_share'),
    path('out/addfeatured/<int:pk>', out_featured, name='out_featured'),

    path('commant', comment, name='comment'),

    path('Transaction-Registration', Transaction_Registration.as_view(), name='Transaction_Registration'),
    # extend account
    path('user-info', edit_user_info, name='user_info'),
    path('passwoard-change/<int:pk>', password_change, name='password_change'),
    path('featured', show_featured, name='show_featured'),

]
