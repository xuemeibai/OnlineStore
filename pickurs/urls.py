"""pickurs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from onlinestore import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include

urlpatterns = [
	path('', views.home_action, name='anonymous'),
	path('home', views.home_action, name='home'),
	path('login', views.login_action, name='login'),
	path('logout', views.logout_action, name='logout'),
	path('register', views.register_action, name='register'),
	path('confirm-registration/<slug:username>/<slug:token>',
        views.confirm_action, name='confirm'),
	path('release', views.AddItemPost, name='release'),
	path('get_photo/<id>', views.get_photo, name='get_photo'),
	path('edit_profile/<id>', views.edit_profile, name='edit_profile'),

	path('user_profile/<int:id>', views.user_profile, name='user_profile'),

	path('self_avatar/<id>', views.get_self_avatar, name='self_avatar'),
	path('search', views.search, name='search'),
	path('category/<int:type>', views.category, name='category'),
	path('sort/<int:type>', views.get_sorted_data, name='sort'),

	path('item_details/<int:id>', views.item_detail_action, name='item_details'),
	path('favorites', views.favorites_page_action, name='favorites'),
	path('posting_items', views.posting_items_action, name='posting_items'),
	path('add_to_favorite/<int:id>', views.add_to_favorite_action, name='add_to_favorite'),
	path('delete_from_favorite/<int:id>', views.delete_from_favorite_action, name='delete_from_favorite'),

	path('add_to_favorite_home', views.add_to_favorite_home_action, name='add_to_favorite_home'),
	path('delete_from_favorite_home', views.delete_from_favorite_home_action, name='delete_from_favorite_home'),
	path('request_for_trade/<int:id>', views.request_for_trade_action, name='request_for_trade'),
	path('cancel_trade_request/<int:id>', views.cancel_trade_request_action, name='cancel_trade_request'),
	path('accept_request/<int:id>/<int:userid>', views.accept_request_action, name='accept_request'),
	path('delete_item/<int:id>', views.delete_item_action, name='delete_item'),

	path('history_sells', views.history_sells_action, name='history_sells'),
	path('history_orders', views.history_orders_action, name='history_orders'),
	path('onlinestore/refresh-global', views.get_list_json),

	path('rate/<int:id>', views.rate_action, name = 'rate'),

	path('add-post/<int:ItemId>', views.add_post, name='add_post'),
    path('add-comment/<int:PostId>', views.add_comment, name='add_comment'),
    path('refresh-global', views.refresh_global_json, name='refresh_global'),

    path('my_cart', views.my_cart, name='my_cart'),
]
