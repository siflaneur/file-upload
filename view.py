# coding=utf-8
import os
from flask import request, abort, jsonify, send_file, redirect
from werkzeug.wsgi import SharedDataMiddleware

from app import app, render_template, db
from models import File
from utils import get_file_path, humanize_bytes

ONE_MONTH = 60 * 60 * 24 * 30

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


@app.route('/img/<img_hash>')
def rsize(img_hash):
    w = request.args.get('w')
    h = request.args.get('h')

    old_paste = File.get_by_filehash(img_hash)
    new_paste = File.rsize(old_paste, w, h)
    return new_paste.url_origin


@app.route('/download/<file_hash>', methods=['GET'])
def download(file_hash):
    paste_file = File.get_by_filehash(filehash=file_hash)
    return send_file(open(paste_file.path, 'rb'),
                     mimetype='application/octet-stream',
                     cache_timeout=ONE_MONTH,
                     as_attachment=True,
                     attachment_filename=paste_file.filename.encode('utf-8'))


@app.route('/preview/<file_hash>')
def preview(file_hash):
    paste_file = File.get_by_filehash(file_hash)
    if not paste_file:
        path = get_file_path(file_hash)
        if not os.path.exists(path) and (not os.path.islink(path)):
            return abort(404)

        paste_file = File.create_by_old_paste(file_hash)
        db.session.add(paste_file)
        db.session.commit()

    return render_template('success.html', p=paste_file)


@app.route('/s/<symlink>')
def s(symlink):
    paste_file = File.get_by_symlink(symlink)
    return redirect(paste_file.url_p)
