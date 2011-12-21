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
    
benchmark = ompl_benchmark.OMPLBenchmark("/home/isucan/plannerarena.org/repo/db/benchmark.db")

def index(request):
    return render_to_response('problems/index.html', {'request' : request, 'page_content': "test" }, 
                              context_instance=RequestContext(request))

def list_experiments(request, exps):
    content = "pg"
    return render_to_response('problems/index.html', {'request' : request, 'page_content': mark_safe(content) }, 
                              context_instance=RequestContext(request))

def subindex_geometric(request):
    return list_experiments(request, benchmark.getGeometricExperimentNames())

def subindex_control(request):
    return list_experiments(request, benchmark.getControlExperimentNames())
