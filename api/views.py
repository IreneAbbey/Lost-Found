from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from api.models import LostItem, FoundItem, Match 
from .serializers import FoundItemSerializer, LostItemSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


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
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_protect, name='dispatch')
class LostItemCreateView(generics.CreateAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@method_decorator(csrf_protect, name='dispatch')
class LostItemUpdateView(generics.UpdateAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class LostItemDeleteView(generics.DestroyAPIView):
    serializer_class = LostItemSerializer
    queryset = LostItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({"message": "Lost item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_protect, name='dispatch')
class FoundItemCreateView(generics.CreateAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(csrf_protect, name='dispatch')
class FoundItemUpdateView(generics.UpdateAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class FoundItemDeleteView(generics.DestroyAPIView):
    serializer_class = FoundItemSerializer
    queryset = FoundItem.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]



class FindMatchView(APIView):
    def get(self, request):
        lost_items = LostItem.objects.filter(status="pending")
        found_items = FoundItem.objects.filter(status="pending")
        matched_items = []

        for lost in lost_items:
            for found in found_items:
                name_score = 0.4 if lost.name.lower() == found.name.lower() else 0
                description_score = 0.1 if lost.description.lower() == found.description.lower() else 0
                keyword_score = 0.3 if any(word in found.name.lower() for word in lost.name.lower().split()) else 0
                location_score = 0.2 if lost.location.lower() == found.location.lower() else 0
                vehicle_score = 0.1 if lost.vehicle_type == found.vehicle_type else 0
                vehicle_description_score = 0.1 if lost.vehicle_description.lower() == found.vehicle_description.lower() else 0

                match_score = name_score + description_score + keyword_score + location_score + vehicle_score + vehicle_description_score

                if match_score > 0.7:
                    match = Match.objects.create(
                        lost_item=lost, 
                        found_item=found, 
                        match_score=match_score, 
                        date_match=timezone.now()
                    )
                    lost.status = "matched"
                    lost.save()
                    found.status = "matched"
                    found.save()

                    matched_items.append({
                        "lost_item": lost.name,
                        "found_item": found.name,
                        "match_score": match_score,
                        "location": lost.location,
                    })
        
        return Response({"matches": matched_items}, status=status.HTTP_200_OK)
