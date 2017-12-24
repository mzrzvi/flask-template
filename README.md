# flask-template

## Runtime

Ensure you have the following installed locally:

* `python-3.6.2`

## Setup

Create a `virtualenv` via the regular cli or `mkvirtualenv`. (Find it [here](https://virtualenvwrapper.readthedocs.io/en/latest/))

Install requirements by running:

```bash
pip install -r requirements.txt
```

Fill out all config variables in `app/config.py`. 

Replace `lol` with meaningful, secure values.

Replace the `sqlite://*.db` files with your actual database URI's.

## Local

To start server locally, execute: 

```bash
python3 run.py
```

The app will assume you're running local configurations if you haven't set your `ENVIRONMENT` variable

## Development

Export the `ENVIRONMENT` environment variable:

```bash
export ENVIRONMENT=DEVELOPMENT
```

Then run the server as above:

```bash
python3 run.py
```

The server will run on port `5000`.

## Production

Export the `ENVIRONMENT` environment variable:

```bash
export ENVIRONMENT=PRODUCTION
```

Then run the server as above:

```bash
python3 run.py
```

The server will run on port `80`.
