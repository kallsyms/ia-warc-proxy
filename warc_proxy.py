#!/usr/bin/env python3
from flask import Flask, request, Response, abort
from warcio.archiveiterator import ArchiveIterator
import requests

app = Flask(__name__)


@app.route('/')
def proxy():
    iapath = request.args['iapath']
    rng = request.args['range']

    item, fn = iapath.split('/')

    meta = requests.get(f"https://archive.org/metadata/{item}").json()

    r = requests.get(f"https://{meta['d1']}{meta['dir']}/{fn}", headers={"Range": f"bytes={rng}"}, stream=True)
    for record in ArchiveIterator(r.raw, arc2warc=True):
        if record.rec_type == 'response':
            def stream():
                stream = record.content_stream()
                buf = stream.read(8192)
                while buf:
                    yield buf
                    buf = stream.read(8192)
                r.close()

            return Response(stream(), mimetype=record.http_headers.get_header('Content-Type'))

    return abort(404)


if __name__ == '__main__':
    app.run()
