# coding: utf-8

from mongoengine.document import Document
from mongoengine.fields import (
    StringField, ListField, IntField, DateTimeField,
    PointField, EmbeddedDocumentField, EmbeddedDocument
)


class Image(EmbeddedDocument):
    path = StringField(required=True)


class Pet(Document):
    images = ListField(EmbeddedDocumentField(Image))
    position = PointField(required=True)
    created_at = DateTimeField(required=True)
    # manual input
    breed_by_user = StringField(required=True)
    # provided by owner
    user_description = StringField()
    # owner's phone number
    phone_number = StringField()

    def __unicode__(self):
        return u'{0}'.format(self.id)
