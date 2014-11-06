from flask import Flask
from website import Website

app = Flask(__name__)
webs = Website()

@app.route('/')
def display_root():
    return webs.display_root()

# http://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
import os
@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js/', path)) #.replace('\\','/'))

@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css/', path)) #.replace('\\','/'))

@app.route('/data/papers.json')
def display_data():
    data = {}
    from config import get_config
    cfg = get_config()
    if cfg['_save_data_as_static_json']['is_active']: # debug
        my_path = cfg['_save_data_as_static_json']['path']
        if not cfg['debug'] and os.path.isfile(my_path):
            from json import load
            json_data_fp = open(my_path, 'r')
            data = load(json_data_fp)
            json_data_fp.close()
        else:
            from json import dump
            data = webs.json_data_with_links()
            static_json_db_fp = open(my_path, 'w')
            dump(data, static_json_db_fp, sort_keys=True, indent=2)
            static_json_db_fp.close()
    else:
        data = webs.json_data_with_links()
    from json import dumps
    return dumps(data, sort_keys=True, indent=2)


if __name__ == '__main__':
    app.run(debug=True)

# with app.test_request_context():
#     ...  print url_for('index')
#     ...  print url_for('login')
#     print url_for('login', next='/')
#     ...  print url_for('profile', username='John Doe')