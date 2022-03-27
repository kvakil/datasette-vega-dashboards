from datasette.app import Datasette
from datasette_vega_dashboards import extra_js_urls
import pytest
import sqlite_utils
import httpx


@pytest.fixture
def datasette():
    return Datasette([], memory=True)


@pytest.mark.asyncio
async def test_plugin_is_installed(datasette):
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-vega-dashboards" in installed_plugins


@pytest.mark.asyncio
async def test_static_assets(datasette):
    for url in extra_js_urls(datasette, None, None):
        assert (await datasette.client.get(url)).status_code == 200


@pytest.fixture
def datasette_custom_vega_urls(tmpdir):
    path = str(tmpdir / "foo.db")
    db = sqlite_utils.Database(path)
    db["users"].insert({"id": 1, "password": "secret"})
    generate_plugin_config = lambda url: {
        "datasette-vega-dashboards": {"vega_urls": ["vega_url_" + url]}
    }
    return Datasette(
        [path],
        memory=True,
        metadata={
            "databases": {
                "foo": {
                    "tables": {
                        "users": {
                            "plugins": generate_plugin_config("table"),
                        },
                    },
                    "plugins": generate_plugin_config("database"),
                },
            },
            "plugins": generate_plugin_config("global"),
        },
    )


@pytest.mark.asyncio
async def test_custom_vega_urls(datasette_custom_vega_urls):
    client = datasette_custom_vega_urls.client

    response = await client.get("/_memory")
    assert 200 == response.status_code
    assert b"vega_url_global" in response.content

    response = await client.get("/foo")
    assert 200 == response.status_code
    assert b"vega_url_database" in response.content

    response = await client.get("/foo/users")
    assert 200 == response.status_code
    assert b"vega_url_table" in response.content
