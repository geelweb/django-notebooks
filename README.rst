================
django-notebooks
================

Django app to store collection of items. Collections are save using localStorage
if the user is not authenticated, or in database if the user is authenticated.


Install
=======

Using Pypi::

    pip install https://github.com/geelweb/django-notebooks/archive/master.zip


Configuring
===========

Add ``geelweb.django.notebooks`` to ``INSTALLED_APPS``.

Create the db with ``python manage.py syncdb``

Load the notebooks tags in your templates with ``{% load notebooks %}``


Models
======

NotebookItem
------------

**user**

Required. A auth.User object.

**content_type**

Required. A contenttypes.ContentType object.

**object_id**

Required. Id of the object stored.


Template tags
=============

**notebook**

Render a notebook collection. Example::

    {% notebook 'catalog' 'product' %}

The syntax is::

    {% notebook 'app_label' 'model' %}

The default template is somethings basic like::

    <ul>
        {% for item in collection %}
        <li>{{ item }}</li>
        {% endfor %}
    </ul>

You can alter the part in the li tags adding a template
``app_label/notebooks/item.html``. The item will be assign to the template in
the ``item`` variable.

In the previous example, to customise the list items for the collection of catalog
products, we can create a template in ``templates/catalog/notebooks/item.html``
with by example::

    <li class="media">
        <a class="pull-left thumbnail" href="{% url 'product' pk=item.id %}">
            <img src="{{ item.thumbnail.image.url }}" />
        </a>
        <div class="media-body">
            <h3 class="media-heading">{{ item }}</a>
        </div>
    </li>


**add_to_notebook**

Render a button to store an element to the collection. Example::

    {% notebook 'catalog' 'product' product.id %}

The syntax is::

    {% notebook 'app_label' 'model' object_id %}
