#!env/bin/python
# -*- coding: utf-8 -*-

from app import db
from alchemy_imagekit import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit, Adjust

from inspect import stack
import os

from PIL import Image

class Watermark(object):
    def __init__(self, mark='nunatak_watermark.png'):
        self.mark = mark

    def process(self, image):
        # Code for adding the watermark.
        watermark = os.path.join('app', 'static', 'img', self.mark)
        print "watermark: " + watermark
        try:
            mark = Image.open(watermark)
        except IOError, e:
            raise IOError('The watermark couldn\'t be opened %s: %s' % \
                          (watermark, e))
        logoim = mark #transparent image
        image.paste(logoim,(image.size[0]/2-logoim.size[0]/2,image.size[1]/2-logoim.size[1]/2),logoim)


        return image

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))

    #image_thumb = ImageSpecField(source='image', processors=[Adjust(sharpness=1.1), ResizeToFill(280, 175)], dest='image_thumb')
    image_thumb2 = ImageSpecField.specs(source='image', processors=[Adjust(sharpness=0.1, color=0), ResizeToFill(280, 175)], dest='image_thumb2', options={'quality': 10})
    image_water = ImageSpecField.specs(source='image', processors=[Adjust(sharpness=0.1), ResizeToFit(800, 600), Watermark()], dest='image_water')

    @property
    def image_thumb(self):
        imgspec = ImageSpecField(
            processors=[Adjust(sharpness=1.1), ResizeToFill(280, 175)],
            source=self.image, 
            model=self.__class__.__name__, 
            dest=stack()[0][3], 
            id=self.id
            )
        return imgspec.url()

    def __unicode__(self):
        return self.title

