==================
Django Zip Gallery
==================

This package is for creating galleries from .zip file with images - no need to add image one by one.

Internal image names are auto-generated from image file names - keep in mind while improving your SEO

Quick start
-----------

1. Download package via ``pip install django-zipgallery``
2. Add "zipgallery" to your INSTALLED_APPS
3. Run `python manage.py migrate` to create gallery models in database
4. Start running your development and visit ``admin panel`` add new gallery

Created by `Mateusz Urbanczyk a.k.a Tomatosoup`_

Based on `Mezzanine`_ solution for uploading zip to gallery
See LICENSE for more
.. _`Mezzanine`: https://github.com/stephenmcd/mezzanine
.. _`Mateusz Urbanczyk a.k.a Tomatosoup`: http://tomatosoup.pl