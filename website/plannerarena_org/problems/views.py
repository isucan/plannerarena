from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
import sys
import os

try:
    import ompl_benchmark
except:
    sys.path.append("/home/isucan/plannerarena.org/repo/scripts/ompl-benchmark")
    import ompl_benchmark
    
benchmark = ompl_benchmark.OMPLBenchmark("repo/db/benchmark.db")

def index(request):
    return render_to_response('problems/index.html', {'request' : request, 'page_content': "test" }, 
                              context_instance=RequestContext(request))

def list_experiments(request, exps):
    content = ''
    if len(exps) == 0:
        content = "<h2>There are no experiments</h2>\n"
    else:
        content = "<h2>List of experiments</h2>\n"
    for e in exps:
        content += '<h3>' + e + '</h3><img width="150" src="/static/problems/' + e + '.png"/>' + '</p><img width="150" src="/static/problems/' + e + '_solved.png"/>'

    return render_to_response('problems/index.html', {'request' : request, 'page_content': mark_safe(content) }, 
                              context_instance=RequestContext(request))

def subindex_geometric(request):
    return list_experiments(request, benchmark.getGeometricExperimentNames())

def subindex_control(request):
    return list_experiments(request, benchmark.getControlExperimentNames())
