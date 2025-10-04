#!/bin/bash -x

BASE_DIR="$(cd $(dirname $0) && pwd)"
OUT_DIR="$BASE_DIR/sphinx_corpo_theme/static/css"
ARGS="--style compressed"

mkdir -p $OUT_DIR

if [[ ! "$OUT_DIR" || ! -d "$OUT_DIR" ]]; then
    echo "Could not create temporary directory"
    exit 1
fi

docker run -it --rm -v "$BASE_DIR/scss":/scss -v "$OUT_DIR":/css -w /scss dart-sass:latest $ARGS \
    /scss/priority.scss:/css/priority.css \
    /scss/blog.scss:/css/blog.css \
    /scss/styles.scss:/css/styles.css

