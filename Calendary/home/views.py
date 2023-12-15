import datetime
from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.datetime.now()
        context['year'], context['month'] = date.year,date.month
        return context