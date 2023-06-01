from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Поле обязательно'),
                    URL(message='Ссылка неккоректна')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16), Optional(), Regexp(r'^[A-Za-z0-9]*$')]
    )
    submit = SubmitField('Создать')
