# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'


def is_complete(csp):
  """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""  
  list_variables = csp.variables
  for var in list_variables:
    if var.is_assigned() == False:
      return False
  return True


    # Hint: The list of all variables for the CSP can be obtained by csp.variables.
    # Also, if the variable is assigned, variable.is assigned() will be True.
    # (Note that this can happen either by explicit assignment using variable.assign(value),
    # or when the domain of the variable has been reduced to a single value.)

