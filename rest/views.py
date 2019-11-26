from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import ConfessionSerializer
from .models import Confession
from rest_framework.response import Response
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
        confession = Confession.objects.get(pk=id)
        serialized_confession = ConfessionSerializer(confession)
        return Response(sserialized_confession.data)

    @action(methods=['put'], detail=True)
    def put(self, request, id):
        return Response(dict(error='Not implemented'),status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['delete'], detail=True)
    def delete(self, request, id):
        ConfessionSerializer.delete(id)
        return Response(dict(error='Deleted id: {}'.format(id)),status=status.HTTP_200_OK)

    