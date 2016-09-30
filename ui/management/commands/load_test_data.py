# -*- coding: utf-8 -*-
import random

from django.core.management.base import BaseCommand

from ui.models import *


class Command(BaseCommand):
    help = 'Loads initial data for testing'

    def handle(self, *args, **options):
        Corpus.objects.all().delete()
        Entity.objects.all().delete()
        Sentence.objects.all().delete()
        User.objects.filter().delete()

        User.objects.create_superuser(username='distorti', email='distorti@ut.ee', password='distortion1')
        User.objects.create_user(username='sven', email='sven@ut.ee', password='sven.laur')

        Corpus.objects.create(pk=1, name='Test korpus')

        Entity.objects.create(pk=1, text='kallas', corpus_id=1, categories=['PER', 'O'])

        Sentence.objects.create(entity_id=1, entity_start=18, entity_end=24, text="Toimetaja : Riina Kallas")
        Sentence.objects.create(entity_id=1, entity_start=0, entity_end=6,
                                text="Kallas ütles BNS-ile , et rahandusministeeriumi arvutuste kohaselt kuluks täiendavate toimetulekutoetuste peale 17 miljonit krooni .")
        Sentence.objects.create(entity_id=1, entity_start=48, entity_end=55,
                                text="Arco Vara Kinnisvara Saare büroo juhataja Veiko Kallase hinnangul ei ole kevad Kuressaare kinnisvaraturgu märgatavalt elavdanud .")
        Sentence.objects.create(entity_id=1, entity_start=0, entity_end=7,
                                text="Kallase sõnul said paari aasta taguse kinnisvarabuumi ajal ka saarlased eluasemelaenu , praegu on see väikeste palkade tõttu peaaegu võimatu")
        Sentence.objects.create(entity_id=1, entity_start=6, entity_end=12,
                                text="Järve kaldal oli külm .")

        Entity.objects.create(pk=2, text='savisaar', corpus_id=1, categories=['PER', 'LOC'])

        Sentence.objects.create(entity_id=2, entity_start=0, entity_end=8, text="Savisaar ütles, et kõik on ok .")
        Sentence.objects.create(entity_id=2, entity_start=6, entity_end=14, text="Külas Savisaar on hea ilm.")
        Sentence.objects.create(entity_id=2, entity_start=6, entity_end=14, text="Edgar Savisaar on tore .")

        user_ids = User.objects.all().values_list('id', flat=True)
        entity_ids = Entity.objects.all().values_list('id', flat=True)
        order = list(range(Sentence.objects.count()))
        random.shuffle(order)
        for uid in user_ids:
            user_order = order[:]
            for entity_id in entity_ids:
                snts = Sentence.objects.filter(entity_id=entity_id).values_list('id', flat=True)
                ea = EntityAnnotation.objects.create(annotator_id=uid, entity_id=entity_id,
                                                     unprocessed_sentences=len(snts))
                for snt in snts:
                    SentenceAnnotation.objects.create(sentence_id=snt, entity_annotation_id=ea.id,
                                                      order=user_order.pop())

        self.stdout.write(self.style.SUCCESS('Done!'))
