from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import ConvoySerializer
from .models import Convoy

class ConvoyViewSet(viewsets.ViewSet):
    def create(self, request):
        convoy = request.convoy
        try:
            serializer = ConvoySerializer(data=convoy)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(data=convoy, status=status.HTTP_406_NOT_ACCEPTABLE)

    def alive(self, request, pk=None):
        result = True
        return Response(data=result, status=status.HTTP_200_OK)