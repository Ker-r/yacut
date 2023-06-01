from flask import flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .get_short import get_unique_short_id
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    # Если ошибок не возникло, то
    if form.validate_on_submit():
        short_id = form.custom_id.data
        # Если в БД уже есть ссылка, которую ввёл пользователь,
        if URLMap.query.filter_by(short=short_id).first():
             # вызвать функцию flash и передать соответствующее сообщение
            flash(f'Имя {short_id} уже занято!')
            # и вернуть пользователя на главную страницу
            return render_template('yacut.html', form=form)
        if short_id is None or short_id == '':
            short_id = get_unique_short_id()
        # нужно создать новый экземпляр класса URLMap
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        # Затем добавить его в сессию работы с базой данных
        db.session.add(url_map)
        # И зафиксировать изменения
        db.session.commit()
        return render_template('yacut.html', form=form, short=short_id), 200
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url_original = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_original.original)
