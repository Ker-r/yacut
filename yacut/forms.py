from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import REGEXP_SAMPLE


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Поле обязательно'),
                    URL(message='Ссылка неккоректна')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16), Optional(), Regexp(REGEXP_SAMPLE)]
    )
    submit = SubmitField('Создать')
