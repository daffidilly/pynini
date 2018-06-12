# c11n markdown demo

Usage:

```
$ cd examples/markdown
$ c11r
$ cat dist/example.html
<h3>This is HTML</h3>
<div style="border: 1px solid black; padding: 1em; margin: 1em">
<h1>This is Markdown.</h1>
...
$
```

Markdown exists between a filter, like this:

```
{% filter as_markdown %}
# This is Markdown.

- one
- two
- three
{% endfilter %}

You can also `{% include 'anyfile.md' %}` inside the filter.

