from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView

from user.serializers import UserRegistrationSerializer


@api_view(['GET'])
def health_check(request):
    data = {'message': 'OK'}
    return Response(data)


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        URL: POST https://<server>/api/user/
        유저 생성 함수.
        :param request:
            username            str.
            password            str.
            team                str.
            confirm_password    str.
        :param args:
        :param kwargs:
        :return:
            {
                "id": 6,
                "username": <username>,
                "team": <teamname>,
                "token": "7afe799f775749d4184e9ad7fd277e07590ebd5c"
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token = Token.objects.create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
