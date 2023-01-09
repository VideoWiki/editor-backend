from django.urls import path, include
from .views import add_subscribe, add_volunteer, contactForm,ChainLink

urlpatterns = [
    path('subscribe/', add_subscribe.as_view()),
    path('volunteer/', add_volunteer.as_view()),
    path('contact_us/', contactForm.as_view()),

    path('chainlink/<str:pk>/', ChainLink.as_view())
]
