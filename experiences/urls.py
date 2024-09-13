from django.urls import path
from .views import Perks, PerkDetail


urlpatterns = [
    path("perks/", Perks.as_view()),
    path("perk/<int:pk>/", PerkDetail.as_view()),
]
