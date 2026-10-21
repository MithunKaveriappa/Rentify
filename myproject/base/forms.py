from django import forms
from .models import Item, RentalRequest, UserProfile, Review, Dispute, Wishlist
from django.contrib.auth.models import User

# UserProfile Update Form (user cannot edit is_verified or wallet_balance directly)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'contact_number', 'address', 'city', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),
            'contact_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Number'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

# Item add/edit form (all except owner, created/updated dates)
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'category', 'title', 'slug', 'description', 'image', 'condition',
            'daily_rent_price', 'deposit_amount', 'location', 'max_rental_days', 'metadata'
        ]
        widgets = {
            'category': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Slug'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'Description'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'condition': forms.Select(attrs={'class':'form-control'}),
            'daily_rent_price': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
            'deposit_amount': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'max_rental_days': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
            'metadata': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
        }

# Rental request form (user requests rental for other's item)
class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['request_message', 'rental_start', 'rental_end']
        widgets = {
            'request_message': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder':'Request Message'}),
            'rental_start': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'rental_end': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
        }

# Wishlist isn't created via form (added via view/action).

# Review form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class':'form-control'}, choices=[(i, str(i)) for i in range(1,6)]),
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder':'Comments'}),
        }

# Dispute Raise form
class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'Describe your issue'}),
        }

# Optionally, User creation form (for admin only, can use Django admin but form for site admin view)
class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }
