from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .Serializers.user_serialzer import UserSerializer
from .Serializers.bank_serializer import BankSerializer, BankDetailsReadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import User, Bank, Branches
from rest_framework_jwt.settings import api_settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
from django.db import transaction, DatabaseError
from rest_framework import request
from .error import Error


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BankAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):

        id = request.data.get('bank_id')
        if not isinstance(id, int):
            return Response({'detail': 'Please provide Integer BankId'},
                            status=status.HTTP_400_BAD_REQUEST)
        bank_data = request.data

        transaction.set_autocommit(False)
        try:
            serializer_class = BankSerializer(data=bank_data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                transaction.commit()
                transaction.set_autocommit(True)
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': serializer_class.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as ex:
            transaction.rollback()
            transaction.set_autocommit(True)
            return Response({'detail': 'Error inserting database'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self, ifsc_code=None):

        try:
            bank_details = Branches.objects.filter(ifsc_code=ifsc_code)
            return bank_details, None
        except DatabaseError as e:
            error = Error({'detail':'Ifsc code does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
            return None, error


    def get(self, request):
        ifsc_code = request.data.get('ifsc_code')
        if ifsc_code is None:
            return Response({'detail': 'Please provide ifsc code'},
                            status=status.HTTP_400_BAD_REQUEST)

        data, error = self.get_queryset(ifsc_code=ifsc_code)

        if data is not None:
            serializer_class = BankDetailsReadSerializer(self.get_queryset(ifsc_code))
            return Response({'results': serializer_class.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail':error.message },
                            status=error.status)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                user_details = {}
                user_details['name'] = f'{user.first_name} {user.last_name}'
                user_details['token'] = token
                user_details['email'] = user.email
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'account is currently inactive, please activate your account'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'pleasae provide email address and password'}
        return Response(res)