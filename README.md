# Multi-label register classification

## Information

This repository contains
[ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html)
Flask based REST API for
[Multi-label register classification](https://github.com/annsaln/torch-transformers-multilabel)

Original authors: TurkuNLP (Veronika Laippala et al.) under different

This ELG API was developed in EU's CEF project:
[Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Quickstart

### Development

```
git clone https://github.com/lingsoft/tnpp-proxy-elg.git
docker build -t reglab-dev -f Dockerfile.dev .
docker run -it --rm -p 8000:8000 -v $(pwd):/app -u $(id -u):$(id -g) reglab-dev bash
flask run --host 0.0.0.0 --port 8000
```

Tests

```
python -m unittest discover -s tests/ -v
```

### Usage

```
docker build -t reglab .
docker run --rm -p 8000:8000 --init reglab
```

Or pull directly ready-made image
`docker pull lingsoft/tnpp-proxy:tagname`

Simple test call

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process -d '{"type":"text","content":"Hello, world!"}'
```

Response should be

```json

```

More information about registers (classes or text genres) can be found from
the file `app/ttml/README.md`.

Text request can also contain parameters:

```json
{
    "type": "text",
    "content": "Hello, world!",
    "params": {
        "sub_registers": false
    }
}
```

The `content` property contains text to be analyzed.
Note that text can not be too long (512 tokens).
The `params` property is optional and can contain

- `sub_registers` (boolean, default = true)
  - include also sub-registers (if false then general registers only)

### Local installation

Use ELG-compatible service locally

```
cd elg_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image).
