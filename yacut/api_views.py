import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error import InvalidAPIUsage
from .get_short import get_unique_short_id
from .models import URLMap
from settings import REGEXP_SAMPLE

LIMIT = 16


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        # Выбрасываем собственное исключение.
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        # Выбрасываем собственное исключение
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if short_id:
        if len(short_id) >= LIMIT or not re.match(REGEXP_SAMPLE, short_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    else:
        short_id = get_unique_short_id()
    url = URLMap(
        original=data.get('url'),
        short=short_id
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    original_url = URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original_url.original}), HTTPStatus.OK
