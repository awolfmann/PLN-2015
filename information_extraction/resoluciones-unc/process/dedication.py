# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

# from iepy.preprocess.ner.regexp import RegExpNERRunner
from process.regexp_ner import (RegExpNERRunner, options_re, optional_re, 
    tokenized_re)

class DedicationNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        dedications = ['dedicaci6n simple', 'DS']
        regexp = options_re(dedications)
        super(DedicationNERRunner, self).__init__('dedication', regexp, override)
