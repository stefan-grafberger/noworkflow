# Copyright (c) 2014 Universidade Federal Fluminense (UFF), Polytechnic Institute of New York University.
# This file is part of noWorkflow. Please, consult the license terms in the LICENSE file.

from __future__ import absolute_import

import sys
import ast
from datetime import datetime

import persistence
from utils import print_msg
from .function_visitor import FunctionVisitor
from .slicing_visitor import SlicingVisitor



def visit_ast(metascript):
    '''returns a visitor that visited the tree and filled the attributes:
        functions: map of function in the form: name -> (arguments, global_vars, calls, code_hash)
        name_refs[path]: map of identifiers in categories Load, Store
        dependencies[path]: map of dependencies
    '''
    tree = ast.parse(metascript['code'], metascript['path'])
    visitor = SlicingVisitor(metascript)
    visitor.result = visitor.visit(tree)
    visitor.extract_disasm()
    visitor.teardown()
    return visitor


def collect_provenance(args, metascript):
    now = datetime.now()
    try:
        persistence.store_trial(now, sys.argv[0], metascript['code'], ' '.join(sys.argv[1:]), args.bypass_modules)
    except TypeError:
        print_msg('not able to bypass modules check because no previous trial was found', True)
        print_msg('aborting execution', True)
        sys.exit(1)

    print_msg('  registering user-defined functions')
    visitor = visit_ast(metascript)
    persistence.store_function_defs(visitor.functions)
    if args.disasm:
        print('\n'.join(visitor.disasm))
    metascript['definition'] = visitor