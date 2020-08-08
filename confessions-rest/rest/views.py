from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action, authentication_classes, permission_classes
from .serializers import ConfessionSerializer, CommentSerializer
from .models import Confession, Comment, Vote, vote_choices
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from json.decoder import JSONDecodeError
from django.shortcuts import get_object_or_404
from .helper import get_response, get_error_response, do_vote
from .permissions import ReadOnly


# Create your views here.
class ConfessionListView(APIView):
    @action(methods=['get'], detail=False)
    def get(self, request):
        confessions = Confession.objects.filter(deleted=False)
        if confessions.count() > 0:
            confessions_serializer = ConfessionSerializer(confessions, many=True)
            return get_response(confessions_serializer.data)
        else:
            return get_response(Confession.objects.none())

    @action(methods=['post'], detail=True)
    def post(self, request):
        try:
            request_body = json.loads(request.body)
        except JSONDecodeError:
            return get_error_response('Failed to read provided request data. JSON data format is invalid', status.HTTP_400_BAD_REQUEST)

        serializer = ConfessionSerializer()
        try:
            response = ConfessionSerializer.create(request_body)
        except TypeError as e:
            return get_error_response(e.args[0], status.HTTP_500_INTERNAL_SERVER_ERROR)

        return get_response(response.data, status=status.HTTP_201_CREATED)


class ConfessionDetailView(APIView):
    @action(methods=['get'], detail=False)
    def get(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)
            if not confession.deleted:
                serialized_confession = ConfessionSerializer(confession)
                return get_response(serialized_confession.data)
            else:
                raise Confession.DoesNotExist()
        except Confession.DoesNotExist:
            return get_error_response("Confession with id: {} not found".format(id), status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)
    def put(self, request, confession_id):
        return get_error_response('Not implemented', status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, confession_id):
        try:
            ConfessionSerializer.delete(id)
            return get_response(dict(message='Confession with id: {} deleted'.format(id)), status=status.HTTP_200_OK)
        except Confession.DoesNotExist:
            return get_error_response('Confession with id: {} not found'.format(id), status=status.HTTP_404_NOT_FOUND)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    @action(methods=['get'], detail=False)
    def get(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)
        except Confession.DoesNotExist as e:
            return get_error_response("Confession with id: {} not found".format(id), status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(
            confession=confession
        ).order_by(
            '-id'
        )

        if comments.count() > 0:
            comments_serializer = CommentSerializer(comments, many=True)
            return get_response(comments_serializer.data)
        else:
            return get_response(Comment.objects.none())

    @action(methods=['post'], detail=True)
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, confession_id):
        try:
            confession = Confession.objects.get(pk=confession_id)

            comment = CommentSerializer.create(
                confession,
                request.user,
                request.data
            )

            serializer = CommentSerializer(comment)

            return get_response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Confession.DoesNotExist:
            return get_error_response('Confession with id: {} does not exist', status.HTTP_404_NOT_FOUND)
        except JSONDecodeError:
            return get_error_response('Received corrupt JSON data', status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @action(methods=['put'], detail=True, description='Modify a comment')
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user.id != comment.user.id:
            return get_error_response('Unauthorized', status.HTTP_401_UNAUTHORIZED)

        if 'text' in request.data:
            comment.text = request.data['text']
        else:
            return get_error_response('Expected attribute \'text\', not found', status.HTTP_400_BAD_REQUEST)

        comment.save()

        serializer = CommentSerializer(comment)

        return get_response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, description='Delete a comment')
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.deleted = True
        comment.save()
        return get_response(dict(message='Deleted'), status.HTTP_201_CREATED)


class CommentVoteView(APIView):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True, description='Vote on a comment')
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, comment_id):
        return do_vote('comment', comment_id, request)


class ConfessionVoteView(APIView):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True, description='Vote on a confession')
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def post(self, request, confession_id):
        return do_vote('confession', confession_id, request)
