# -*- coding: utf-8 -*-
import re

from django.core.exceptions import ObjectDoesNotExist

from apostello.exceptions import ArchivedItemException

gsm_regex = re.compile(
    r'^[\w@?£!1$"¥#è?¤é%ù&ì\\ò(Ç)*:Ø+;ÄäøÆ,<LÖlöæ\-=ÑñÅß.>ÜüåÉ/§à¡¿\']+$'
)
non_gsm_regex = re.compile(
    r'[^\w@?£!1$"¥#è?¤é%ù&ì\\ò(Ç)*:Ø+;ÄäøÆ,<LÖlöæ\-=ÑñÅß.>ÜüåÉ/§à¡¿\'\s]'
)


def exists_and_archived(form, model_class, identifier):
    """
    Check if a user tries to create an object is now archived.

    Works for Groups, Recipients and Keywords.
    Returns the instance of the existing Person (etc) for editing if it exists,
    otherwise returns None.
    """
    unique_fields = {
        'keyword': 'keyword',
        'group': 'name',
        'recipient': 'number'
    }

    all_errors = [
        form.errors.as_data()[x][0].code for x in form.errors.as_data()
    ]
    try:
        instance = model_class.objects.get(
            **{
                unique_fields[identifier]: form.data[unique_fields[identifier]]
            }
        )
    except ObjectDoesNotExist:
        raise ArchivedItemException

    if ('unique' in all_errors) and instance.is_archived:
        return instance
    else:
        raise ArchivedItemException


def fetch_default_reply(msg=''):
    """Fetch default reply from database."""
    from site_config.models import DefaultResponses
    replies = DefaultResponses.get_solo().__dict__
    return replies[msg]
