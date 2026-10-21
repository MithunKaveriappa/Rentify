from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    wallet_balance = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    # ... other fields if needed

    def __str__(self):
        return self.full_name


# 2. Category (admin only for add/edit/delete)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

CONDITION_CHOICES = (
    ('NEW', 'New'),
    ('LIKE_NEW', 'Like New'),
    ('GOOD', 'Good'),
    ('FAIR', 'Fair'),
    ('POOR', 'Poor'),
)
# 3. Item (managed by item owner only)
class Item(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/%Y/%m/', null=True, blank=True)
    condition = models.CharField(max_length=12, choices=CONDITION_CHOICES, default='GOOD')
    daily_rent_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    max_rental_days = models.PositiveIntegerField(default=30)
    metadata = models.JSONField(blank=True, null=True, help_text='Optional JSON for extra attributes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['owner', 'is_available'])]
    def __str__(self):
        return f"{self.title} — {self.owner}"

REQUEST_STATUS = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('ONGOING', 'Ongoing'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
)

class RentalRequest(models.Model):
    renter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='rental_requests')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rental_requests')
    request_message = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    rental_start = models.DateField()
    rental_end = models.DateField()
    status = models.CharField(max_length=12, choices=REQUEST_STATUS, default='PENDING')
    total_rent_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    deposit_taken = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    payment_confirmed = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-requested_at']
    def __str__(self):
        return f"{self.item.title} requested by {self.renter} ({self.status})"
    def rental_days(self):
        return (self.rental_end - self.rental_start).days + 1
    def calculate_total(self):
        days = self.rental_days()
        rent = (self.item.daily_rent_price * days)
        self.total_rent_amount = rent
        return self.total_rent_amount

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlists')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'item')
    def __str__(self):
        return f"{self.user} -> {self.item.title}"

class Review(models.Model):
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_reviews')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reviews')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.rating} by {self.reviewer} for {self.owner}"

DISPUTE_STATUS = (
    ('OPEN', 'Open'),
    ('IN_REVIEW', 'In Review'),
    ('RESOLVED', 'Resolved'),
    ('REJECTED', 'Rejected'),
)

class Dispute(models.Model):
    rental_request = models.ForeignKey(RentalRequest, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='raised_disputes')
    description = models.TextField()
    status = models.CharField(max_length=12, choices=DISPUTE_STATUS, default='OPEN')
    resolution_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Dispute {self.id} ({self.status})"

class ChatRoom(models.Model):
    participants = models.ManyToManyField(UserProfile, related_name='chat_rooms')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"ChatRoom {self.id}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f"Message {self.id} in {self.room} by {self.sender}"


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    related_request = models.ForeignKey(RentalRequest, null=True, blank=True, on_delete=models.CASCADE)  # <-- Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"Notification for {self.user}: {self.title}"

