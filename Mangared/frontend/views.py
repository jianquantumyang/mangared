from django.shortcuts import render
from django.views.generic import TemplateView

def index(request,mangauuid=None,uuid=None):
    return render(request, 'frontend/index.html')


class ServiceWorkerView(TemplateView):
    template_name = 'sw.js'
    content_type = 'application/javascript'
    name = 'sw.js'
