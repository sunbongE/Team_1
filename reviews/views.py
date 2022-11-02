from django.http import JsonResponse
from django.shortcuts import render,redirect
from reviews.models import Review,Comment
from reviews.forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
def main(request):
    return render(request,'reviews/main.html')

def search(request):
    if request.method=='POST':
        searched = request.POST['searched']
        reviews = Review.objects.filter(store_name__contains=searched)
        context = {
            'searched' : searched,
            'reviews' : reviews,
        }
        return render(request, 'reviews/search.html', context)
    else:
        return render(request, 'reviews/search.html')



def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews,
    }
    return render(request, 'reviews/index.html',context)
    
@login_required
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


@login_required
def comment_create(request,detail_pk):
    review = Review.objects.get(pk=detail_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review=review
            comment.user = request.user
            comment.save()
            return redirect("reviews:detail", detail_pk) 
   
   
    return redirect("reviews:detail", detail_pk) 

@login_required
def comment_delete(request,detail_pk,comment_pk):
    comment = Comment.objects.get(pk=comment_pk) # 어떤 댓글인지?(리뷰)
    if request.method=='POST' and comment.user == request.user :
        comment.delete()
        return redirect('reviews:detail', detail_pk)
    else:
        return redirect('reviews:detail', detail_pk)
    
def detail(request,detail_pk):
    review = Review.objects.get(pk=detail_pk)
    comment_form = CommentForm
    comments = review.comment_set.all()

    context = {
        'comment_form':comment_form,
        'review' : review,
        'comments':comments,
    }
    return render(request,'reviews/detail.html',context)


@login_required
def update(request,detail_pk):
    review = Review.objects.get(pk=detail_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:detail", detail_pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        "form": form,
    }
    return render(request, "reviews/create.html", context)

@login_required
def delete(request,detail_pk):
    if request.method=='POST':
        review = Review.objects.get(pk=detail_pk)
        review.user = request.user
        review.delete()
        return redirect('reviews:index')
    else:
        return redirect('reviews:detail', detail_pk)

# 테스트용 map 함수
def mapmap(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews,
        'adrs_js': json.dumps([review.json() for review in reviews])
    }
    return render(request, 'reviews/map.html', context)


def favorites(request,review_pk):
    review = Review.objects.get(pk=review_pk)

    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        is_favorites = False
    else:
        review.like_users.add(request.user) 
        is_favorites=True   
    data = {'is_favorites':is_favorites,'favorites_count':review.like_users.count()}
    return JsonResponse(data)
    