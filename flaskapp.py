import flask

app = flask.Flask(__name__)

import hacks.kookooverify
app.register_blueprint(hacks.kookooverify.app, url_prefix='/kookooverify')

if __name__ == '__main__':
    app.run(debug=True)
