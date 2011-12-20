from django.shortcuts import render_to_response
from django.template import RequestContext

def hw():
    return "Hello, world. You're at the poll index."

def index(request):
    return render_to_response('results/index.html', {'request' : request, 'page_content': hw() }, 
                              context_instance=RequestContext(request))

def subindex(request):
    return render_to_response('results/index.html', {'request' : request, 'page_content': 'sub page!' }, 
                              context_instance=RequestContext(request))
