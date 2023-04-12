import os, json, sys
import geoip2.database as gid
from flask import Flask, request, render_template

class Response:
    def createOutput(self, ok, status, code, msg):
        return {
            "ok": ok,
            "status": status,
            "code": code,
            "msg": msg 
        }

    def ok(self, msg):
        return self.createOutput(True, "ok", 200, msg)
    
    def error(self, msg):
        return self.createOutput(False, "error", 400, msg)
    
    def warning(self, msg):
        return self.createOutput(True, "warning", 404, msg)

class Router:
    def __init__(self) -> None:
        self.router = Flask(__name__)
        self.router.add_url_rule('/', view_func=self.handleForm, methods=['GET', 'POST'])
        self.reader = gid.Reader(os.environ['ROOT'] + '/../data/GeoLite2_City/GeoLite2-City.mmdb')

    def run(self):
        port = sys.argv[1] if sys.argv and sys.argv[1] else 5000 
        self.router.run(debug=False, host='0.0.0.0', port=port)

    def handleForm(self):
        if request.method=='POST':
            return self.formSubmit()

        return render_template('home.html')
    
    def formSubmit(self):
        if not request.form.get('ip'):
            return json.dumps(Response().warning("Invalid IP provided."))
        
        with self.reader as reader:
            try: 
                response = reader.city(request.form.get('ip'))
                if response:
                    return json.dumps(Response().ok({
                        "ip": request.form.get('ip'),
                        "country": response.country.iso_code,
                        "postal": response.postal.code,
                        "city": response.city.name,
                        "time_zone": response.location.time_zone,
                        "accuracy_radius": response.location.accuracy_radius
                    }))
                else:
                    return json.dumps(Response().error("IP not found."))
            except Exception as e:
                return json.dumps(Response().error(str(e)))


if __name__=="__main__":
    router = Router()
    router.run()
