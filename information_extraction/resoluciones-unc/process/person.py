# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

from process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class PersonNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        # surname_re = upperletters_re('surname')
        # surname_re = u'(?P<<surname>><[A-ZÁÉÍÓÚÑ]*>)'
        # surnames_re = u'(?P<<surname>><{}*\s{}*>)'.format(upperletter, upperletter)
        surname = upperletters_re() + optional_re(' ' + upperletters_re()) 
        # name_re = lowerletters_re('name')
        # name_re = u'(?P<<name>><[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>)'
        name = capitalizedletters_re() + optional_re(' ' + capitalizedletters_re()) 
        regexp = surname + tokenized_re('<,>') + name

        super(PersonNERRunner, self).__init__('person', regexp, override)

    def process_match(self, match):
        #surname = ' '.join(match.group('surname'))
        name = ' '.join(match.group('name'))
        #complete_name = name + ' ' + surname
        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(name, kind, name, offset, offset_end)

        return entity_oc
