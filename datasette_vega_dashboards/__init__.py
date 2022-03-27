from datasette import hookimpl

PLUGIN_NAME = "datasette-vega-dashboards"


def get_static_url(datasette, fragment):
    return datasette.urls.static_plugins(PLUGIN_NAME, fragment)


EXTRA_JS_URL_CACHE = dict()


@hookimpl
def extra_js_urls(datasette, database, table):
    cache_key = (datasette, database, table)
    if cache_key in EXTRA_JS_URL_CACHE:
        return EXTRA_JS_URL_CACHE[cache_key]

    plugin_config = datasette.plugin_config(PLUGIN_NAME, database=database, table=table)
    if plugin_config is None:
        plugin_config = dict()

    vega_urls = plugin_config.get(
        "vega_urls",
        [
            get_static_url(datasette, "vega@5"),
            get_static_url(datasette, "vega-lite@5"),
            get_static_url(datasette, "vega-embed@6"),
        ],
    )
    # Copy so that we don't mutate the config.
    vega_urls = vega_urls[:]
    vega_urls.append(get_static_url(datasette, "inject.js"))

    EXTRA_JS_URL_CACHE[cache_key] = vega_urls
    return vega_urls
