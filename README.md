# datasette-vega-dashboards

[![PyPI](https://img.shields.io/pypi/v/datasette-vega-dashboards.svg)](https://pypi.org/project/datasette-vega-dashboards/)

Build custom Vega/Vega-Lite dashboards in Datasette.

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-vega-dashboards

## Usage

See the example fixture in `example_fixture` for a minimal example.

In the minimal example, we create a canned query in `metadata.json`:

```json
"read_sleep": {
  "hide_sql": true,
  "sql": "SELECT * FROM sleep_log ORDER BY date DESC LIMIT 20",
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
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": "container",
    "description": "sleep quality over time",
    "mark": "line",
    "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "subjective_quality", "type": "quantitative", "aggregate": "average"}
    }
}
</script>
</div>
```

Note that the Vega-Lite spec above does not contain a `data` field --
any data field will be replaced by the plugin based on the data returned
by the canned query. For Vega specs, the data field will be prepended
with a new dataset with the name `data`.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-vega-dashboards
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
