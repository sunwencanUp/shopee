"""
# start
python3 http_server.py

# test
curl 'http://127.0.0.1:8001/shopee/test?a=11a&b='
curl 'http://127.0.0.1:8001/shopee/test1?a=11a&b='
curl 'http://127.0.0.1:8001/shopee/test?a=11a&b=john'
curl 'http://127.0.0.1:8001/shopee/test?a=11&b=john'
"""
import json
import urllib

import urllib.parse
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

SUCCESS_CODE = 0  # , success
SYSTEM_ERRCODE = 11  # , system error
PARAMS_ERRCODE = 21  # , empry or wrong params


class MyRequestHandler(BaseHTTPRequestHandler):

    def _output(self, code=200, body=None):
        body = json.dumps(body) if body is not None else ""
        print("response to {}: [{}]{}".format(self.client_address[0], code, body))
        self.send_response(code)
        self.send_header("Content-Length", 0 if body is None else len(body))
        self.end_headers()
        self.wfile.write(body.encode())

    def _resp(self, error_code=None, error_message=None, reference=None):
        if error_code is None: error_code = SUCCESS_CODE
        if error_message is None: error_message = "success"

        ret = {
            "error_code"   : str(error_code),
            "error_message": error_message
        }
        if reference is not None:
            ret.update({"reference": reference})

        self._output(200, ret)

    def _resp_params_err(self):
        ret = {
            "error_code"   : str(PARAMS_ERRCODE),
            "error_message": "empry or wrong params"
        }
        self._output(200, ret)

    def _resp_system_err(self):
        ret = {
            "error_code"   : str(SYSTEM_ERRCODE),
            "error_message": "system error"
        }
        self._output(200, ret)

    def _test(self, qvars):
        args = {k: vals[0] for k, vals in qvars.items()}
        print(args)
        if args.get("a") is None or args.get("a") == "" or \
                args.get("b") is None or not isinstance(args.get("b"), str):
            self._resp_params_err()
        try:
            x = int(args.get("a", ""))
        except Exception as e:
            self._resp_params_err()

        reference = f"NO.{args['a']} is {args['b']}"

        self._resp(reference=reference)

    def do_GET(self):
        try:
            print("from {}: {}".format(self.client_address[0], self.path))
            scheme, netloc, mpath, mquery, fragment = urllib.parse.urlsplit(self.path)
            qvars = urllib.parse.parse_qs(mquery)
            if mpath == "/shopee/test":
                self._test(qvars)
            else:
                self._resp_system_err()
        except Exception as e:
            self._resp_system_err()
            pass


if __name__ == "__main__":
    _server = HTTPServer(('0.0.0.0', 8001), MyRequestHandler)
    _server.serve_forever()
