from flask import request, jsonify

from app import get_app
from error import HttpError
from models import Session
from views import AdvertView

app = get_app()


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response

advertisment_view = AdvertView.as_view("post_view")
app.add_url_rule("/advertisment/", view_func=advertisment_view, methods=["POST"])
app.add_url_rule("/advertisment/<int:advertisment_id>/", view_func=advertisment_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run()