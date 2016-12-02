# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

from iepy.preprocess.ner.regexp import RegExpNERRunner

def options_re(options):
    options2 = []
    for o in options:
        options2.append(tokenized_re(o))
    result = '(' + ' | '.join(options2) + ')'
    return result

def optional_re(option):
    result = '(' + option + ')?'
    return result

def tokenized_re(s):
    return '<' + '> <'.join(s.split()) + '>'

class  PositionNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        positions = ['Ayudante A', 'Ayudante B',
                    'Asistente', 'Adjunto', 'Asociado',
                    'Titular']
        positions_p = ['Ayudantes A', 'Ayudantes B',
                    'Asistentes', 'Adjuntos', 'Asociados',
                    'Titulares']
        position = options_re(positions+positions_p)
        regexp = "<Profesor|Profesores|Prof|Profs>" + optional_re("<,>") + optional_re("<.>") + position
        super(PositionNERRunner, self).__init__('position', regexp, override)
