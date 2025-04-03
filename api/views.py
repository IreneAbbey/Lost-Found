from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from api.models import LostItem, FoundItem, Match 
from .serializers import FoundItemSerializer, LostItemSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")  
        password = request.data.get("password")  

        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password) 

        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status = status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return super().get_object()


@method_decorator(csrf_exempt, name='dispatch')
class LostItemCreateView(generics.CreateAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class LostItemUpdateView(generics.UpdateAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class LostItemDeleteView(generics.DestroyAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"message": "Lost item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class FoundItemCreateView(generics.CreateAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class FoundItemUpdateView(generics.UpdateAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class FoundItemDeleteView(generics.DestroyAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_exempt, name='dispatch')
class FindMatchView(APIView):
    def get(self, request):
        lost_item = LostItem.objects.filter(status= "pending")
        found_item = FoundItem.objects.filter(status= "pending")
        matched_item = []

        for lost in lost_item:
            for found in found_item:
                name_score = 0.4 if lost.item_name.lower() == found.name.lower() else 0
                description_score = 0.1 if lost.description.lower() == found.description.lower() else 0
                keyword_score = 0.3 if any(word in found.item_name.lower() for word in lost.item_name.lower().split()) else 0
                location_score = 0.2 if lost.location.lower() == found.location.lower() else 0
                vehicle_score = 0.1 if lost.vehicle_type == found.vehicle_type else 0
                vehicle_description_score = 0.1 if lost.vehicle_description.lower() == found.vehicle_description.lower() else 0

                match_score = name_score + description_score + keyword_score + location_score + vehicle_score + vehicle_description_score
                if match_score > 0.7:
                    match = Match.objects.create(lost_item=lost, found_item=found, match_score=match_score, date_match= now())
                    lost.status = "matched"
                    lost.save()
                    found.status = "matched"
                    found.save()

                    matched_item.append({
                        "lost_item": lost.item_name,
                        "found_item": found.item_name,
                        "match_score": match_score,
                        "location": lost.location,
                    })
        return Response({"matches": matched_item}, status=status.HTTP_201_CREATED)