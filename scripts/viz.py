#!/usr/bin/env python

import os
import sys

try:
    import gviz_api
except:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/google-visualization-python")
    import gviz_api

try:
    import ompl_benchmark
except:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ompl-benchmark")
    import ompl_benchmark

def toJson(tbl):
    data_table = gviz_api.DataTable(tbl.description)
    data_table.LoadData(tbl.data)
    return data_table.ToJSon(columns_order=[c[0] for c in tbl.description], order_by=tbl.orderby)

def getExperimentImages(exps):
    """ Given experiment names, find image files with the same name, to construct the links to the experiments """
    pth = {}
    for x in os.walk('../problems'):
        for f in x[2]:
            (nm, ext) = os.path.splitext(f)
            if ext == ".jpg" or ext == ".png":
                if nm in exps:
                    pth[nm] = [os.path.join(x[0], f)]
                    solved_fnm = os.path.join(x[0], nm + "_solved" + ext)
                    if os.path.isfile(solved_fnm):
                        pth[nm].append(solved_fnm)
    return pth

def main():
    b = ompl_benchmark.OMPLBenchmark("../db/benchmark.db")
    print b.getExperimentNames()
    print toJson(b.getGeometricPlannersTable('cubicles_se3'))


if __name__ == "__main__":
    main()
