# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import transaction

from ui.models import *

MAX_SENTENCES_PER_ENTITY = 10


class Command(BaseCommand):
    help = 'Drops user annotations'

    def add_arguments(self, parser):
        parser.add_argument('user-name')
        parser.add_argument('corpus-name')

    @transaction.atomic
    def handle(self, *args, **options):
        user = User.objects.get(username=options['user-name'])
        corpus = Corpus.objects.get(name=options['corpus-name'])
        UserCorpus.objects.filter(user=user, corpus=corpus).delete()
        EntityAnnotation.objects.filter(annotator_id=user, entity__corpus_id=corpus).delete()
        self.stdout.write(self.style.SUCCESS('Done!'))
