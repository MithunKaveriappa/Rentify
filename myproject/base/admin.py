from django.contrib import admin
from .models import (
    UserProfile, Category, Item, RentalRequest,
    Wishlist, Review, Dispute, ChatRoom, ChatMessage, Notification
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'wallet_balance', 'is_verified')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('is_verified',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'is_available', 'daily_rent_price', 'created_at')
    list_filter = ('is_available', 'category', 'condition')
    search_fields = ('title', 'owner__user__username', 'category__name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'renter', 'rental_start', 'rental_end', 'status', 'payment_confirmed', 'created_at')
    list_filter = ('status', 'payment_confirmed')
    search_fields = ('item__title', 'renter__user__username')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'added_at')
    search_fields = ('user__user__username', 'item__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'owner', 'item', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__user__username', 'owner__user__username', 'item__title')

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('rental_request', 'raised_by', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('rental_request__item__title', 'raised_by__user__username')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'timestamp', 'read')
    list_filter = ('read',)
    search_fields = ('room__id', 'sender__user__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__user__username', 'title')
