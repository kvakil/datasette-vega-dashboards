# datasette-vega-dashboards

[![PyPI](https://img.shields.io/pypi/v/datasette-vega-dashboards.svg)](https://pypi.org/project/datasette-vega-dashboards/)

Build custom Vega/Vega-Lite dashboards in Datasette, for
presentation-ready plots and visualizations.

![Example Screenshot](https://raw.githubusercontent.com/kvakil/datasette-vega-dashboards/master/example_fixture/screenshot.png)

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-vega-dashboards

## Tutorial

See the example fixture in `example_fixture` for a minimal example.
You can run the fixture via:

```
datasette -m metadata.json --template-dir templates/ sleep_log.db
```

and then open
[http://127.0.0.1:8001/sleep\_log/read\_sleep](http://127.0.0.1:8001/sleep_log/read_sleep)
to see the dashboard.

In the minimal example, we create a canned query in `metadata.json`:

```json
"read_sleep": {
  "hide_sql": true,
  "sql": "SELECT * FROM (SELECT * FROM sleep_log ORDER BY date DESC LIMIT 7) ORDER BY date",
  "write": false
}
```

The template for this canned query is extended by editing the
`templates/query-sleep_log-read_sleep.html` file. You can use the
instructions provided in the [Datasette custom template
documentation](https://docs.datasette.io/en/stable/custom_templates.html#custom-templates)
to determine what the name of the file should be for other resources,
such as dashboards you want to display on a database or table.

Each graph should have a `<script>` tag wrapped in a `<div>` tag.  The
`<script>` tag should contain the Vega/Vega-Lite specification, and
*must* have a `type` of either `application/vnd.vegalite+json` (for
Vega-Lite) or `application/vnd.vega+json` (for Vega). The `<div>` tag
will be used for rendering the actual graph, and should have whatever
CSS styling you want (such as setting the width or height).

```html
<div style="width: 1000px">
    <script type="application/vnd.vegalite+json">
    /* insert vegalite spec here */
    </script>
</div>
<div style="width: 1000px">
    <script type="application/vnd.vega+json">
    /* or, insert a vega spec here */
    </script>
</div>
```

Note that the Vega-Lite spec need not contain a `data` field -- any data
field will be replaced by the plugin based on the data returned by the
canned query. For Vega specs, the data field will be prepended with a
new dataset with the name `data`.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-vega-dashboards
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
