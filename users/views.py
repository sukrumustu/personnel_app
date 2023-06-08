from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Profile
from .permissions import IsOwnerOrStaff
from rest_framework.permissions import IsAuthenticated

class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class =RegisterSerializer
    
    
    def create(self, request, *args, **kwargs):      # bu fonksiyon aslında CreateAPIView'den gelen ve kullanıcıyı create (register) eden fonksiyon. Ancak oluşturduğumuz Token'ı bize geri dönmesi için bu değişikliği yaptık.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = serializer.data
        data["key"] = token.key     # burada key yerine token dersek register olduğumuzda "token" = ... şeklinde döner
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrStaff, IsAuthenticated]