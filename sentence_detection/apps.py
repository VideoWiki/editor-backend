from django.apps import AppConfig

import spacy
import pysbd

class SentencedetectionConfig(AppConfig):
    name = 'sentence_detection'
    nlp = spacy.blank('en')
    nlp.add_pipe(pysbd.utils.PySBDFactory(nlp))