from django.urls import path
from . import views

urlpatterns = [
    # Default Home Dashboard (can be project landing)
    path('', views.home, name='dashboard'),

    # My items, all items (not my items)
    path('myitems/', views.my_items, name='my_items'),
    path('items/', views.all_items, name='all_items'),

    # Individual item details and CRUD for own items
    path('item/add/', views.add_item, name='add_item'),
    path('item/<slug:slug>/', views.item_detail, name='item_detail'),
    # base/urls.py
    path('item/<slug:slug>/view/', views.item_public_view, name='item_public_view'),
    path('item/<slug:slug>/edit/', views.edit_item, name='edit_item'),
    path('item/<slug:slug>/delete/', views.delete_item, name='delete_item'),

    # User profile
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.update_profile_user, name='update_profile_user'),

    # Category management (admin only)
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # Rental Requests
    path('item/<slug:slug>/request/', views.request_rental, name='request_rental'),
    path('myrequests/', views.my_requests, name='my_requests'),
    path('incomingrequests/', views.incoming_requests, name='incoming_requests'),
    path('requests/<int:pk>/<str:action>/', views.handle_request, name='handle_request'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('item/<slug:slug>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('item/<slug:slug>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/<slug:slug>/checkout/', views.checkout_wishlist, name='checkout_wishlist'),

    # Reviews
    path('item/<slug:slug>/review/', views.add_review, name='add_review'),

    # Disputes
    path('requests/<int:pk>/dispute/', views.raise_dispute, name='raise_dispute'),

    # Notifications
    path('notifications/', views.my_notifications, name='my_notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/clear-read/', views.clear_read_notifications, name='clear_read_notifications'),

]
