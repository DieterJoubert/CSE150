# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'


def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """  
    import Queue
    q = Queue.PriorityQueue()

    for value in variable.domain:
      count = 0
      for const in csp.constraints[variable]:
        if const.var2.is_assigned() == False and value in const.var2.domain:
          count += 1
      q.put(  (count, value  ))

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


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
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

    else:
      var = select_unassigned_variable(csp)
      for value in order_domain_values(csp, var):

        csp.variables.begin_transaction()

        if is_consistent(csp, var, value):
          var.assign(value)

          if backtrack(csp) == True:
            return True

        csp.variables.rollback()

    return False

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

