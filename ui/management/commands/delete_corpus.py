# -*- coding: utf-8 -*-
import random

from django.core.management.base import BaseCommand

from ui.models import *


class Command(BaseCommand):
    help = 'Deletes corpus and all annotations'

    def add_arguments(self, parser):
        parser.add_argument('corpus-id')

    def handle(self, *args, **options):
        Corpus.objects.filter(pk=options['corpus-id']).delete()
        self.stdout.write(self.style.SUCCESS('Done!'))
