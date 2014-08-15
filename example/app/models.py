#!env/bin/python
# -*- coding: utf-8 -*-

from app import db

from alchemy_imagekit import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit, Adjust
from PIL import Image

import os
from PIL import ImageFilter

class LensBlur(object):
	""" filtro de blur a la imagen """
	def process(self, image):
		# Code for adding the watermark goes here.
		image = image.convert('RGB')
		iterations = 6
		n = 0
		while n < iterations:
			image = image.filter(ImageFilter.BLUR)
			n += 1
		return image


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

    image_thumb = ImageSpecField.specs(source='image', processors=[ResizeToFill(280, 175)], dest='image_thumb')
    image_water = ImageSpecField.specs(source='image', processors=[ResizeToFill(800, 600), LensBlur()], dest='image_water')
    image_blackandwhite = ImageSpecField.specs(source='image', processors=[ResizeToFill(400, 300), Adjust(color=0.5)], dest='image_blackandwhite')

    def __unicode__(self):
        return self.title

