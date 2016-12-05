# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

# from iepy.preprocess.ner.regexp import RegExpNERRunner
from process.regexp_ner import (RegExpNERRunner, options_re, optional_re, 
    tokenized_re)


class DesignationNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        designations = ['Deslgnar', 'Aceptar', 'Prorrogar', 'designaci6n', 'Otorgar', 'Designar']
        designations_p = ['designaciones', ]
        regexp = options_re(designations+designations_p)
        super(DesignationNERRunner, self).__init__('designation', regexp, override)
