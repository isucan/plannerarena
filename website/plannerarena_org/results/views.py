from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
import sys
import os

try:
    import gviz_api
except:
    sys.path.append("/home/isucan/plannerarena.org/repo/scripts/google-visualization-python")
    import gviz_api

try:
    import ompl_benchmark
except:
    sys.path.append("/home/isucan/plannerarena.org/repo/scripts/ompl-benchmark")
    import ompl_benchmark

benchmark = ompl_benchmark.OMPLBenchmark("/home/isucan/plannerarena.org/repo/db/benchmark.db")

def toJson(tbl):
    data_table = gviz_api.DataTable(tbl.description)
    data_table.LoadData(tbl.data)
    return data_table.ToJSon(columns_order=[c[0] for c in tbl.description], order_by=tbl.orderby)

def hw():
    x = " "#.join(getattr(problems, benchmark).getExperimentNames())
    return "Hello, world. You're at the poll index." + x

def getJsTables(tables):
    table_template = """
<script src="https://www.google.com/jsapi" type="text/javascript"></script>
<script>
    google.load('visualization', '1', {packages:['table', 'corechart', 'motionchart']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
      %s
    }
  </script>
"""
    js = ""
    div = ""
    for t in tables:
        js += t[0]
        div += t[1]
    return (table_template % js, div)
    
def getJsTable(name, json, chart = True):
    from string import replace
    tname = replace(name, " ", "_")
    js = "var json_data_%s = new google.visualization.DataTable(%s, 0.6);\n\n" % (tname, json)
    if chart:
        js = js + "var json_chart_%s = new google.visualization.MotionChart(document.getElementById('chart_div_%s'));\n" % (tname, tname)
        js = js + "var chart_%s_options = {};\n" % tname
        js = js + "chart_%s_options['state'] = '{\"playDuration\":1500}';\n" % tname
        js = js + "chart_%s_options['width'] = 640;\n" % tname
        js = js + "chart_%s_options['height'] = 420;\n" % tname
        js = js + "json_chart_%s.draw(json_data_%s, chart_%s_options);\n" % (tname, tname, tname)
    else:
        js = js + "var json_table_%s = new google.visualization.Table(document.getElementById('table_div_%s'));\n" % (tname, tname)
        js = js + "json_table_%s.draw(json_data_%s, {showRowNumber: false});\n" % (tname, tname)
    div = ""
    if chart:
        div = '<h2>%s</h2><div id="chart_div_%s"></div>' % (name, tname)
    else:
        div = '<h2>%s</h2><div id="table_div_%s"></div>' % (name, tname)
    return [js, div]

def index(request):
    tables = []
    tables.append(getJsTable("all_exps", toJson(benchmark.getExperimentsTable()), False))
    exps = benchmark.getGeometricExperimentNames()
    for e in exps:
        tables.append(getJsTable(e, toJson(benchmark.getGeometricPlannersTable(e)), True))

    (js, div) = getJsTables(tables)
    content = js + div
    return render_to_response('results/index.html', {'request' : request, 'page_content': mark_safe(content) }, 
                              context_instance=RequestContext(request))

#def subindex(request):
#    return render_to_response('results/index.html', {'request' : request, 'page_content': 'sub page!' }, 
#                              context_instance=RequestContext(request))
