from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from collection.models import Cinema, Movie, Review, Genre

class CinemaListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Cinema
        fields = '__all__'

class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def get_cinema(self, obj):
        return CinemaListSerializer(obj.cinema, many=True).data

    def get_genres(self, obj):
        return GenreListSerializer(obj.genres, many=True).data
    

class ReviewValidateSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=100)
    text = serializers.CharField()
    cinema_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=4)
    description = serializers.CharField(min_length=30)
    cinema_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())
    reviews = serializers.ListField(child=ReviewValidateSerializer())

    def validate_title(self, title):
        movies = Movie.objects.filter(title=title)
        if movies.count() > 0:
            raise ValidationError('Movie with this title already exists!')

    def validate_cinema_id(self, cinema_id):
        try:
            Cinema.objects.get(id=cinema_id)
        except Cinema.DoesNotExist:
            raise ValidationError("cinema_id not found!")

    # def validate(self, attrs):
    #     cinema_id = attrs['cinema_id']
    #     try:
    #         Cinema.objects.get(id=cinema_id)
    #     except Cinema.DoesNotExist:
    #         raise ValidationError("cinema_id not found!")