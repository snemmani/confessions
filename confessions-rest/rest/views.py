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
    def get(self, request, id):
        try:
            confession = Confession.objects.get(pk=id)
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
    def put(self, request, id):
        return Response(dict(error='Not implemented'),status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, id):
        try:
            ConfessionSerializer.delete(id)
            return Response(dict(message='Confession with id: {} deleted'.format(id)),status=status.HTTP_200_OK)
        except Confession.DoesNotExist:
            return Response(dict(error='Confession with id: {} not found'.format(id)),status=status.HTTP_404_NOT_FOUND)


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
            print(request.auth)
            print(request.user)
            confession = Confession.objects.get(pk=confession_id)
            validated_data = json.loads(request.body)

            comment = CommentSerializer.create(
                confession,
                validated_data
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
        
        