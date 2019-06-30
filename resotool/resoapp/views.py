from django.shortcuts import render
from django.views import generic

from .models import Resolution


class ResolutionListView(generic.ListView):
    def get_queryset(self):
        return Resolution.objects.all().order_by("-date_submitted")


class ResolutionView(generic.DetailView):
    model = Resolution
