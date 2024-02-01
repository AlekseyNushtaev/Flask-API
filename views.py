from flask import request, jsonify
from flask.views import MethodView
from unicodedata import normalize

from models import Session, Advertisment
from schema import CreateAdvert, UpdateAdvert
from tools import get_advertisment_by_id, validate_json, add_advert


class AdvertView(MethodView):

    @property
    def session(self) -> Session:
        return request.session


    def get(self, advertisment_id):
        advert = get_advertisment_by_id(advertisment_id)
        return jsonify(advert.dict)

    def post(self):
        json_data = validate_json(CreateAdvert, request.json)
        advert = Advertisment(**json_data)
        add_advert(advert)
        response = jsonify(advert.dict)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


    def patch(self, advertisment_id):
        json_data = validate_json(UpdateAdvert, request.json)
        advert = get_advertisment_by_id(advertisment_id)
        for field, value in json_data.items():
            setattr(advert, field, value)
        add_advert(advert)
        return jsonify(advert.dict)


    def delete(self, advertisment_id):
        advert = get_advertisment_by_id(advertisment_id)
        self.session.delete(advert)
        self.session.commit()
        return jsonify({"status": "delete"})