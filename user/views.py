from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import NEW, CODE_VERIFIED
from .models import User
from .serializers import SignUpSerializer


# Create your views here.


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer

class VerifyApi(APIView):
    parser_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.GET.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )

    @staticmethod
    def check_verify(user, code):
        verify = user.verify_codes.filter(
            expiration_time__gte=datetime.now(),
            code=code,
            is_confirmed=False
        ).exists()

        if not verify:
            data = {
                'message': 'Code xato yoki amal qilish muddati o‘tib ketgan'
            }
            raise ValidationError(data)
        else:
            user.updated(is_confirmed=True)

        if user.auth_status == 'NEW':
            user.auth_status = 'CODE_VERIFIED'
        user.save()

        return user
