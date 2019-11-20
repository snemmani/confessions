from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import ConfessionSerializer
from .models import Confession
from rest_framework.response import Response

# Create your views here.
class ConfessionViewSet(viewsets.ModelViewSet):
    @action(methods=['get'], detail=True)
    def select(self, request):
        confessions = Confession.objects.filter(deleted=False)
        if confessions.count() > 0:
            confessions_serializer = ConfessionSerializer(confessions)
            return Response(confessions_serializer.data)
        else:
            return Response(Confession.objects.none())
        