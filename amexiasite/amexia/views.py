from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Currency, Exchange, Statistic
from django.contrib.auth.models import User
from .serializers import CurrencySerializer, SignUpSerializer, ExchangeSerializer, StatisticSerializer, LoginSerializer
from rest_framework.views import APIView

class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = SignUpSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
            username = serializer.validated_data['username'],
            password = serializer.validated_data['password']
            )
            if user:
                print("user  our ",user)
                refresh = RefreshToken.for_user(user)
                print(refresh)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrencyAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddCurrency(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CurrencySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Currency appended successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExchangeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        exchanges = Exchange.objects.all()
        serializer = ExchangeSerializer(exchanges, many=True)
        return Response(serializer.data)

class AddExchange(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ExchangeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Exchange appended successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatisticAPIView(APIView):
    def get(self, request, *args, **kwargs):
        statistics = Statistic.objects.all()
        serializer = StatisticSerializer(statistics, many=True)
        return Response(serializer.data)




