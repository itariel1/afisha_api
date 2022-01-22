from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collection.serializers import MovieListSerializer, MovieReviewSerializer, CinemaListSerializer, GenreListSerializer, MovieValidateSerializer
from .models import Movie, Review, Cinema, Genre
from rest_framework import status
# Create your views here.

@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieListSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        print(request.data)
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors':serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data['title']
        description = request.data['description']
        cinema_id = request.data['cinema_id']
        genres = request.data['genres']
        movie = Movie.objects.create(
            title=title,
            description=description,
            cinema_id=cinema_id,
        )
        movie.save()
        movie.genres.set(genres)
        for i in request.data['reviews']:
            Review.objects.create(
                author=i['author'],
                text=i['text'],
                movie=movie,
            )
        movie.save()
        return Response(data={'message': 'The movie was created!'})

@api_view(['GET', 'PUT', 'DELETE'])
def movie_item_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'Message': 'Movie not found!!!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieListSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={'Message': 'Movie removed!'})
    else:
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors':serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data['title']
        description = request.data['description']
        cinema_id = request.data['cinema_id']
        genres = request.data['genres']
        movie.title = title
        movie.description = description
        movie.cinema_id = cinema_id
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieListSerializer(movie).data)

@api_view(['GET'])
def get_review(request, id):
    try:
        product = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieReviewSerializer(product).data
    return Response(data=data)


@api_view(['GET'])
def cinema_view(request):
    cinemas = Cinema.objects.all()

    data = CinemaListSerializer(cinemas, many=True).data
    return Response(data=data)

@api_view(['GET'])
def genre_view(request):
    genres = Genre.objects.all()

    data = GenreListSerializer(genres, many=True).data
    return Response(data=data)