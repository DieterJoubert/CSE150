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

def is_complete(csp):
  """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""  
  list_variables = csp.variables
  for var in list_variables:
    if var.is_assigned() == False:
      return False
  return True






