#!env/bin/python
# -*- coding: utf-8 -*-

from pilkit.processors import ProcessorPipeline, ResizeToFit, Adjust

from pilkit import utils

from config import UPLOADS_DIR
import os
import errno
from PIL import Image
import hashlib


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class FieldProperty(object):
    """ TODO: hacer andar esto con todos los campos """
    def __init__(self, field, source):
        self.field, self.source = field, source

    def __get__(self, obj, typ=None):

        if typ is None:
            typ = obj.__class__
        specs = self.field(
            source = getattr(obj, self.source),
            model = typ.__name__,
            id = obj.id)

        return specs.url()


class ImageSpecField(object):

    def __init__(
        self, model=None, dest=None, processors=None, format=None, options=None,
            source=None, cachefile_storage=None, autoconvert=None,
            cachefile_backend=None, cachefile_strategy=None, spec=None,
            id=None):

        self.processors = processors
        self.format = format
        self.options = options
        self.source = source
        self.cachefile_storage = cachefile_storage
        self.autoconvert = autoconvert
        self.cachefile_backend = cachefile_backend
        self.cachefile_strategy = cachefile_strategy
        self.spec = spec
        self.id = id
        self.dest = dest
        self.model = model

    @classmethod
    def specs(cls, source):
        return FieldProperty(cls, source)

    def url(self):
        """ Obtiene la url final de la imagen, si no existe esta versión, la genera """

        img = Image.open(os.path.join(UPLOADS_DIR, self.source))


        # Generamos hash a partir del histograma
        hashimg = hashlib.sha256()
        hashimg.update(str(img.histogram()))
        new_image_filename = str(
            hashimg.hexdigest()) + "_" + self.dest + '.jpg'

        cache_dir = os.path.join(
            UPLOADS_DIR, 'cache', self.model, str(self.id))

        cache_filename = os.path.join(
            cache_dir, new_image_filename)

        if not os.path.exists(cache_dir):
            mkdir_p(cache_dir)

        # Vemos si la imagen ya existia
        if os.path.exists(cache_filename):
            return "/media/cache/" + self.model + "/" + str(self.id) + "/" + new_image_filename

        else:
            processor = ProcessorPipeline(self.processors)
            new_image = processor.process(img)

            utils.save_image(new_image, cache_filename, 'JPEG')

            return "/media/cache/" + self.model + "/" + str(self.id) + "/" + new_image_filename

    def __unicode__(self):
        return self.url()
