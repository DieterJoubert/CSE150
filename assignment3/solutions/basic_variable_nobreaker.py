# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

def select_unassigned_variable(csp):
    if is_complete(csp):
      return None

    min_domain = 99999999999
    min_var = None

    for var in csp.variables:

      if var.is_assigned():
        continue

      if len( var.domain ) < min_domain:
        min_domain = len( var.domain )
        min_var = var

    return min_var

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


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



















