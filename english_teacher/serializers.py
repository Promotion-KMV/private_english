from .models import ReviewsTeacher
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsTeacher
        fields = '__all__'


