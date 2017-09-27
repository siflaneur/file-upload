# coding=utf-8
import os
import uuid
from datetime import datetime

from PIL import Image
from flask import abort, request
from werkzeug.utils import cached_property

from mimes import IMAGE_MIMES, AUDIO_MIMES, VIDEO_MIMES
from utils import get_file_path, get_file_md5
from app import app, db


class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    uploadtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __init__(self, filename='', mimetype='application/octet-stream',
                 size=0, filehash=None, filemd5=None):
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename = filename if filename else self.filehash
        self.filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return "{}.{}".format(uuid.uuid4().hex, suffix)
