from rest_framework import serializers
from .models import Student, Course, Attandance



class AttandanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attandance
        fields = '__all__'

