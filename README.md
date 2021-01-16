# plunderphonics
Server stack for warp-lane.

## Installation

A conda environment file is supplied:

```bash
conda env create -f conda_env.yml
```

## Run

```bash
uvicorn server_app:main:app
```

The `--reload` flag is handy for development.

## Test

The OpenAPI docs are accessible at

```
http://127.0.0.0:8000/docs
```
