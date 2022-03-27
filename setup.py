from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-vega-dashboards",
    description="Build custom Vega/Vega-Lite dashboards in Datasette.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Keyhan Vakil",
    author_email="kvakil@pypa.kvakil.me",
    url="https://git.sr.ht/~kvakil/datasette-vega-dashboards",
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License"
    ],
    version=VERSION,
    packages=["datasette_vega_dashboards"],
    entry_points={"datasette": ["vega_dashboards = datasette_vega_dashboards"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx", "sqlite-utils"]},
    package_data={
        "datasette_vega_dashboards": ["static/*"]
    },
    python_requires=">=3.7",
)
