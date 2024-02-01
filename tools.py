import pydantic
from flask import request
from sqlalchemy.exc import IntegrityError

from error import HttpError
from models import Advertisment


def get_advertisment_by_id(advertisment_id):
    advert = request.session.get(Advertisment, advertisment_id)
    if advert is None:
        raise HttpError(404, "advertisment_not_found")
    return advert


def validate_json(class_schema, json_data):
    try:
        return class_schema(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise HttpError(404, error)


def add_advert(advert: Advertisment):
    try:
        request.session.add(advert)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Advertisment with this title already exists")