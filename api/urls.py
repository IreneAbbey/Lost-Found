from django.urls import path
from.views import FindMatchView, FoundItemCreateView, FoundItemDeleteView, FoundItemUpdateView, LostItemCreateView, LostItemDeleteView, LostItemUpdateView, RegisterView, LoginView, LogoutView, UserProfileView, login_view, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
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