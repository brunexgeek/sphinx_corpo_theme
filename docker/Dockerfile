FROM sphinxdoc/sphinx:7.4.7

RUN apt update && apt install -y gettext && apt clean && \
    pip install polib sphinx-autobuild