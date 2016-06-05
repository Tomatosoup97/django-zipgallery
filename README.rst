==================
Django Zip Gallery
==================

This package is for creating galleries from .zip file with images - no need to add image one by one.

Internal image names are auto-generated from image file names - keep in mind while improving your SEO

Quick start
-----------

1. Download via `pip install django-zipgallery`
2. Add "zipgallery" to your INSTALLED_APPS
    INSTALLED_APPS = [
    ...
    'zipgallery'.
    ]
3. Run `python manage.py migrate` to create gallery models 
4. Start running your development and visit admin panel add new gallery

Created by Mateusz Urbanczyk a.k.a Tomatosoup




Based on 'Mezzanine'_ solution for uploading zip to gallery
See LICENSE for more
.. _`mezzanine`: https://github.com/stephenmcd/mezzanine