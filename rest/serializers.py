from rest_framework import serializers
from .models import Confession, Comment
from django.db import models
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    text = serializers.CharField(max_length=2000)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created']

class ConfessionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    heading = serializers.CharField()
    text = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)
    comments = CommentSerializer(
        many=True,
        read_only=True,
        source="filter_deleted_comment"
    )

    @staticmethod
    def create(validated_data):
        """
        Create and return a new Confession instance
        """
        return ConfessionSerializer(Confession.objects.create(**validated_data))

    @staticmethod
    def delete(id):
        """
        Delete the Confession instance
        """
        confession = Confession.objects.get(pk=id)
        if confession.deleted:
            raise Confession.DoesNotExist()
        else:
            confession.deleted = True
        confession.save()

    class Meta:
        model = Confession
        fields = ['id', 'heading', 'text', 'created', 'comments']
