from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    """ Class for create User """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]