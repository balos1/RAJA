#!/usr/bin/env python
#
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# All rights reserved.
#
# This source code cannot be distributed without permission and
# further review from Lawrence Livermore National Laboratory.
#


import sys
from itertools import permutations
from lperm import *
 

def writeView(ndims_list):

  for ndims in ndims_list:
    dim_names = getDimNames(ndims)
  
    # Open struct definition
    print "template<typename DataType, typename Layout>"
    print "struct View%dd {" % ndims
    
    # Create some typedef's to describe the template parameters
    print "  typedef typename Layout::Permutation Permutation;"
    for a in dim_names:
      print "  typedef typename Layout::Index%s Index%s;" % (a.upper(), a.upper())
    print ""
    
    # Add local variables
    print "  Layout const layout;"
    print "  DataType *data;"
    print ""
        
    # Define constructor
    args = map(lambda a: "Index_type n"+a, dim_names)
    argstr = ", ".join(args)
    print "  inline View%dd(DataType *data_ptr, %s):" % (ndims, argstr)
    args = map(lambda a: "n"+a, dim_names)
    argstr = ", ".join(args)
    print "    layout(%s)," % argstr
    print "    data(data_ptr)"
    print "  {}"
    print ""
    
    # Define () Operator (const)
    args = map(lambda a: "Index%s %s"%(a.upper(), a), dim_names)
    argstr = ", ".join(args)
    print "  inline DataType &operator()(%s) const {" % argstr
    argstr = ", ".join(dim_names)
    print "    return data[convertIndex<Index_type>(layout(%s))];" % argstr
    print "  }"
        
    print "};"
    print ""


def writeViewImpl(ndims_list):

  for ndims in ndims_list:
    dim_names = getDimNames(ndims)
    
    print ""
    print "/******************************************************************"
    print " *  Implementation for View%dD" % ndims
    print " ******************************************************************/"
    print ""
                
    # Define constructor
    args = map(lambda a: "Index_type n"+a, dim_names)
    argstr = ", ".join(args)    
    print "  template<typename T, typename L>"
    print "  inline View%dd<T,L>::View%dd(T *data_ptr, %s):" % (ndims, ndims, argstr)    
    args = map(lambda a: "n"+a, dim_names)
    argstr = ", ".join(args)
    print "    layout(%s)," % argstr
    print "    data(data_ptr)"
    print "  {"
    print "  }"
    print ""

    # Define () Operator (const)
    args = map(lambda a: "Index_type "+a, dim_names)
    argstr = ", ".join(args)      
    print "  template<typename T, typename L>"
    print "  inline T &View%dd<T,L>::operator()(%s) const {" % (ndims, argstr)
    argstr = ", ".join(dim_names)
    print "    return(data[layout(%s)]);" % argstr
    print "  }"
    print ""
               
  
 


# ACTUAL SCRIPT ENTRY:
print """//AUTOGENERATED BY genView.py
/*
 * Copyright (c) 2016, Lawrence Livermore National Security, LLC.
 * Produced at the Lawrence Livermore National Laboratory.
 *
 * All rights reserved.
 *
 * This source code cannot be distributed without permission and
 * further review from Lawrence Livermore National Laboratory.
 */
  
#ifndef RAJA_VIEW_HXX__
#define RAJA_VIEW_HXX__

#include <RAJA/Layout.hxx>

namespace RAJA {
"""

ndims_list = range(1,5+1)

# Dump all declarations (with documentation, etc)
writeView(ndims_list)


print """

} // namespace RAJA

#endif
"""

