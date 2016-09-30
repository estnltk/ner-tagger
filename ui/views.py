import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.db.models import F
from django.template import RequestContext

from ui.models import Corpus, Entity, Sentence, SentenceAnnotation, EntityAnnotation

SENTENCE_BATCH_SIZE = 5


@login_required
def corpus_list_view(request):
    corpus_list = []
    for corpus in Corpus.objects.all():
        if EntityAnnotation.objects.filter(annotator=request.user, entity__corpus=corpus).count() == 0:
            continue
        corpus_list.append(corpus)
        corpus.entity_count = EntityAnnotation.objects.filter(annotator=request.user, entity__corpus=corpus).count()
        corpus.unprocessed_entity_count = EntityAnnotation.objects \
            .filter(annotator=request.user, entity__corpus=corpus, unprocessed_sentences__gt=0) \
            .exclude(category1_marked=True, category2_marked=True).count()
        corpus.sentence_count = Sentence.objects.filter(entity__corpus=corpus).count()
        corpus.unprocessed_sentence_count = SentenceAnnotation.objects \
            .filter(entity_annotation__annotator=request.user, entity_annotation__entity__corpus=corpus,
                    processed=False) \
            .exclude(entity_annotation__category1_marked=True, entity_annotation__category2_marked=True).count()
    return render_to_response('corpus.html', RequestContext(request, {'corpus_list': corpus_list, 'page': 'corpus'}))


@login_required
def load_sentences_view(request):
    """
    Sample response:
    [{
            "id": 1,
            "text": 'Tallinn on Eesti pealinn .",
            "entity_id": 1,
            "entity_text": "Tallinn",
            "entity_categories": ['LOC', 'O'],
            "entity_start": 0,
            "entity_end": 7
    },
    ...
    ]
    """
    corpus_id = request.POST['corpus_id']
    annotations = SentenceAnnotation.objects \
                      .filter(processed=False, entity_annotation__entity__corpus_id=corpus_id,
                              entity_annotation__annotator=request.user) \
                      .exclude(entity_annotation__category1_marked=True, entity_annotation__category2_marked=True) \
                      .exclude(entity_annotation__unprocessed_sentences=0) \
                      .select_related('entity_annotation', 'sentence', 'entity_annotation__entity') \
                      .order_by('sentence__order')[:SENTENCE_BATCH_SIZE]
    return render(request, 'sentences.html', {'sentence_annotations': annotations},
                  content_type='application/json; charset=utf-8')


@login_required
def submit_sentences_view(request):
    """
    Request should contain sentence annotations in json format:
    [
        {
            "id": 1,
            "entity_annotation_id": 34,
            "time": 10,
            "marked_category": "LOC",    // optional
            "entity_categories: ["LOC", "PER"],
            "corpus_id": 35
        },
        ...
    ]

    Response contains the next portion of sentencess to process.
    """
    sentences = json.loads(request.body.decode('utf-8'))
    for snt in sentences:
        sa = SentenceAnnotation(id=snt['id'],
                                processed=True,
                                time=snt['time'],
                                marked_category=snt.get('marked_category'))
        sa.save(force_update=True, update_fields=['processed', 'time', 'marked_category'])
        ea = EntityAnnotation(id=snt['entity_annotation_id'], unprocessed_sentences=F('unprocessed_sentences') - 1, )
        update_fields = ['unprocessed_sentences']
        if "marked_category" in snt:
            if snt["marked_category"] == snt["entity_categories"][0]:
                ea.category1_marked = True
                update_fields.append('category1_marked')
            elif snt["marked_category"] == snt["entity_categories"][1]:
                ea.category2_marked = True
                update_fields.append('category2_marked')
        ea.save(force_update=True, update_fields=update_fields)

    request.POST = request.POST.copy()
    request.POST['corpus_id'] = int(sentences[0]["corpus_id"])
    return load_sentences_view(request)
