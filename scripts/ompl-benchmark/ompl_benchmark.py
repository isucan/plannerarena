#!/usr/bin/python
# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

"""Extracts useful tables from a OMPL Benchmark database"""

__author__ = "Ioan Sucan"

import sqlite3

class OMPLTableData(object):
  def __init__(self, description, data, orderby):
    self.description = description
    self.data = data
    self.orderby = orderby

class OMPLBenchmark(object):
  """Loads an OMPL benchmark database"""

  def __init__(self, dbname):
    """ Open the database """    
    self.conn = sqlite3.connect(dbname)
    self.cursor = self.conn.cursor()
    self.cursor.execute('PRAGMA FOREIGN_KEYS = ON')

  def __del__(self):
    self.conn.commit()
    self.cursor.close()

  def getExperimentNames(self):
    self.cursor.execute('SELECT DISTINCT name FROM experiments')
    return [e[0] for e in self.cursor.fetchall()]
    
  def getExperiments(self):
    description = [("name", "string", "Name"), ("count", "number", "Executions"), ("time", "number", "Total Time (s)")]
    data = []
    exps = self.getExperimentNames()
    for e in exps:
      c.execute('SELECT count(id), total(totaltime) FROM experiments WHERE name = "%s"' % e)
      t = c.fetchone()
      data.append((e, t[0], t[1]))
    return OMPLDataTable(description, data, "name")

  def getPlannerNames(self, exp_name):
    """ Get the names of the planners that solve a particular problem """
    from string import replace
    prefix = 'best_' + exp_name + '_'
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    return [replace(str(t[0]), prefix, '') for t in self.cursor.fetchall() if t[0].startswith(prefix)]

  def getPlannerConfigs(self, planner_name, exp_name = None):
    if exp_name == None:
      self.cursor.execute('SELECT DISTINCT plannerid FROM planner_%s ORDER BY plannerid' % planner_name)
    else:
      self.cursor.execute('SELECT DISTINCT plannerid FROM planner_%s INNER JOIN experiments ON planner_%s.experimentid=experiments.id WHERE experiments.name="%s" ORDER BY plannerid' % (planner_name, planner_name, exp_name))
    return [c[0] for c in self.cursor.fetchall()]

  def getPlannersTable(self, exp_name, with_simplification = True):
    from string import replace

    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    view_names = [ str(t[0]) for t in self.cursor.fetchall() if t[0].startswith('best_' + exp_name)]
    
    data = []
    description = [("planner", "string", "Planner name"), ("runs", "number", "Number of runs"), ("time", "number", "Solution time (s)"),
                   ("length", "number", "Solution length"), ("failed", "number", "Failure percentage"), ("states", "number", "Graph states"),
                   ("motions", "number", "Graph motions"), ("smoothness", "number", "Solution smoothness"), ("clearance", "number", "Solution clearance")]

    # best configuration per planner 
    for p in view_names:
      if with_simplification:
        self.cursor.execute('SELECT ifnull(time + simplification_time, 0) as total_time, ifnull(simplified_solution_length, 0) as solution_length, ifnull(simplified_solution_clearance, 0) as solution_clearance, ifnull(simplified_solution_smoothness, 0) as solution_smoothness, ifnull(graph_states, 0) as graph_states, ifnull(graph_motions, 0) AS graph_motions, ifnull(solved = 1 AND crashed = 0 AND correct_solution = 1 AND approximate_solution = 0, 0) AS solved FROM %s' % p)
      else:
        self.cursor.execute('SELECT ifnull(time, 0) as total_time, ifnull(solution_length, 0) as solution_length, ifnull(solution_clearance, 0) as solution_clearance, ifnull(solution_smoothness, 0) as solution_smoothness, ifnull(graph_states, 0) as graph_states, ifnull(graph_motions, 0) AS graph_motions, ifnull(solved = 1 AND crashed = 0 AND correct_solution = 1 AND approximate_solution = 0, 0) AS solved FROM %s' % p)

      nm = replace(p, 'best_' + exp_name + '_geometric_', '')
      rid = 0
      sid = 0
      total_time = 0
      solution_length = 0
      solution_clearance = 0
      solution_smoothness = 0
      graph_states = 0
      graph_motions = 0
      solved = 0
      for r in self.cursor.fetchall():
        rid = rid + 1
        if r[6] == 1:
          solved = solved + 1
          sid = sid + 1
          total_time = total_time + r[0]
          solution_length = solution_length + r[1]
          solution_clearance = solution_clearance + r[2]
          solution_smoothness = solution_smoothness + r[3]
          graph_states = graph_states + r[4]
          graph_motions = graph_motions + r[5]
        if sid == 0:
          data.append((nm, rid + 100, 0, 0, 1.0 - solved / float(rid), 0, 0, 0, 0))
        else:
          data.append((nm, rid + 100, total_time / float(sid), solution_length / float(sid), 1.0 - solved / float(rid),
                       graph_states / float(sid), graph_motions / float(sid), solution_smoothness / float(sid), solution_clearance / float(sid)))
    return OMPLTableData(description, data, "planner")
    
  def getPlannerConfigs(self, exp_name, p_name, with_simplification = True):
    data = []
    description = [("config", "string", "Planner configuration"), ("runs", "number", "Number of runs"), ("time", "number", "Solution time (s)"),
                   ("length", "number", "Solution length"), ("failed", "number", "Failure percentage"), ("states", "number", "Graph states"),
                   ("motions", "number", "Graph motions"), ("smoothness", "number", "Solution smoothness"), ("clearance", "number", "Solution clearance")]
    
    if with_simplification:
      self.cursor.execute('SELECT plannerid, ifnull(time + simplification_time, 0) AS total_time, ifnull(simplified_solution_length, 0) AS solution_length, ifnull(simplified_solution_clearance, 0) AS solution_clearance, ifnull(simplified_solution_smoothness, 0) AS solution_smoothness, ifnull(graph_states, 0) AS graph_states, ifnull(graph_motions, 0) AS graph_motions, ifnull(solved = 1 AND crashed = 0 AND correct_solution = 1 AND approximate_solution = 0, 0) AS solved FROM planner_%s INNER JOIN experiments ON planner_%s.experimentid=experiments.id WHERE experiments.name="%s" ORDER BY plannerid' % (p_name, p_name, exp_name))
    else:
      self.cursor.execute('SELECT plannerid, ifnull(time, 0) AS total_time, ifnull(solution_length, 0) AS solution_length, ifnull(solution_clearance, 0) AS solution_clearance, ifnull(solution_smoothness, 0) AS solution_smoothness, ifnull(graph_states, 0) AS graph_states, ifnull(graph_motions, 0) AS graph_motions, ifnull(solved = 1 AND crashed = 0 AND correct_solution = 1 AND approximate_solution = 0, 0) AS solved FROM planner_%s INNER JOIN experiments ON planner_%s.experimentid=experiments.id WHERE experiments.name="%s" ORDER BY plannerid' % (p_name, p_name, exp_name))
                  
    rid = 0
    sid = 0
    total_time = 0
    solution_length = 0
    solution_clearance = 0
    solution_smoothness = 0
    graph_states = 0
    graph_motions = 0
    solved = 0
    last_id = -1
    for r in c.fetchall():
      if last_id != r[0]:
        rid = 0
        sid = 0
        total_time = 0
        solution_length = 0
        solution_clearance = 0
        solution_smoothness = 0
        graph_states = 0
        graph_motions = 0
        solved = 0
        last_id = r[0]
      rid = rid + 1
      if r[7] == 1:
        solved = solved + 1
        sid = sid + 1
        total_time = total_time + r[1]
        solution_length = solution_length + r[2]
        solution_clearance = solution_clearance + r[3]
        solution_smoothness = solution_smoothness + r[4]
        graph_states = graph_states + r[5]
        graph_motions = graph_motions + r[6]
      if sid == 0:
        data.append(('C' + str(r[6]), rid + 100, 0, 0, 1.0 - solved / float(rid), 0, 0, 0, 0))
      else:
        data.append(('C' + str(r[6]), rid + 100, total_time / float(sid), solution_length / float(sid), 1.0 - solved / float(rid),
                     graph_states / float(sid), graph_motions / float(sid), solution_smoothness / float(sid), solution_clearance / float(sid)))
    return OMPLTableData(description, data, "config")
