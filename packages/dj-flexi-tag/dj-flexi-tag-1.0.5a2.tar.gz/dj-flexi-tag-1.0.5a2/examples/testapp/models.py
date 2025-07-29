from django.db import models

from flexi_tag.utils.models import FlexiTagMixin


class TestModel(FlexiTagMixin):
    name = models.CharField(max_length=100)


class AnotherModel(FlexiTagMixin):
    title = models.CharField(max_length=200)
