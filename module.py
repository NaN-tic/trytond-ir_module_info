#This file is part ir_module_info module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.modules import get_module_info
import os
import re
try:
    import docutils.core
    has_docutils = True
except ImportError:
    has_docutils = False

__all__ = ['Module']
__metaclass__ = PoolMeta


class Module:
    __name__ = "ir.module.module"
    description = fields.Function(fields.Text("Description"), 'get_description')
    models = fields.Function(fields.One2Many('ir.model', None, 'Models'),
                'get_models')
    fields = fields.Function(fields.One2Many('ir.model.field', None, 'Fields'),
                'get_fields')

    @staticmethod
    def read_rst(doc_path):
        f = open(doc_path, "r")
        description = f.read()

        def rst2html(source, source_path=None, source_class=docutils.io.StringInput,
                     destination_path=None, reader=None, reader_name='standalone',
                     parser=None, parser_name='restructuredtext', writer=None,
                     writer_name='html', settings=None, settings_spec=None,
                     settings_overrides=None, config_section=None,
                     enable_exit_status=None):
            """
            Set up & run a `Publisher`, and return a dictionary of document parts.
            Dictionary keys are the names of parts, and values are Unicode strings;
            encoding is up to the client. For programmatic use with string I/O.

            For encoded string input, be sure to set the 'input_encoding' setting to
            the desired encoding. Set it to 'unicode' for unencoded Unicode string
            input. Here's how::

            publish_parts(..., settings_overrides={'input_encoding': 'unicode'})

            Parameters: see `publish_programmatically`.
            """
            output, pub = docutils.core.publish_programmatically(
                source=source, source_path=source_path, source_class=source_class,
                destination_class=docutils.io.StringOutput,
                destination=None, destination_path=destination_path,
                reader=reader, reader_name=reader_name,
                parser=parser, parser_name=parser_name,
                writer=writer, writer_name=writer_name,
                settings=settings, settings_spec=settings_spec,
                settings_overrides=settings_overrides,
                config_section=config_section,
                enable_exit_status=enable_exit_status)
            return pub.writer.parts['fragment'], pub.document.reporter.max_level, pub.settings.record_dependencies

        def remove_tags(text):
            TAG_RE = re.compile(r'<[^>]+>')
            return TAG_RE.sub('', text)

        if has_docutils:
            output, error_level, deps = rst2html(
                    description, settings_overrides={
                        'initial_header_level': 2,
                        'record_dependencies': True,
                        'stylesheet_path': None,
                        'link_stylesheet': True,
                        'syntax_highlight': 'short',
                    })
            return remove_tags(output)
        else:
            return description

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

    def get_models(self, name):
        if not self.state == 'installed':
            return
        Model = Pool().get('ir.model')
        return [x.id for x in Model.search([('module', '=', self.name)])]


    def get_fields(self, name):
        if not self.state == 'installed':
            return
        Field = Pool().get('ir.model.field')
        return [x.id for x in Field.search([('module', '=', self.name)])]
