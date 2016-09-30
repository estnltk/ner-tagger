# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import transaction

from ui.models import *

MAX_SENTENCES_PER_ENTITY = 10


class Command(BaseCommand):
    help = 'Assigns a corpus to a user'

    def add_arguments(self, parser):
        parser.add_argument('user-name')
        parser.add_argument('corpus-name')

    @transaction.atomic
    def handle(self, *args, **options):
        user = User.objects.get(username=options['user-name'])
        corpus = Corpus.objects.get(name=options['corpus-name'])
        UserCorpus.objects.create(user=user, corpus=corpus)
        entity_ids = Entity.objects.filter(corpus=corpus).values_list('id', flat=True)
        snts_count, snts_total = 0, Sentence.objects.filter(entity__corpus=corpus).count()
        for entity_id in entity_ids:
            snt_ids = Sentence.objects.filter(entity_id=entity_id).values_list('id', flat=True)
            ea = EntityAnnotation.objects.create(annotator=user, entity_id=entity_id,
                                                 unprocessed_sentences=min(MAX_SENTENCES_PER_ENTITY, len(snt_ids)))
            for snt_id in snt_ids:
                SentenceAnnotation.objects.create(sentence_id=snt_id, entity_annotation_id=ea.id)
                snts_count += 1

            if snts_count % 100 == 0 or snts_count == snts_total:
                self.prnt('processed {} / {} sentences'.format(snts_count, snts_total))

        self.prnt(self.style.SUCCESS('Done!'))


    def prnt(self, msg):
        self.stdout.write(msg)
