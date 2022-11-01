from django.shortcuts import render,redirect
from reviews.models import Review
from reviews.forms import CommentForm, ReviewForm
# Create your views here.

def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews,
    }
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

def detail(request,review_detail_pk):
    review = Review.objects.get(pk=review_detail_pk)
    context = {
        'review' : review,
    }
    return render(request,'reviews/detail.html')

# def comment_create(request,review_pk):
#     review = Review.objects.get(pk=review_pk)
#     if request.meth == 'POST':
#         comment_form = CommentForm(request.POST, request.FILES)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.user = request.user
#             comment.review=review
#             comment.save()
#             return redirect("reviews:detail") # 댓글 작성 후 어디로 갈지 회의
#     else:
#         comment_form=()
#     context={
#         comment_form
#     }
#     return render(request,'reviews/comment_create.html')