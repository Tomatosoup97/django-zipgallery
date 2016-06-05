import os
from io import BytesIO
from string import punctuation

from zipfile import ZipFile
from chardet import detect as charset_detect

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.db import models

# MEDIA_ROOT + UPLOAD_DIR = Location of gallery
UPLOAD_DIR = 'galleries'

class BaseGallery(models.Model):
    """
    Abstract Gallery functionality
    Inherit for use
    """
    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
        help_text=_("gallery title"),
        )
    slug = models.SlugField(
        max_length=110,
        verbose_name='slug',
        help_text=_('url name'),
        )
    zip_import = models.FileField(
        verbose_name='zip import',
        help_text=_('upload zip file containing images'),
        upload_to=UPLOAD_DIR,
        )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Create slug based on title

        If a zip file is uploaded, extract images from it and add
        them to the gallery.
        Removes zip file afterwards
        """
        self.slug = slugify(self.title)

        super(BaseGallery, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    # backwards compatibile with PIL
                    from Pillow import Image
                    image = Image.open(BytesIO(data))
                    image.load()
                    image = Image.open(BytesIO(data))
                    image.verify()
                except ImportError:
                    pass
                except:
                    continue
                name = os.path.split(name)[1]
                # This is a way of getting around the broken nature of
                # os.path.join on Python 2.x. See also the comment below.
                if isinstance(name, bytes):
                    encoding = charset_detect(name)['encoding']
                    tempname = name.decode(encoding)
                else:
                    tempname = name

                # A gallery with a slug of "/" tries to extract files
                # to / on disk
                slug = self.slug if self.slug != "/" else ""
                path = os.path.join(UPLOAD_DIR, slug, tempname)
                saved_path = default_storage.save(path, ContentFile(data))
                self.images.create(file=saved_path)
            zip_file.close()
            self.zip_import.delete(save=True)

class Gallery(BaseGallery):
    """
    Pure, basic gallery
    """
    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

class GalleryImage(models.Model):
    """
    Images for gallery
    """
    gallery = models.ForeignKey(Gallery, related_name="images")
    file = models.FileField(upload_to=UPLOAD_DIR)
    description = models.CharField(
        verbose_name=_('description'), max_length=400, blank=True,
        help_text=_('leave blank to autogenerate from image name'),
        )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = force_text(self.file)
            name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(GalleryImage, self).save(*args, **kwargs)