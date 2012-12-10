#!/usr/bin/env python

import cv
import os
import urllib2
import hashlib
import tempfile
from StringIO import StringIO
import SimpleCV

import flask
from flask import Flask
app = Flask(__name__)
from flask import send_file

from PIL import Image


cache_dir = 'cache/'

@app.route('/face')
def face():
    """Loads jpeg image from web (cached).
        Finds the face.  Makes silhouetted image around face from it.
        Returns the new image.

        Useful for profile pictures (one face).
    """
    url = flask.request.values.get('url')
    cache_name = os.path.join(cache_dir, hashlib.md5(url).hexdigest() + '.jpg')

    
    # TODO: save final circle for speed!
    #pil_photo = Image.open(cache_name).convert('RGBA')
    #return serve_pil_image(cropped)

    # load photo if cached or download otherwise
    if not os.path.exists(cache_name):
        try:
            jpg = urllib2.urlopen(url).read()
        except:
            # try three times
            try:
                jpg = urllib2.urlopen(url).read()
            except:
                try:
                    jpg = urllib2.urlopen(url).read()
                except Exception, e:
                    return 'Not Found: %s' % e, 404
        with open(cache_name, 'wb') as f:
            f.write(jpg)

    cv_photo = SimpleCV.Image(cache_name)

    faces = cv_photo.findHaarFeatures(os.path.abspath('haarcascade_frontalface_alt.xml'))
    sizeX,sizeY = tuple(cv_photo.size())
    if faces != None:
        x,y = tuple(faces[0].coordinates())
        maxX,minX,maxY,minY = tuple(faces[0].extents())
        rX = max(maxX - x, x - minX) * 1.5
        rY = max(maxY - y, y - minY) * 1.5
        maxR = max(rX, rY)
        rx, ry = maxR, maxR # bias toward circle
    else:
        x,y = sizeX / 2, sizeY / 2
        rx, ry = sizeX / 2, sizeY / 2

    # resize toward ellipse if necessary
    maxRx = min(x, sizeX - x)
    maxRy = min(y, sizeY - y)
    rx = float(rx if rx <= maxRx else maxRx)
    ry = float(ry if ry <= maxRy else maxRy)

    # load photo and make silhouette
    # TODO: antialias?
    pil_photo = Image.open(cache_name).convert('RGBA')
    pix = pil_photo.load()
    for i in xrange(sizeX):
        for j in xrange(sizeY):
            d = (((i - x) ** 2) / (rx * rx)) + (((j - y) ** 2) / (ry * ry))
            threshold = 0.80
            if d > threshold:
                p = pix[i,j]
                if d > 1.00:
                    pix[i,j] = (0, 0, 0, 0)
                else:
                    alpha = (1.0 - d) / (1.0 - threshold) * 255.0
                    pix[i,j] = (p[0], p[1], p[2], int(alpha))

    #crop the image
    box = (int(x - rx), int(y - ry), int(x + rx), int(y + ry))
    cropped = pil_photo.crop(box)

    # return photo file image
    return serve_pil_image(cropped)

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9223))
    app.run(host='0.0.0.0', port=port, debug=True)

