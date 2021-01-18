from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin
from ..serializers import LogupSerializer
from VolgaREST.root.models import UserModel

class LogupViewSet(GenericViewSet, CreateModelMixin):
   
   serializer_class = LogupSerializer
   queryset = UserModel.objects.all()
   authentication_classes = permission_classes = []

   def create(self, request):
      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      authtoken = Token.objects.create(user=user)
      return Response(
         data={
            'credentials': {
               'username': user.username,
               'password': user.password
            },
            'token': authtoken.key
         },
         status=HTTP_201_CREATED)
