from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ReportFoundItemView, ReportLostItemView, UserMatchesView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('lost/', ReportLostItemView.as_view()),
    path('found/', ReportFoundItemView.as_view()),
    path('matches/', UserMatchesView.as_view()),
]