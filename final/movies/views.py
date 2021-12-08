from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Comment, Movie
from .forms import CommentForm
import random

# Create your views here.
@require_safe
def index(request):
    if request.user.is_authenticated: 
        movies = Movie.objects.all().order_by('-vote_average','-vote_count')
        me = request.user  
        genre_box = []
        for i in range(len(movies)):
            if movies[i].like_users.filter(pk=me.pk).exists():  # 내가 좋아요를 누른 영화면 아래 코드로
                for j in range(len(movies[i].genre_ids.all())):
                    genre_box.append(movies[i].genre_ids.all()[j])
        genre_box = list(set(genre_box))


        recommended_movies = []
        for i in range(len(movies)):
            if movies[i].like_users.filter(pk=me.pk).exists():
                continue
            for j in range(len(movies[i].genre_ids.all())):
                if movies[i].genre_ids.all()[j] in genre_box:
                    recommended_movies.append(movies[i])
                    break
        
        recommended_movies = recommended_movies[:12]
        random_lsit = []
        while len(random_lsit) <4:
            random_lsit.append(random.randint(0, 11))
            random_lsit = list(set(random_lsit))
        print(random_lsit)

        result = []
        if len(recommended_movies) > 0:
            for i in range(12):
                if i in random_lsit:
                    result.append(recommended_movies[i])
                    
        recommended_movies = result

        movies = Movie.objects.all()
        context = {
            'movies': movies,
            'recommended_movies' : recommended_movies
        }
    else:
        movies = Movie.objects.all()
        context = {
            'movies': movies
        }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie': movie,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@login_required
@require_POST
def comments_delete(request, movie_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user.is_authenticated:
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        context = {
            'liked': liked,
            'count': movie.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')

@login_required
@require_safe
def pay(request, username):
    if request.user.is_authenticated:
        info = get_object_or_404(get_user_model(), username=username)
        context = {
            'info':info,
        }
        return render(request, 'movies/pay.html', context)
    return redirect('accounts:login')