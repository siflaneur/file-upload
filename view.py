# coding=utf-8
from flask import request, abort, jsonify
from werkzeug.wsgi import SharedDataMiddleware

from app import app, render_template, db
from models import File
from utils import get_file_path, humanize_bytes

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/file/': get_file_path()
})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        w = request.form.get('w')
        h = request.form.get('h')
        if not uploaded_file:
            return abort(400)

        if w and h:
            paste_file = File.rsize(uploaded_file, w, h)
        else:
            paste_file = File.create_by_upload_file(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()

        return jsonify({
            'url_d': paste_file.url_d,
            'url_i': paste_file.url_i,
            'url_s': paste_file.url_s,
            'url_p': paste_file.url_p,
            'filename': paste_file.filename,
            'size': humanize_bytes(paste_file.size),
            'time': str(paste_file.uploadtime),
            'type': paste_file.type,
            'quoteurl': paste_file.quoteurl
        })
    return render_template('index.html', **locals())
