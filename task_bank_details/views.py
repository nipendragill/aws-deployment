from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .Serializers.user_serialzer import UserSerializer
from .Serializers.bank_serializer import BankSerializer, BranchesReadSerializer, BranchesWriteSerializer
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
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        request.data['password'] = make_password(salt='ryan',password=request.data['password'])
        transaction.set_autocommit(False)
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.is_valid(raise_exception=True)
                serializer.save()
                transaction.commit()
                transaction.set_autocommit(True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                transaction.rollback()
                transaction.set_autocommit(False)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            transaction.rollback()
            transaction.set_autocommit(False)
            return Response({'detail':'Database error occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        bank_data = request.data
        transaction.set_autocommit(False)
        try:
            context = {"data": request.data}
            serializer_class = BankSerializer(data=bank_data, context=context)
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


class BranchesView(generics.ListCreateAPIView):

    def post(self, request):

        data = request.data

        bank_id = request.data.get('bank')
        transaction.set_autocommit(False)
        try:
            bank_id_exists = Bank.objects.filter(bank_id=bank_id)
            if not bank_id_exists:
                return Response('BankId doesnot exists',
                                status=status.HTTP_400_BAD_REQUEST)
            serializer_class = BranchesWriteSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                transaction.commit()
                transaction.set_autocommit(True)
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response('Database error occured',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankBranchDetails(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = BranchesReadSerializer
    pagination_class = CustomPagination

    def get_queryset(self, bank_name=None, city_name=None):
        queryset = Branches.objects.select_related('bank').filter(bank__name=bank_name, city=city_name)
        queryset = self.paginate_queryset(queryset)
        return queryset, None

    def get(self, request):
        bank_name = request.query_params.get('bank_name')
        city_name = request.query_params.get('city_name')
        if bank_name is None or city_name is None:
            return Response({'detail': 'Both bank name and city name is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        bank_name = bank_name.upper()
        city_name = city_name.upper()
        data, error = self.get_queryset(bank_name=bank_name, city_name=city_name)
        if error is not None:
            return Response({'detail': error.message},
                            status=status.HTTP_400_BAD_REQUEST)
        serialized_data = BranchesReadSerializer(data, many=True).data

        return self.get_paginated_response(serialized_data)


class BankIFSCDetails(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, ifsc_code=None):
        try:
            bank_details = Branches.objects.filter(ifsc_code=ifsc_code)

            if bank_details.exists():
                return bank_details.first(), None
            else:
                error = Error({'detail': 'IFSC code doesnot exists'},
                              status=status.HTTP_400_BAD_REQUEST)
                return None, error
        except DatabaseError as e:
            error = Error({'detail': 'Ifsc code does not exist'},
                          status=status.HTTP_400_BAD_REQUEST)
            return None, error

    def get(self, request):

        ifsc_code = request.query_params.get('ifsc_code')
        if ifsc_code is None:
            return Response({'detail': 'Please provide ifsc code'},
                            status=status.HTTP_400_BAD_REQUEST)

        data, error = self.get_queryset(ifsc_code=ifsc_code)

        if data is not None:
            serializer_class = BranchesReadSerializer(data)
            return Response({'results': serializer_class.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': error.message},
                            status=error.status)



@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = make_password(salt='ryan', password=request.data['password'])
        if email is None or password is None:
            return Response({'detail':'Both email and password are required'},
                             status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email, password=password)
        if user.exists():
            try:
                user = user.first()
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
                'error': 'No user exists with this name and password'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'detail':'User does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)