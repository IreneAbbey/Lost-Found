from django.urls import path
from.views import FindMatchView, FoundItemCreateView, FoundItemDeleteView, FoundItemUpdateView, LostItemCreateView, LostItemDeleteView, LostItemUpdateView, RegisterView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('lost-items/', LostItemCreateView.as_view(), name='lost_items_create'),
    path('lost-items/<int:pk>/', LostItemUpdateView.as_view(), name='lost_items_update'),
    path('lost-items/<int:pk>/delete/', LostItemDeleteView.as_view(), name='lost_items_delete'),
    path('found-items/', FoundItemCreateView.as_view(), name='found_items_create'),
    path('found-items/<int:pk>/', FoundItemUpdateView.as_view(), name='found_items_update'),
    path('found-items/<int:pk>/delete/', FoundItemDeleteView.as_view(), name='found_items_delete'),
    path('find/', FindMatchView.as_view(), name='find_match'),
]