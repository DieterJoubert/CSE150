# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'


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

      if var.is_assigned():
        continue

      if len( var.domain ) == min_domain:
        min_list.append(var)
      elif len( var.domain ) < min_domain:
        min_domain = len( var.domain )
        min_list = [var]

    if len(min_list) == 1:
      return min_list[0]

    max_count = 0
    max_var = None

    for var in min_list:

      count = 0

      for const in csp.constraints[var]:
        count += 1

      for var_other in csp.variables:
        if var_other.is_assigned() or var_other == var:
          continue
        else:
          for const in csp.constraints[var, var_other]:
            count += 1

      if count > max_count:
        max_count = count
        max_var = var

    return max_var


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


##HELPERS

def is_complete(csp):
  """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""  
  list_variables = csp.variables
  for var in list_variables:
    if var.is_assigned() == False:
      return False
  return True






