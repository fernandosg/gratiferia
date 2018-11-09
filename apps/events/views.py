from django.shortcuts import render
from django.views import View
from datetime import datetime
from .models import Event
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class EventListView(View):

    def get(self, request, *args, **kwargs):
        events_list = Event.objects.filter(date_event__gte=datetime.now()).all()
        title = "Lista de eventos"
        page = request.GET.get("page")
        paginator = Paginator(events_list, 12)
        events = paginator.get_page(page)
        return render(request, "events/index.html", locals())


class EventDetailView(View):

    @property
    def id(self):
        if "id" in self.kwargs:
            return self.kwargs["id"]
        return None

    def get(self, request, *args, **kwargs):
        id = self.id
        if id is None:
            return HttpResponseForbidden()
        event = Event.objects.filter(id=id).first()
        if event is None:
            return HttpResponseForbidden()
        title = "Evento el {}".format(event.date_event.strftime("%w/%m/%Y %H:%M"))
        return render(request, "events/detail.html", locals())
