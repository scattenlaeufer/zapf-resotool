from django.views import generic

from .models import Resolution, ResolutionEmail


class ResolutionListView(generic.ListView):
    def get_queryset(self):
        return Resolution.objects.all().order_by("-date_submitted")


class ResolutionView(generic.DetailView):
    model = Resolution


class ResolutionEmailListView(generic.ListView):

    def get_queryset(self):
        return ResolutionEmail.objects.all().order_by("-pk")


