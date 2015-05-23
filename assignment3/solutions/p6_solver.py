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
        
        for neighbor in csp.constraints[Xi]:
          X_k = neighbor.var2
          if X_k == Xi or X_k == Xj:
            continue
          else:
            queue_arcs.append( (X_k, Xi) )

    return True


def revise(csp, xi, xj):
    revised = False

    to_delete = []

    for val_i in xi.domain:
      found = False
      for const in csp.constraints[xi, xj]:
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

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    if is_complete(csp):
      return None

    min_var = None
    min_dom = 9999

    for var in csp.variables:

      if var.is_assigned():
        continue

      elif len(var.domain) < min_dom:
        min_var = var

    return min_var


def is_complete(csp):
  """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""  
  for var in csp.variables:
    if var.is_assigned() == False:
      return False
  return True


def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    for const in csp.constraints[variable]:
      print const

      var_neighbor = const.var2
      if var_neighbor.is_assigned() == False:
        continue
      else:
        if not const.is_satisfied(value, var_neighbor.value):
          print "NOT SATIS"
          return False

    print "SATISFIED"
    return True

    """
    for var2 in csp.variables:
      if not var2.is_assigned() or var2 == variable:
        continue
      else:
        for const in csp.constraints[variable, var2]:
          if not const.is_satisfied(value, var2.value):
            return False
    return True
    """

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

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


