# A basic "hello world" conflatinator sample.

To generate:

    c11r

TODO: actual is:

    c11r -s pages

which is annoying.


You can process a single file or directory by naming it:

    c11r pages  # TODO won't work yet

    c11r pages/index.html.jinja2   # TODO needs -s pages

TODO need:

    c11r -s pages pages/index.html.jinja2 

