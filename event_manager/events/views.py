from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Event, EventRegistration
from .serializers import EventSerializer, UserRegistrationSerializer, EventRegistrationSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date']


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': f"user with name '{user.username}' has been created",
            'api_token': token.key
        }, status=response.status_code)


class EventRegistrationCreateView(generics.CreateAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

        event_title = serializer.validated_data['event'].title
        user_email = user.email
        send_mail(
            'You have successfully registered for an event',
            f'You have successfully registered for the event "{event_title}".',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=True,
        )