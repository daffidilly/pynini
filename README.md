# The Conflatinator

The Conflatinator, formerly known as Pynini, is a fast, simple, standalone "static" HTML generator.

## Rename

If you previously used `pip install pynini` you should now install like this:

    pip install conflatinator

or update your `requirements.txt` file to reflect the name change.


## Installation

```bash
virtualenv mypy       # Doesn't have to be "mypy"; can be anything.
. mypy/bin/activate   # Start using the new virtual python.
pip install conflatinator
```


## Basic Usage: Hello, World

For ready-to-run samples, see ``samples/basic`` and ``samples/variables``.
 
Create working directories:

    mkdir demo        # Any name you like
    cd !$             # cd into it...
    mkdir web templates release

The `web` dir is where all your HTML and other static assets will go.
It doesn't have to be called `web` but that is the default source directory.

The Conflatinator will walk the contents of that directory. 

Files with the extension `.jinja2` are processed as Conflatinator source files
and the result written to `release` directory. Files without that extension are
copied as-is. Relative paths of the files are kept as-is.

For example:

- `web/index.html.jinja2` is processed and the output written to `release/index.html`
- `web/favicon.ico` is copied as-is to `release/favicon.ico`
- `web/js/foo.js` is copied as-is to `release/js/foo.js`
- `web/js/bar.js.jinja2` is processed and the output written to `release/js/bar.js`


## Running

Run Conflatinator as a command-line script like this:

    $ conflatinator
    
Or equivalently but with less typing:

    $ c11r
    
By default the Conflatinator expects to read and write from certain directories,
but each of these can be changed with either command line options or the
`conflatinator.ini` file in the root directory of the project:

- Search source files in the `web` directory
- Read data from the `data` directory (TODO: should this just be an include dir?)
- Output to the `release` directory
- Include from the `templates` directory
 
That is the equivalent of

    $ c11r -r web -d data -o release -i templates

 
## Formatting and templates

All formatting is done through Jinja2.

You don't have to use template files, but if you do the convention is to place them
in the `templates` directory. To be more general, any file you want to access during
processing but not have included in the output should be placed in an `include`
directory, with the default being `templates`.
 
Here's an example template, which might be under `templates/main.html` (it can be
called anything):

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

Add an HTML file like ``web/index.html``:

```html
{% extends "main.html" %}
{% block title %}Basic Sample{% endblock %}
{% block body %}
Hello, World
{% endblock body %}
```

Note that you could also write `extends "templates/main.html"` if you specifc the current
directory as an include directory with `conflatinator -i .`.

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
HTML content, server APIs and dynamic client-side HTML templating such
as React and Angular.

Pynini is inspired by [Zurb Foundation's Panini](http://foundation.zurb.com/sites/docs/panini.html)
and [Frozen Flask](http://pythonhosted.org/Frozen-Flask/).

We've sought to take the best elements of both, remove elements we didn't like,
and add in our own - hopefully useful and modern - ideas.

Use Pynini in conjection with tools like ``webpack`` to assemble the entire site
and tools like ``rsync`` and ``lftp`` to push changes to a hosting server.


## Principles

TODO THIS IS OUTDATED

- convention over configuration and code.

  The suggested directory layout:

        src/
          layouts/
          pages/
          partials/
        dist/       # automatically created
    
  Page data is provided by naming conventions, so the file ``foo.html``
  can have data provided by ``foo.yml`` (or ``foo.json``).
  
- no code required.

- predefined variables ``page`` and ``root``.


Pynini differs from Panini:

- It's a standalone tool so there is no dependency on gulp (or npm)

- It uses [jinja2 templates](http://jinja.pocoo.org/docs/dev/) not Handlebars.

- Data is kept separate from HTML, unlike Panini which bundles data into the template.

- It's built with Python not JavaScript, in case that matters to anyone.

The "frozen flask" project is another inspiration, but from that we didn't like
having to have *any* code. Pynini uses data to fill in variables as well as generate
pages.


### Variables, Data and Page Generation

Pages can refer to variables defined in data files, and pages can be *generated* from data.

Data is matched by filename. Consider an example template ``about.html``:

```html
{% extends "layouts/main.html" %}
{% block body %}
<h1>About</h1>
<ul class="staff">
  {% for person in staff %}
  <li>{{person.first}} {{person.last}}
    <img alt="image of {{person.first}} {{person.last}}" src="{{person.img}}">
  </li>
  {% endfor %}
</ul>
{% endblock body %}
```

TODO HAVE ACCESS TO DATA BY A DIRECTIVE LIKE {% data 'anything.yml' %}

Data like ``staff`` must be specified in a file named ``about.yml``: (Other formats like
JSON are intended to be supported. File an issue if this is a priority.)

```yml
staff:
    - first:   Andrew
      last:    Olson
      img:     https://randomuser.me/api/portraits/men/78.jpg

    - first:   Adam
      last:    Willis
      img:     https://randomuser.me/api/portraits/men/91.jpg
```

Pages can be generated. Documentation on that is not yet written. To see an example
look in ``samples/variables``, particularly ``src/pages/products/item.html``.

