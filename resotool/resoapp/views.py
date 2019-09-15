"""
Collection of all views of resoapp
"""

from django.views import generic

from .models import Resolution


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
