# gopherflow

Gopher front-end to stack overflow

## Quick start

    $ git clone git@github.com:dacav/gopherflow
    $ cd gopherflow
    $ python3 -m virtualenv venv
    $ source venv/bin/activate
    $ pip install pituophis html2text stackexchange
    $ python -m gopherflow.server
    $ lynx gopher://localhost:9070/1/q/2483041
