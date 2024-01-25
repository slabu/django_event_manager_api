from django.urls import path
from .views import EventListCreateView, EventDetailView, UserRegistrationView, EventRegistrationCreateView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('event-registration/', EventRegistrationCreateView.as_view(), name='event-registration'),
]
