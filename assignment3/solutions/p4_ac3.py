# -*- coding: utf-8 -*-
__author__ = "Dieter Joubert, Joseph Luttrell, Spenser Cornett"
__email__ = 'djoubert@ucsd.edu,jluttrell@ucsd.edu,scornett@ucsd.edu'

from collections import deque
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