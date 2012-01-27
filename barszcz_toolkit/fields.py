import os

from django.db.models.fields.files import ImageField
from django.conf import settings


class PILThumbnailerImageField(ImageField):
    """
    Django field that behaves as ImageField but auto resizes images on upload.
    """
    def __init__(self, *args, **kwargs):
        """
        Added fields:
        - resize_source: a dict containing width and height to resize image:
            {'size': (width, height)}
        """
        self.resize_source = kwargs.get('resize_source', {})
        del kwargs['resize_source']
        super(PILThumbnailerImageField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super(PILThumbnailerImageField, self).pre_save(model_instance, add)
        if self.resize_source and (file.width != self.resize_source['size'][0] or file.height != self.resize_source['size'][1]):
            file_fullpath = os.path.join(settings.MEDIA_ROOT, file.name)
            self._resize_image(file_fullpath, self.resize_source)
        return file

    def _resize_image(self, filename, resize_source):
        """
        Resizes the image to specified width and height.
        - filename: full path of image to resize
        - resize_source: a dict containing width and height to resize image:
            {'size': (width, height)}
        """
        from PIL import Image, ImageOps
        img = Image.open(filename)
        img = ImageOps.fit(img, resize_source['size'], Image.ANTIALIAS)
        try:
            img.save(filename, optimize=1)
        except IOError:
            img.save(filename)
