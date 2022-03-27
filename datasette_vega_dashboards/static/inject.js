document.addEventListener('DOMContentLoaded', async () => {
    // TODO(keyhan): support other mime types
    const specNodes = [];
    for (const node of document.querySelectorAll('script[type="application/vnd.vegalite+json"]')) {
        specNodes.push({node, isVegaLite: true});
    }
    for (const node of document.querySelectorAll('script[type="application/vnd.vega+json"]')) {
        specNodes.push({node, isVegaLite: false});
    }

    if (specNodes.length === 0) {
        return;
    }

    const jsonUrl = new URL(document.querySelector('.export-links a[href*=json]').href);
    jsonUrl.searchParams.set('_shape', 'array');

    // XXX: Get the data using .text() rather than .json() since we may
    // have multiple vegaEmbeds, each vegaEmbed may mutate its copy.
    // We'll avoid this by making multiple copies via JSON.parse below.
    const dataAsJson = await (await fetch(jsonUrl)).text();

    const specRenderPromises = [];
    for (const {node, isVegaLite} of specNodes) {
        const spec = JSON.parse(node.innerText);
        const values = JSON.parse(dataAsJson);
        if (isVegaLite) {
            spec.data = {values};
        } else {
            // Vega.
            if (!spec.data) {
                spec.data = [];
            }
            spec.data.unshift({"name": "data", values});
        }
        specRenderPromises.push(vegaEmbed(node.parentNode, spec));
    }
    await Promise.all(specRenderPromises);
});
