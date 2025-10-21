# FastAPI Quickstart

## Prereqs
- Python 3.11+ (recommend `pyenv` or system Python)
- Pipenv (`pip install --user pipenv` if needed)

## Install (dev)
pipenv --python 3.11
pipenv sync --dev


## Install (Production)
pipenv --python 3.11
pipenv install --deploy --ignore-pipfile

## Start Server
pipenv run uvicorn app.main:app --reload

# Create items
curl -X POST http://127.0.0.1:8000/items \
  -H "content-type: application/json" \
  -d '{"name":"Azure Widget","price":19.99,"tags":["azure","blue"]}'

curl -X POST http://127.0.0.1:8000/items \
  -H "content-type: application/json" \
  -d '{"name":"Widget","price":9.99,"tags":["aws","serverless"]}'

## Db Version (Sqlite)
curl -X POST http://127.0.0.1:8000/itemsDb \
  -H "content-type: application/json" \
  -d '{"name":"Widget","price":9.99,"tags":["aws","serverless"]}'

# Get item 1
curl http://127.0.0.1:8000/items/1
curl http://127.0.0.1:8000/itemsDb/1

# List All
curl "http://127.0.0.1:8000/items"
curl "http://127.0.0.1:8000/itemsDb"


# List (optional tag filter)
curl "http://127.0.0.1:8000/items?tag=aws"
curl "http://127.0.0.1:8000/itemsDb?tag=aws"

# Secure (note: path is /items/secure because of prefix)
curl -i -H "x-api-key: secret" http://127.0.0.1:8000/items/secure

# Test
pipenv shell
pytest -q


## Optional VS Code interpreter
pipenv --venv

Run the command above in terminal, then copy that path and select it as your Python interpreter in VS Code.

## add or bump a package → resolve & regenerate lock
pipenv install <package>           # runtime
pipenv install --dev <package>     # dev-only

## update everything to latest compatible & relock
pipenv update

## keep the env tidy
pipenv clean

### CI parity (local)
```bash
pipenv --python 3.12
pipenv sync --dev
pipenv run pytest -q


### Tiny tips
- Commit **both** `Pipfile` and `Pipfile.lock`.  
- If a teammate has a different Python: they should run `pipenv --python 3.11` first, then `pipenv sync --dev`.  
- Use `pipenv --venv` to see where the venv lives; `pipenv --rm` to nuke it if needed.
::contentReference[oaicite:0]{index=0}