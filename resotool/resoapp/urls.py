"""
Configuation of all URLs used in resoapp
"""

from django.urls import path

from . import views

app_name = "resoapp"
urlpatterns = [
    path("", views.ResolutionListView.as_view(), name="index"),
    path("<int:pk>/", views.ResolutionView.as_view(), name="resolution"),
    path("email/", views.ResolutionEmailListView.as_view(), name="email"),
    path('email/<int:pk>/', views.ResolutionEmailView.as_view(), name="emaildetail")
]
