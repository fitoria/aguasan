 # -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse
from mapeo.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def formulario(request):
	return render_to_response('mapeo/formulario.html',context_instance=RequestContext(request))

