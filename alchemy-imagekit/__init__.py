#!env/bin/python
# -*- coding: utf-8 -*-

from pilkit.processors import ProcessorPipeline

from pilkit import utils

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


class ImageSpecField(object):

    def __init__(
        self, model=None, dest=None, processors=None, format='JPEG', options=None,
            source=None, id=None, uploads_dir=None):

        self.processors = processors
        self.format = format
        self.options = options
        self.source = source
        self.id = id
        self.dest = dest
        self.model = model
        self.uploads_dir = uploads_dir

    def get_uploads_dir(self):
        """ 
        Returns the base dir where original and generated images are stored 
        
        It looks first for the directory passed as a parameter, 
        if it is None, it looks for the config module.
        If none of this exists, it throws an exception
        """

        if self.uploads_dir:
            uploads_dir = self.uploads_dir
        else:
            try:
                import config
                uploads_dir = config.UPLOADS_DIR
            except Exception, e:
                e.message += " You shoud have a config module in \
                your App or send a uploads_dir parameter to your specs"
                raise e

        return uploads_dir

    def get_extension(self):
        return '.' + self.format.lower()

    def url(self):
        """ Returns the final url for this version of the image. 
        If it doesn't exists, it generates it"""

        uploads_dir = self.get_uploads_dir()

        img = Image.open(os.path.join(uploads_dir, self.source))

        # We generate a filename using the original image's histogram and internal variables
        # the filename's end is sent by the caller, but it should be the field name for
        # this image version
        hashimg = hashlib.sha256()
        propertieslist = [str(self.source), str(self.dest), str(
            self.processors), str(self.format), str(self.options), str(self.uploads_dir)]
        hashimg.update(str(img.histogram()) + ','.join(propertieslist))

        file_extension = self.get_extension()

        new_image_filename = str(
            hashimg.hexdigest()) + "_" + self.dest + file_extension

        # generate the full names and create directories if necesary
        base_cache_dir = os.path.join('cache', self.model, str(self.id))

        cache_dir = os.path.join(
            uploads_dir, base_cache_dir)

        cache_filename = os.path.join(
            cache_dir, new_image_filename)

        if not os.path.exists(cache_dir):
            mkdir_p(cache_dir)

        # Check if the generated image already existed
        if os.path.exists(cache_filename):
            return "/cache/" + self.model + "/" + str(self.id) + "/" + new_image_filename

        else:

            # we process the image and save it on the cache folder
            processor = ProcessorPipeline(self.processors)
            new_image = processor.process(img)

            utils.save_image(new_image, cache_filename, self.format, self.options)

            return os.path.join(base_cache_dir, new_image_filename)

    def __unicode__(self):
        return self.url()

    @classmethod
    def specs(cls, source, dest=None, processors=None, format='JPEG', options=None, uploads_dir=None):
        return FieldProperty(cls, source, dest, processors, format, options, uploads_dir)


class FieldProperty(object):

    def __init__(self, field, source, dest, processors, format, options, uploads_dir):
        self.field, self.source, self.dest, self.processors, self.format, self.options, self.uploads_dir = field, source, dest, processors, format, options, uploads_dir

    def __get__(self, obj, typ=None):

        if typ is None:
            typ = obj.__class__
        specs = self.field(
            source=getattr(obj, self.source),
            dest=self.dest,
            processors=self.processors,
            options=self.options,
            format=self.format,
            uploads_dir=self.uploads_dir,
            model=typ.__name__,
            id=obj.id)
        print "en get: " + str(self.uploads_dir)
        print typ.__name__
        return specs.url()
