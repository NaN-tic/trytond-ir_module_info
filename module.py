#This file is part ir_module_info module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.modules import get_module_info
import os

__all__ = ['Module']
__metaclass__ = PoolMeta


class Module:
    __name__ = "ir.module.module"
    description = fields.Function(fields.Text("Description"), 'get_description')

    @staticmethod
    def read_rst(doc_path):
        f = open(doc_path, "r")
        return f.read()

    def get_description(self, name):
        Config = Pool().get('ir.configuration')

        description = ''

        lang = self._context.get('language') or Config.get_language()
        lang = lang[:2]

        #if catalan language, use spanish language
        if lang == 'ca':
            lang = 'es'

        module = get_module_info(self.name)
        path = module['directory']

        doc_path = '%s/doc/%s/index.rst' % (path, lang)
        if os.path.exists(doc_path):
            return self.read_rst(doc_path)

        doc_path = '%s/doc/index.rst' % (path)
        if os.path.exists(doc_path):
            return self.read_rst(doc_path)

        return description
