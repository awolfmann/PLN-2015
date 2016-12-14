from iepy.preprocess.pipeline import BasePreProcessStepRunner
from iepy.data.models import EntityKind


class ClearEntities(BasePreProcessStepRunner):

    def __init__(self, kind_name):
        self.kind = EntityKind.objects.get(name=kind_name)

    def __call__(self, doc):
        doc.entity_occurrences.filter(entity__kind=self.kind).delete()