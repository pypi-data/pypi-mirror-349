<h1 align="center">django-image-uploader-widget</h1>

<p align="center">
    <img src="https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/behaviour_inline.gif" />
</p>

<p align="center">
    <img alt="Supported Python Versions" src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" />
    <img alt="Supported Django Versions" src="https://img.shields.io/badge/Django-4.2%20|%205.0%20|%205.1-blue" />
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/django-image-uploader-widget" />
    <img alt="GitHub License" src="https://img.shields.io/github/license/inventare/django-image-uploader-widget" />
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/django-image-uploader-widget" />
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/inventare/django-image-uploader-widget/test.yml?label=tests" />
</p>

## Introduction

`django-image-uploader-widget` provides a beautiful image uploader widget for **django** and a multiple image inline editor for **django-admin**.

## Requirements

- Python 3.8+
- Django 4.2+
- Django 3.2,4.0,4.1 (uses `django-image-uploader-widget<=0.7.1`)

## Features

- [x] Support required and optional `ImageField`;
- [x] Support for `ImageField` inside inlines **django-admin**;
- [x] Support preview modal;
- [x] Support custom inline for **django-admin** usage.
- [x] Support reordering inside **django-admin** inline.
- [x] Support `ArrayField` for `PostgreSQL` databases.
- [x] Support upload by dropping file.
- [x] Out of box HTMX support.

## Installation

Install from PyPI:

```bash
pip install django-image-uploader-widget
```

>
> On the `1.0.0` release of this package we droped the support for `Django 3.2`, `Django 4.0` and `Django 4.1`. We, currently, maintain the support for `Django 4.2` (LTS), `Django 5.0` and `Django 5.1`. Then, if you are using `Django 3.2`, `4.0` or `4.1`, installs `0.7.1` version:
>
> ```bash
> pip install django-image-uploader-widget==0.7.1
> ```
>

Add `image_uploader_widget` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'image_uploader_widget',
    # ...
]
```

## Basic Usage

### With Admin

The `ImageUploaderWidget` is a class that implements a custom widget for single image uploader and can be used inside the `formfield_overrides` attribute inside the `ModelAdmin` class.

```python
# admin.py
from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import YourModel


@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }
```

See the [documentation](https://inventare.github.io/django-image-uploader-widget/widget/resumed/) for more complex usage's.

### With ModelForm

The `ImageUploaderWidget` can be used inside the `widgets` Meta attribute of a `Form`/`ModelForm`:

```python
# forms.py
from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

class ExampleForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'
```

See the [documentation](https://inventare.github.io/django-image-uploader-widget/widget/resumed/) for more complex usage's.

### Custom Inline Admin

The `ImageUploaderInline` is implemented with the base of the `admin.StackedInline` to create an custom **django-admin** to work with multiple images upload using a model only to store the images:

```python
# models.py

class Product(models.Model):
    # ...

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField("image")
    # ...
```

```python
# admin.py
from django.contrib import admin
from image_uploader_widget.admin import ImageUploaderInline
from .models import Product, ProductImage

class ProductImageAdmin(ImageUploaderInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
```

See the [documentation](https://inventare.github.io/django-image-uploader-widget/inline_admin/tutorial/) for more complex usage's.

### Array Field

The ArrayField support is made by a custom field, called `ImageListField`. Then, to use it, we need to change the field from default `ArrayField` to `ImageListField`. The reason for it is: the default `ArrayField` with `ImageField` not works and some part of the behaviour of the `ImageField` is implemented inside the `ImageListField`.

```python
# models.py
from django.db import models
from image_uploader_widget.postgres import ImageListField

class TestWithArrayField(models.Model):
    images = ImageListField(blank=True, null=True, upload_to="admin_test")

    class Meta:
        verbose_name = "Test With Array Field"
```

See the [documentation](https://inventare.github.io/django-image-uploader-widget/array_field/tutorial/) for more complex usage's.

## Documentation

All the documentation of basic and advanced usage of this package is disponible at [documentation](https://inventare.github.io/django-image-uploader-widget/).

## Preview

![Widget with Image in Dark Theme](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/widget_image_dark.png#gh-dark-mode-only)![Widget with Image in Light Theme](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/widget_image.png#gh-light-mode-only)

![Widget in Dark Theme](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/widget_dark.png#gh-dark-mode-only)![Widget in Light Theme](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/widget.png#gh-light-mode-only)

## Behaviour

![Widget Behaviour](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/behaviour_widget.gif)

![Custom Admin Inline Behaviour](https://raw.githubusercontent.com/inventare/django-image-uploader-widget/main/docs/_images/behaviour_inline.gif)
