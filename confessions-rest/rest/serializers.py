from rest_framework import serializers
from .models import Confession, Comment, Vote, vote_choices
from django.db import models
from django.contrib.auth.models import User


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    vote_type = serializers.ChoiceField(choices=vote_choices)

    class Meta:
        model = Vote
        fields = ['user', 'vote_type']


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    text = serializers.CharField(max_length=2000)
    created = serializers.DateTimeField(read_only=True)
    votes = VoteSerializer(many=True, read_only=True, source="get_votes")

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'votes', 'created']

    @staticmethod
    def create(confession, user, validated_data):
        """
        Create and return a new Comment instance
        """
        return Comment.objects.create(
            confession=confession,
            user=user,
            **validated_data
        )

    @staticmethod
    def delete(id):
        """
        Delete the Comment instance
        """
        comment = Comment.objects.get(pk=id)
        if comment.deleted:
            raise Comment.DoesNotExist()
        else:
            comment.deleted = True
        comment.save()


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
