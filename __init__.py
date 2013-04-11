#This file is part ir_module_info module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from trytond.pool import Pool
from .module import *

def register():
    Pool.register(
        Module,
        module='ir_module_info', type_='model')
