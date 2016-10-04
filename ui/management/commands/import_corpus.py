# -*- coding: utf-8 -*-
import os
import json
import random
import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from ui.models import *


class Command(BaseCommand):
    help = 'Loads corpus from csv fle'

    def add_arguments(self, parser):
        parser.add_argument('corpus-name')
        parser.add_argument('corpus-file')

    @transaction.atomic
    def handle(self, *args, **options):
        corpus_name = options['corpus-name']
        corpus_file = options['corpus-file']

        snt_order = list(range(1000000))
        random.shuffle(snt_order)

        corpus = Corpus.objects.create(name=corpus_name)

        with open(corpus_file, encoding='utf-8') as inf:
            reader = csv.DictReader(inf)
            prew_entity = None
            for i, row in enumerate(reader):
                if prew_entity is not None and prew_entity.text == row["entity"]:
                    entity = prew_entity
                else:
                    entity = Entity.objects.create(corpus=corpus, text=row["entity"],
                                                   categories=[row["category1"], row["category2"]])

                Sentence.objects.create(entity=entity,
                                        entity_start=row["entity_start"],
                                        entity_end=row["entity_end"],
                                        text=row["sentence"],
                                        order=snt_order.pop())
                prew_entity = entity

                if i % 1000 == 0:
                    self.stdout.write('{} rows imported'.format(i))

            self.stdout.write('{} rows imported'.format(i))

        self.stdout.write(self.style.SUCCESS('Done!'))
