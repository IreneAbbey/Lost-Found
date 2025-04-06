from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from api import models
from api.models import FoundItem, LostItem, Match
from .serializers import LostItemSerializer, RegisterSerializer, LoginSerializer, UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ReportLostItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LostItemSerializer(data=request.data)
        if serializer.is_valid():
            lost_item = serializer.save(user = request.user)
            matches = save_matches_for_lost_item(lost_item)
            return Response({
                "message": "Lost item reported successfully.",
                "saved_matches": matches
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReportFoundItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LostItemSerializer(data=request.data)
        if serializer.is_valid():
            found_item = serializer.save(user = request.user)
            matches = save_matches_for_found_item(found_item)
            return Response({
                "message": "Found item reported successfully.",
                "saved_matches": matches
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def calculate_match_score(lost, found):
    score = 0

    if lost.item_name and found.item_name:
        if lost.item_name.lower() == found.item_name.lower():
            score += 30

    if lost.description and found.description:
        lost_words = set(lost.description.lower().split())
        found_words = set(found.description.lower().split())
        overlap = lost_words.intersection(found_words)
        if overlap:
            desc_score = (len(overlap) / max(len(lost_words), 1)) * 30
            score += desc_score

    if lost.location and found.location:
        if lost.location.lower() == found.location.lower():
            score += 10

    if lost.vehicle_type and found.vehicle_type:
        if lost.vehicle_type.lower() == found.vehicle_type.lower():
            score += 15

    if lost.license_plate and found.license_plate:
        if lost.license_plate.lower() == found.license_plate.lower():
            score += 15

    return round(score, 2)

def save_matches_for_found_item(found_item, threshold=60):
    matches = []
    lost_items = LostItem.objects.all()

    for lost in lost_items:
        score = calculate_match_score(lost, found_item)
        if score >= threshold:
            match = Match.objects.create(
                lost_item=lost,
                found_item=found_item,
                match_score=score
            )
            matches.append({
                "match_score": score,
                "lost_item_id": lost.id,
                "item_name": lost.item_name,
                "reported_by": lost.user.email,
            })

    return matches


def save_matches_for_lost_item(lost_item, threshold=60):
    matches = []
    found_items = FoundItem.objects.all()

    for found in found_items:
        score = calculate_match_score(lost_item, found)
        if score >= threshold:
            match = Match.objects.create(
                lost_item=lost_item,
                found_item=found,
                match_score=score
            )
            matches.append({
                "match_score": score,
                "found_item_id": found.id,
                "item_name": found.item_name,
                "reported_by": found.user.email,
            })

    return matches


class UserMatchesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        matches = Match.objects.filter(
            models.Q(lost_item__user=user) |
            models.Q(found_item__user=user)
        ).select_related("lost_item", "found_item")

        data = []
        for match in matches:
            data.append({
                "match_id": match.id,
                "match_score": match.match_score,
                "lost_item": {
                    "id": match.lost_item.id,
                    "name": match.lost_item.item_name,
                },
                "found_item": {
                    "id": match.found_item.id,
                    "name": match.found_item.item_name,
                },
                "created_at": match.created_at,
            })

        return Response(data)
