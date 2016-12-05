# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

# from iepy.preprocess.ner.regexp import RegExpNERRunner
from process.regexp_ner import (RegExpNERRunner, options_re, optional_re, 
    tokenized_re)


class DesignationTypeNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        temporaries = ['interinas', 'interina', 'interinamente', 'interi`no']
        contests = ['concurso']
        resignations = ['renuncia']
        expirations = ['cesan', 'cese']
        leave = ['licencia']
        regexp = options_re(temporaries+contests+resignations+expirations+leave)
        super(DesignationTypeNERRunner, self).__init__('designation_type', regexp, override)
