from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Corpus(models.Model):
    name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Entity(models.Model):
    text = models.TextField()
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, db_index=True)
    categories = ArrayField(models.TextField())

    def __str__(self):
        return self.text


class UserCorpus(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
   
   class Meta:
       unique_together = ('user', 'corpus')


class Sentence(models.Model):
    text = models.TextField()
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, db_index=True)
    entity_start = models.IntegerField()
    entity_end = models.IntegerField()
    order = models.IntegerField(db_index=True)

    def __str__(self):
        return self.text


class EntityAnnotation(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, db_index=True)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    category1_marked = models.BooleanField(default=False)
    category2_marked = models.BooleanField(default=False)
    unprocessed_sentences = models.IntegerField()

    def __str__(self):
        return '{}: {} - {}'.format(self.entity.text, self.annotator.username, self.unprocessed_sentences)


class SentenceAnnotation(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, db_index=True)
    entity_annotation = models.ForeignKey(EntityAnnotation, on_delete=models.CASCADE, db_index=True)
    processed = models.BooleanField(default=False, db_index=True)
    time = models.IntegerField(null=True)
    marked_category = models.TextField(null=True)
