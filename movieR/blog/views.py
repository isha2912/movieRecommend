from django.shortcuts import render
from scipy import sparse
from django.http import HttpResponse
# Create your views here.
import os
import pickle
import random
import pandas as pd
from django.http import JsonResponse
from csv import writer
import datetime

def models(request):
    filename=os.path.dirname(os.path.abspath(__file__))+'/movies_pickle'
    with open(filename,'rb') as f:
        model=pickle.load(f)
    return model

def home(request):
    model=models(request)
    movie=[]
    s=model.index.size
    for i in range(21):
        r=random.randint(1,s)
        movie.append(model.index[r])
    return render(request,'home.html',{'movies':movie})

def detail(request):
    model=models(request)
    movie=request.GET['movie']
    if movie in model.index:
        return render(request,'detail.html',{'movie':movie})
    else:
        return render(request,'detail.html',{'movie':movie,'message':'Movie Not found'})

def get_similar(request,movie_name,rating):
    model=models(request)
    similar_ratings=model[movie_name]*(rating-2.5)
    similar_ratings=similar_ratings.sort_values(ascending=False)
    return similar_ratings

def recommend_movie(request,movie_collection):
    similar_movies=pd.DataFrame()
    for movie,rating in movie_collection:
        similar_movies=similar_movies.append(get_similar(request,movie,rating),ignore_index=True)
    movies=similar_movies.sum().sort_values(ascending=False).head(9).index
    return movies

def recommendation(request):
    #record=os.path.dirname(os.path.abspath(__file__)*'/record.csv')
   
    movie=request.GET['movie']
    rating=request.GET['ratings']

    
    movie_collection=[]
    movie_collection.append((movie,int(rating)))
    movies=recommend_movie(request, movie_collection)
    return render(request,'recommendation.html',{'movies':movies,'m':movie})

# def Search(request):
#     model=reading_pickle(request)
#     mName=request.GET['q']
#     value=[val for val in model.index if val.startswith(mName.title())]
#     return JsonResponse({'movie':value[:10]})

