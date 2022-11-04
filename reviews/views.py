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


# djanog template 문법을 보던가
# views.py에서 filter attribute로 접근해봅시다.

def index(request):
    reviews = Review.objects.all()
    mor = Comment.objects.filter(tag__contains='morning')
    mor_list=[]
    memoM = []
    for i in range(len(mor)):
        if mor[i].review_id not in memoM:
            mor_list.append(mor[i])
            memoM.append(mor[i].review_id)

    lun = Comment.objects.filter(tag__contains='lunch')
    lun_list=[]
    memoL = []
    for i in range(len(lun)):
        if lun[i].review_id not in memoL:
            lun_list.append(lun[i])
            memoL.append(lun[i].review_id)

    din = Comment.objects.filter(tag__contains='dinner')
    din_list=[]
    memo = []
    for i in range(len(din)):
        if din[i].review_id not in memo:
            din_list.append(din[i])
            memo.append(din[i].review_id)

    sna = Comment.objects.filter(tag__contains='midnight_snack')
    sna_list=[]
    memoS = []
    for i in range(len(sna)):
        if sna[i].review_id not in memoS:
            sna_list.append(sna[i])
            memoS.append(sna[i].review_id)     
    context = {
        'reviews' : reviews,
        'tag_morning' : mor_list,
        'tag_lunch' : lun_list,
        'tag_dinner' :din_list,
        'tag_midnight_snack' :sna_list,
        # 'list_review' : list_review, 
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
        "re":review,
    }
    return render(request, "reviews/update.html", context)

@login_required
def delete(request,detail_pk):
    if request.method=='POST':
        review = Review.objects.get(pk=detail_pk)
        review.user = request.user
        review.delete()
        return redirect('reviews:index')
    else:
        return redirect('reviews:detail', detail_pk)

# 테스트용 함수
def mapmap(request):
    reviews = Review.objects.all()
    comment_morning = Comment.objects.filter(tag__contains='morning')
    comment_lunch = Comment.objects.filter(tag__contains='lunch')
    comment_dinner = Comment.objects.filter(tag__contains='dinner')
    comment_midnight_snack = Comment.objects.filter(tag__contains='midnight_snack')
    
    context = {
        'reviews' : reviews,
        'comment_morning' : comment_morning,
        'comment_lunch' : comment_lunch,
        'comment_dinner' :comment_dinner, 
        'comment_midnight_snack' :comment_midnight_snack,
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
    