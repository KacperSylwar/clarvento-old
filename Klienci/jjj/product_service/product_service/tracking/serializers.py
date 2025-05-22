# tracking/serializers.py
from rest_framework import serializers
from .models import TrackClick

class TrackClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackClick
        fields = ['product_id', 'action', 'timestamp']
