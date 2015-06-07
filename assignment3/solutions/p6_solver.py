# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

from collections import deque

def inference(csp, variable):
    """Performs an inference procedure for the variable assignment. """
    return ac3(csp, csp.constraints[variable].arcs())

def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None

def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    #if all variables assigned, must have passed inconsistency check, found solution    
    if is_complete(csp):
      return True

    var = select_unassigned_variable(csp)

    for value in order_domain_values(csp, var):

      #will assign this value to the var create inconsistency?
      if is_consistent(csp, var, value):

        #about to assign, save CSP configuration
        csp.variables.begin_transaction()
        var.assign(value)

        #check if AC3 finds any violations
        var_inference = inference(csp, var)
        if var_inference != False:
          result = backtrack(csp)
          if result != False:
            return result

        #if false return, rollback to before assignment, try next value
        csp.variables.rollback()

    #no result found, return false
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

    #run as long as deque is not empty
    while queue_arcs:
      (Xi, Xj) = queue_arcs.pop()

      #use revise to reduce domains
      if revise(csp, Xi, Xj):

        #if revision resulted in a variable with no domain, error, return false
        if Xi.domain is None or len(Xi.domain) == 0:
          return False
        
        #add all neighboring arcs (without Xj) flipped
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

    #check each constraint that involves xi and xj
    for const in csp.constraints[xi, xj]:

      #iterate through each val in xi's domain
      for val_i in xi.domain:
        found = False

        #iterate through each val in xj's domain
        for val_j in xj.domain:
          if const.is_satisfied(val_i, val_j):
            #found const that is satisfied by this val, will not delete it
            found = True

        #not able to satisfy this constraint with value, delete it
        if found == False:
          to_delete.append(val_i)
          #domain will be changed, set revised to true
          revised = True

    #remove all values from xi's domain that can't satisfy
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

    min_domain = 99999999999
    min_list = []

    for var in csp.variables:

      #if already assigned, pass over it
      if var.is_assigned():
        continue

      #if just as long as shortest we've found, add to our list of shortest
      if len( var.domain ) == min_domain:
        min_list.append(var)
      #if shorter than shortest found, create new list with just this new one, save min domain
      elif len( var.domain ) < min_domain:
        min_domain = len( var.domain )
        min_list = [var]

    #if only one variable in final list, return it, otherwise tie-break
    if len(min_list) == 1:
      return min_list[0]

    max_count = 0
    max_var = None

    #tie-break between list of variables with all the same min domain size
    for var in min_list:

      count = 0

      #check how many constraints on unassigned variables this var is involved with
      for const in csp.constraints[var]:
        if const.var2.is_assigned():
          continue
        else:
          count += 1

      #check if variable is found that is involved in more constraints than best so far
      if count > max_count:
        max_count = count
        max_var = var

    return max_var

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

      var_neighbor = const.var2
      if var_neighbor.is_assigned() == False:
        continue
      else:
        if not const.is_satisfied(value, var_neighbor.value):
          return False

    return True

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """  
    #keep queue of values with priority being the LCV
    import Queue
    q = Queue.PriorityQueue()

    for value in variable.domain:
      count = 0

      for const in csp.constraints[variable]:

        #if other value in constraint is not assigned
        if const.var2.is_assigned() == False:

          for val2 in const.var2.domain:
            if const.is_satisfied(value, val2):
              continue
            else:
              #if not satisfied, rules out a value, count++
              count += 1

      q.put( (count, value) )

    result = []
    #depopulate queue into result to return list ordered by LCV
    while not q.empty():
      (priority, value) = q.get()
      result.append(value)

    return result