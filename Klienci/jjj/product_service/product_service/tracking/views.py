# tracking/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TrackClickSerializer

class TrackClickView(APIView):
    def post(self, request, format=None):
        serializer = TrackClickSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Zapisuje dane w bazie
            return Response({'message': 'Zdarzenie zapisane'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
