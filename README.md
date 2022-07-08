# ELG proxy for Turku neural parser

## Information

This repository contains
[ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html)
Flask based ELG proxy for
[Turku neural parser pipeline](https://turkunlp.org/Turku-neural-parser-pipeline/)

Original authors for TNPP:
Jenna Kanerva and Filip Ginter and Niko Miekka and Akseli Leino and Tapio Salakoski.
Turku Neural Parser Pipeline: An End-to-End System for the CoNLL 2018 Shared Task,
Proceedings of the CoNLL 2018 Shared Task: Multilingual Parsing from Raw Text to
Universal Dependencies,
Association for Computational Linguistics, Brussels, Belgium, 2018.
Source code published under Apache-2.0 License.

This ELG API was developed in EU's CEF project:
[Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Quickstart

### Development

```
git clone https://github.com/lingsoft/tnpp-proxy-elg.git
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 8000
```

Note. Use ELG compatible TNPP container on localhost.

Tests

```
python -m unittest discover -s tests/ -v
```

### Usage

```
docker build -t lingsoft/tnpp-proxy:<tagname> .
docker run --rm -p 8000:8000 --init lingsoft/tnpp-proxy:<tagname>
```

Or pull directly ready-made image `docker pull lingsoft/tnpp-proxy:<tagname>`.

Simple test call

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process -d '{"type":"text","content":"Minulla on koira."}'
```

Response should be

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "udpipe/docs": [
        {
          "start": 0,
          "end": 17,
          "features": {
            "doc_id": 1
          }
        }
      ],
      "udpipe/paragraphs": [
        {
          "start": 0,
          "end": 17,
          "features": {
            "par_id": 1
          }
        }
      ],
      "udpipe/sentences": [
        {
          "start": 0,
          "end": 17,
          "features": {
            "sent_id": 1
          }
        }
      ],
      "udpipe/tokens": [
        {
          "start": 0,
          "end": 7,
          "features": {
            "words": [
              {
                "id": "1",
                "form": "Minulla",
                "lemma": "minä",
                "upos": "PRON",
                "feats": "Case=Ade|Number=Sing|Person=1|PronType=Prs",
                "head": 0,
                "deprel": "root",
                "misc": "TokenRange=0:7"
              }
            ]
          }
        },
        {
          "start": 8,
          "end": 10,
          "features": {
            "words": [
              {
                "id": "2",
                "form": "on",
                "lemma": "olla",
                "upos": "AUX",
                "feats": "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act",
                "head": 1,
                "deprel": "cop:own",
                "misc": "TokenRange=8:10"
              }
            ]
          }
        },
        {
          "start": 11,
          "end": 16,
          "features": {
            "words": [
              {
                "id": "3",
                "form": "koira",
                "lemma": "koira",
                "upos": "NOUN",
                "feats": "Case=Nom|Number=Sing",
                "head": 1,
                "deprel": "nsubj:cop",
                "misc": "SpaceAfter=No|TokenRange=11:16"
              }
            ]
          }
        },
        {
          "start": 16,
          "end": 17,
          "features": {
            "words": [
              {
                "id": "4",
                "form": ".",
                "lemma": ".",
                "upos": "PUNCT",
                "head": 1,
                "deprel": "punct",
                "misc": "SpacesAfter=\\n|TokenRange=16:17"
              }
            ]
          }
        }
      ]
    }
  }
}
```

Text request can also contain a parameter:

```json
{
    "type":"text",
    "content": "text to be parsed",
    "params": {
        "includeConllu": true
    }
}
```

Boolean parameter `includeConllu` controls the API in outputting the original
ConLL-U format from the parser. The parameter has a default value of `false`.

### Local installation

Use ELG-compatible service locally

```
cd elg_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image).
