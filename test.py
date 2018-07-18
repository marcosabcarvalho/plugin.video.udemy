#!/usr/bin/env python2.7
import os
import sys
sys.path.append(os.path.realpath('../script.module.matthuisman/lib'))

from matthuisman.test import run_test
from resources.lib.controller import Controller

ROUTES = [
    #'',
    '?_route=home',
    #'?_route=login',
    #'?_route=my_courses',
    #'?_route=course&id=1647296',
    '?_route=play&id=12333336',
   # '?_route=play&id=13435466',
    #'?_route=logout'
]

run_test(Controller, ROUTES)