# -*- coding: utf-8 -*-
__author__ = 'Please write your names, separated by commas.'
__email__ = 'Please write your email addresses, separated by commas.'

from collections import deque

def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())

def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """
    if is_complete(csp):
      return True

    var = select_unassigned_variable(csp)

    for value in order_domain_values(csp, var):
      if is_consistent(csp, var, value):

        csp.variables.begin_transaction()

        var.assign(value)

        var_inference = inference(csp, var)
        if var_inference != False:
          result = backtrack(csp)
          if result != False:
            return result

        csp.variables.rollback()

    return False


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise.  Note that this method does not
    return any additional variable assignments (for simplicity)."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    while queue_arcs:
      (Xi, Xj) = queue_arcs.pop()
      if revise(csp, Xi, Xj):
        if Xi.domain is None or len(Xi.domain) == 0:
          return False
        
        for (a, b) in csp.constraints[Xi].arcs():
          if b == Xi or b == Xj:
            continue
          else:
            queue_arcs.append( (b, a) )

    return True



def revise(csp, xi, xj):
    revised = False

    to_delete = []

    for const in csp.constraints[xi, xj]:

      found = False

      for val_i in xi.domain:
        for val_j in xj.domain:
          if const.is_satisfied(val_i, val_j):
            found = True

      if found == False:
        to_delete.append(val_i)
        revised = True

    import copy
    domain_new = copy.deepcopy(xi.domain)
    for val in to_delete:
      if val in domain_new:
        domain_new.remove(val)

    xi.domain = copy.deepcopy(domain_new)

    return revised


def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def is_complete(csp):
  """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""  
  for var in csp.variables:
    if var.is_assigned() == False:
      return False
  return True


def is_consistent(csp, variable, value):
    for const in csp.constraints[variable]:

      var_neighbor = const.var2
      if var_neighbor.is_assigned() == False:
        continue
      else:
        if not const.is_satisfied(value, var_neighbor.value):
          return False

    return True


def order_domain_values(csp, variable):
    import Queue
    q = Queue.PriorityQueue()

    for value in variable.domain:
      neigh_choices = neighbor_choices(csp, variable) 

      csp.variables.begin_transaction()

      variable.assign(value)
      
      neigh_choices_star = neighbor_choices(csp, variable) 
      q.put( (neigh_choices - neigh_choices_star, value)  )

      csp.variables.rollback()

    result = []

    while not q.empty():
      (priority, value) = q.get()
      result.append(value)

    return result



def neighbor_choices(csp, var):      
  choices = 0
  for value in var.domain:
    for var_other in csp.variables:
      if var_other.is_assigned() or var_other == var:
        continue
      else:
        for const in csp.constraints[var, var_other]:
          for val_other in var_other.domain:

            if const.is_satisfied(value, val_other):
              choices += 1
  return choices


