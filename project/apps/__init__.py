# coding: utf-8

from apps import settings
from apps.public.text import PoFilter


terms = getattr(settings, 'TERMS_TEXT', [])

pof = PoFilter()
pof.init(terms)

screen_replace = pof.replace

