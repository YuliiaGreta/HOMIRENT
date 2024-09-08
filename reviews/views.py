from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.listing = listing
            review.save()
            return redirect('reviews:listing_reviews', listing_id=listing_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'listing': listing})

@login_required
def listing_reviews(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    reviews = listing.reviews.all()
    return render(request, 'reviews/listing_reviews.html', {'listing': listing, 'reviews': reviews})