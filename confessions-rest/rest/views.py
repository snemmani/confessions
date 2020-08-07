from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action, authentication_classes, permission_classes
from .serializers import ConfessionSerializer, CommentSerializer
from .models import Confession, Comment
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from json.decoder import JSONDecodeError
from django.shortcuts import get_object_or_404


# Create your views here.
class ConfessionListView(APIView):
    @action(methods=['get'], detail=False)
    def get(self, request):
        confessions = Confession.objects.filter(deleted=False)
        if confessions.count() > 0:
            confessions_serializer = ConfessionSerializer(confessions, many=True)
            return Response(confessions_serializer.data)
        else:
            return Response(Confession.objects.none())

    @action(methods=['post'], detail=True)
    def post(self, request):
        try:
            request_body = json.loads(request.body)
        except JSONDecodeError:
            return Response(
                dict(error='Failed to read provided request data. JSON data format is invalid'),
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ConfessionSerializer()
        try:
            response = ConfessionSerializer.create(request_body)
        except TypeError as e:
            return Response(
                dict(
                    error=e.args[0]
                )
            )

        return Response(response.data, status=status.HTTP_201_CREATED)


class ConfessionDetailView(APIView):
    @action(methods=['get'], detail=False)
    def get(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)
            if not confession.deleted:
                serialized_confession = ConfessionSerializer(confession)
                return Response(serialized_confession.data)
            else:
                raise Confession.DoesNotExist()
        except Confession.DoesNotExist:
            return Response(
                dict(
                    error="Confession with id: {} not found".format(id)
                ),
                status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=['put'], detail=True)
    def put(self, request, confession_id):
        return Response(dict(error='Not implemented'), status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, confession_id):
        try:
            ConfessionSerializer.delete(id)
            return Response(dict(message='Confession with id: {} deleted'.format(id)), status=status.HTTP_200_OK)
        except Confession.DoesNotExist:
            return Response(dict(error='Confession with id: {} not found'.format(id)), status=status.HTTP_404_NOT_FOUND)


class CommentListView(APIView):
    @action(methods=['get'], detail=False)
    def get(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)
        except Confession.DoesNotExist as e:
            return Response(dict(
                error="Confession with id: {} not found".format(id)
            ),
                status=status.HTTP_404_NOT_FOUND
            )

        comments = Comment.objects.filter(
            confession=confession
        ).order_by(
            '-id'
        )

        if comments.count() > 0:
            comments_serializer = CommentSerializer(comments, many=True)
            return Response(comments_serializer.data)
        else:
            return Response(Comment.objects.none())

    @action(methods=['post'], detail=True)
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)

            comment = CommentSerializer.create(
                confession,
                request.user,
                request.data
            )

            serializer = CommentSerializer(comment)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Confession.DoesNotExist:
            return Response(
                dict(
                    error='Confession with id: {} does not exist'
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        except JSONDecodeError:
            return Response(
                dict(
                    error='Received corrupt JSON data'
                ),
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentDetailView(APIView):
    @action(methods=['put'], detail=True, description='Modify a comment')
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user.id != comment.user.id:
            return Response(
                dict(
                    error='Unauthorized'
                ),
                status=status.HTTP_401_UNAUTHORIZED
            )
        for attribute in request.data:
            if hasattr(comment, attribute):
                setattr(comment, attribute, request.data[attribute])
            else:
                return Response(
                    dict(
                        error='Invalid attribute for comment: {}'.format(attribute)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )

        comment.save()

        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


