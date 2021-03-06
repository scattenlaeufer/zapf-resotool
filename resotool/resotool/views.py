"""
Collection of all views of resotool
"""

from django.views import generic

from .models import Resolution, ResolutionEmail


class ResolutionListView(generic.ListView):
    """
    View to get a list of all Resolution objects
    """

    def get_queryset(self):
        return Resolution.objects.all().order_by("-date_submitted")


class ResolutionView(generic.DetailView):
    """
    View to get the details of one Resolution object
    """

    model = Resolution


class ResolutionEmailListView(generic.ListView):
    """
    View to get a list of all resolution emails
    """

    def get_queryset(self):
        return ResolutionEmail.objects.all().order_by("-pk")


class ResolutionEmailView(generic.DetailView):
    """
    View to get the details of one resolution email
    """

    model = ResolutionEmail
