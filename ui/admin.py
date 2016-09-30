from django.contrib import admin

# Register your models here.
from ui.models import *


class EntityAdmin(admin.ModelAdmin):
    list_display = ('text', 'categories', 'corpus')
    list_filter = ('corpus',)


class EntityAnnotationAdmin(admin.ModelAdmin):
    list_display = ('entity', 'annotator', 'category1_marked', 'category2_marked', 'unprocessed_sentences')
    list_filter = ('annotator', 'entity__corpus')


class SentenceAnnotationAdmin(admin.ModelAdmin):
    list_display = ('processed', 'time', 'entity', 'marked_category', 'annotator', 'sentence')
    list_filter = ('processed', 'marked_category', 'entity_annotation__annotator')

    def entity(self, obj):
        return obj.entity_annotation.entity.text

    def annotator(self, obj):
        return obj.entity_annotation.annotator


class CorpusAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')


class UserCorpusAdmin(admin.ModelAdmin):
    list_display = ('user', 'corpus')


admin.site.register(EntityAnnotation, EntityAnnotationAdmin)
admin.site.register(SentenceAnnotation, SentenceAnnotationAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(UserCorpus, UserCorpusAdmin)
admin.site.register(Sentence)

