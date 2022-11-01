from django.shortcuts import render,redirect
from reviews.models import Review
from reviews.forms import ReviewForm
# Create your views here.

def index(request):
    return render(request, 'reviews/index.html')




def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:index")
    else:
        form = ReviewForm()

    context = {
        "form": form,
    }
    return render(request, "reviews/create.html", context)

