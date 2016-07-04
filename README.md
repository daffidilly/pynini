# Pynini

Pynini is a fast, simple and standalone "flat" or "static" HTML generator.

**Note: Pynini is functional but the API is not stable yet.** 


## Installation

TODO


## Basic Usage: Hello, World

See ``samples/basic``. 

Create a layout file like ``src/layouts/main.html`` (it can be called anything but
by convention is in that directory):

```html
<html>
<head>
<title>{% block title %}{# title will go here #}{% endblock title %}</title>
</head>
<body>
{% block body %}
{# content will go here... #}
{% endblock body %}
</body>
</html>
```

Add a page file like ``src/pages/index.html``:

```html
{% extends "layouts/main.html" %}
{% block title %}Basic Sample{% endblock %}
{% block body %}
Hello, World
{% endblock body %}
```

Run the formatter:

    $ pynini    # or if inside the pynini src: ../../bin/pynini

See the result in ``dist/index.html``

```html
<html>
<head>
<title>Basic Sample</title>
</head>
<body>
Hello, World
</body>
</html>
```


## Background

Static sites are useful over dynamically generated sites for a number 
of reasons, like:

- they're fast to load
- they're easily cached
- they can be pushed to any hosting service, include S3
- they're easily synchronised with tools like ``rsync`` and ``lftp``
 
There is a trend in modern web applications away from dynamically
generated server-side pages and toward a mix of static server-side
HTML content, server APIs and dynamic client-side HTML templating (e.g.
React and Angular).

Pynini is inspired by [Zurb Foundation's Panini](http://foundation.zurb.com/sites/docs/panini.html)
and [Frozen Flask](http://pythonhosted.org/Frozen-Flask/).

I've sought to take the best elements of both, remove elements I didn't like,
and add in latest, modern ideas.

Use Pynini in conjection with tools like ``webpack`` to assemble the entire site
and tools like ``rsync`` and ``lftp`` to push changes to a hosting server.


## Principles

- convention over configuration and code.

  The suggested directory layout:

    src/
      layouts/
      pages/
      partials/

    dist/
    
  Page data is provided by naming conventions, so the file ``foo.html``
  can have data provided by ``foo.yml`` (or ``foo.json``).
  
- no code required.

- predefined variables ``page`` and ``root``.


Pynini differs from Panini:

- It's a standalone tool so there is no dependency on gulp (or npm)

- It uses [jinja2 templates](http://jinja.pocoo.org/docs/dev/) not Handlebars.

- Data is kept separate from HTML, unlike Panini which bundles data into the template.

- It's built with Python not JavaScript, in case that matters to anyone.

The "frozen flask" project is another inspiration, but from that I didn't like
having to have *any* code. Pynini uses data to fill in variables as well as generate
pages.


### Data

  Panini ``index.html``:

    ---
    title: Page Title
    description: Lorem ipsum.
    ---
    
    <!-- The rest of your HTML is down here. -->

  The *Pynini* version of ``index.html``:

    <!-- The rest of your HTML is down here. -->

  with additional ``index.yml`` (or ``INI`` or ``JSON``):

    title: Page Title
    description: Lorem ipsum.
    
