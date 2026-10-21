from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from .forms import UserProfileForm, ItemForm, RentalRequestForm, ReviewForm, DisputeForm
from .models import (
    UserProfile, Category, Item, RentalRequest, Wishlist, Review,
    Dispute, Notification
)

def is_admin(user):
    return user.is_staff

def home(request):
    # Shows some featured items or dashboard
    items = Item.objects.filter(is_available=True).exclude(owner__user=request.user) if request.user.is_authenticated else Item.objects.filter(is_available=True)
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'page_obj': page_obj})

@login_required
def my_items(request):
    user = request.user
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user, full_name=user.get_full_name() or user.username)
    items = user.profile.items.all()
    return render(request, 'myitems.html', {'items': items})


@login_required
def all_items(request):
    # Exclude own items, show others' available items
    profile = request.user.profile
    items = Item.objects.filter(is_available=True).exclude(owner=profile)
    # Optional: Search/filter by category or condition
    query = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if cat:
        items = items.filter(category__id=cat)
    categories = Category.objects.all()
    return render(request, 'allitems.html', {
        'items': items,
        'categories': categories,
        'selected_category': cat,
        'query': query,
    })

@login_required
def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    is_owner = (item.owner.user == request.user)
    reviews = item.reviews.all()
    can_request = (not is_owner and item.is_available)
    already_requested = RentalRequest.objects.filter(item=item, renter__user=request.user, status__in=['PENDING', 'APPROVED', 'ONGOING']).exists()
    return render(request, 'item_detail.html', {
        'item': item,
        'is_owner': is_owner,
        'reviews': reviews,
        'can_request': can_request and not already_requested
    })

def item_public_view(request, slug):
    item = get_object_or_404(Item, slug=slug)
    reviews = item.reviews.all()
    # No login required, no owner/request logic
    return render(request, 'item_public_view.html', {
        'item': item,
        'reviews': reviews
    })

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user.profile
            item.save()
            messages.success(request, 'Item listed for rent successfully.')
            return redirect('my_items')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

@login_required
def edit_item(request, slug):
    item = get_object_or_404(Item, slug=slug, owner=request.user.profile)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, slug):
    item = get_object_or_404(Item, slug=slug, owner=request.user.profile)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted.')
        return redirect('my_items')
    return render(request, 'delete_item.html', {'item': item})

@login_required
def profile_view(request):
    return render(request, 'profile_view.html', {'userprofile': request.user.profile})

@login_required
def update_profile_user(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile_user.html', {'form': form})

# CATEGORY views (admin only)
@user_passes_test(is_admin)
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

@user_passes_test(is_admin)
def add_category(request):
    from .forms import CategoryForm # Define a simple CategoryForm if needed
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@user_passes_test(is_admin)
def edit_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    from .forms import CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=cat)
    return render(request, 'edit_category.html', {'form': form, 'category': cat})

@user_passes_test(is_admin)
def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted.')
        return redirect('manage_categories')
    return render(request, 'delete_category.html', {'category': cat})

# RENTAL REQUEST
@login_required
def request_rental(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if item.owner.user == request.user:
        messages.error(request, 'You cannot rent your own item!')
        return redirect('all_items')
    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental_req = form.save(commit=False)
            rental_req.item = item
            rental_req.renter = request.user.profile
            rental_req.status = 'PENDING'
            rental_req.save()
            # Create owner notification
            Notification.objects.create(
                user=item.owner,
                title="New Rental Request",
                body=f"{request.user.username} has requested to rent your item '{item.title}'.",
                related_request=rental_req  # <-- Link the notification
            )
            messages.success(request, 'Rental request sent!')
            return redirect('all_items')
    else:
        form = RentalRequestForm()
    return render(request, 'request_rental.html', {'item': item, 'form': form})


@login_required
def my_requests(request):
    # requests made by me
    requests = RentalRequest.objects.filter(renter__user=request.user)
    return render(request, 'myrequests.html', {'requests': requests})

@login_required
def incoming_requests(request):
    # requests for my items
    requests = RentalRequest.objects.filter(item__owner__user=request.user)
    return render(request, 'incoming_requests.html', {'requests': requests})

@login_required
def handle_request(request, pk, action):
    rental_request = get_object_or_404(RentalRequest, pk=pk, item__owner__user=request.user)
    if rental_request.status == 'PENDING':
        if action == 'approve':
            rental_request.status = 'APPROVED'
            rental_request.approved_at = timezone.now()
            rental_request.save()
            messages.success(request, 'Request approved.')
        elif action == 'reject':
            rental_request.status = 'REJECTED'
            rental_request.save()
            messages.success(request, 'Request rejected.')
    return redirect('incoming_requests')

# WISHLIST
@login_required
def add_to_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    profile = request.user.profile
    if item.owner == profile:
        messages.error(request, 'Cannot wishlist your own item.')
    else:
        Wishlist.objects.get_or_create(user=profile, item=item)
        messages.success(request, 'Item wishlisted.')
    return redirect('all_items')

@login_required
def remove_from_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    profile = request.user.profile
    Wishlist.objects.filter(user=profile, item=item).delete()
    messages.success(request, 'Item removed from wishlist.')
    return redirect('wishlist')

@login_required
def wishlist(request):
    profile = request.user.profile
    wishlists = profile.wishlists.all()
    return render(request, 'wishlist.html', {'wishlists': wishlists})

@login_required
def checkout_wishlist(request, slug):
    # Redirect to rental request for the item directly from wishlist
    item = get_object_or_404(Item, slug=slug)
    return redirect(reverse('request_rental', args=[slug]))

# REVIEWS
@login_required
def add_review(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user.profile
            review.owner = item.owner
            review.item = item
            review.save()
            messages.success(request, 'Review posted.')
            return redirect('item_detail', slug=slug)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'item': item})

# DISPUTE
@login_required
def raise_dispute(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk, renter__user=request.user)
    if request.method == 'POST':
        form = DisputeForm(request.POST)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.rental_request = rental_request
            dispute.raised_by = request.user.profile
            dispute.save()
            messages.success(request, 'Dispute raised.')
            return redirect('my_requests')
    else:
        form = DisputeForm()
    return render(request, 'raise_dispute.html', {'form': form, 'rental_request': rental_request})

@login_required
def my_notifications(request):
    notifications = request.user.profile.notifications.order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user.profile)
    notification.is_read = True
    notification.save()
    return redirect('my_notifications')

@login_required
def clear_read_notifications(request):
    request.user.profile.notifications.filter(is_read=True).delete()
    return redirect('my_notifications')