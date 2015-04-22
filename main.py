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
    return app.send_static_file(os.path.join('js/', path))  # .replace('\\','/'))

@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css/', path))  # .replace('\\','/'))

@app.route('/resource/<path:path>')
def static_proxy_resource(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('resource/', path))  # .replace('\\','/'))

@app.route('/data/papers/<path:path>')
def display_paper(path):
    # check if path contains any 'C:\\' or '/../'
    import re
    regex = re.compile('[/\\\\]\\.\\.')
    m = regex.search(path)
    if m:
        return FileNotFoundError
    # end check
    from config import get_config
    if path.endswith('.pdf') or path.endswith('.PDF'):
        import platform
        full_path = get_config()['base_dir'] + path  # os.path.join(get_config()['base_dir'], path)
        if 'Windows' == platform.system():
            full_path = full_path.replace('/', '\\')
        pdf_fp = open(full_path, "rb")
        binary_pdf = pdf_fp.read()

        # http://stackoverflow.com/questions/18281433/flask-handling-a-pdf-as-its-own-page
        from flask import make_response
        response = make_response(binary_pdf)
        pdf_fp.close()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename={}'.format(path.split('/')[-1])
        return response
        # return app.send_static_file(full_path)
    else:
        return PermissionError


# def __dl_and_concat(file_list):
#     import urllib
#     res = ''
#     for f in file_list:
#         if 'http' == f[:4]:
#             res += urllib.request.urlopen(f).read().decode('utf-8')
#         else:
#             fd = open(f, 'r')
#             res += fd.read()
#             fd.close()
#     return res

# @app.route('/static/resources/script.js')
# def display_javascript():
#     from config import get_config
#     cfg = get_config()
#     if not cfg['resource_download_and_bundle']['is_active']:
#         raise FileNotFoundError
#         return None
#     js_string = __dl_and_concat(cfg['resource_download_and_bundle']['js'])
#     #css_string = __dl_and_concat(cfg['resource_download_and_bundle']['css'])
#     return js_string

@app.route('/data/papers.json')
def display_data():
    data = {}
    from config import get_config
    cfg = get_config()
    if cfg['_save_data_as_static_json']['is_active']:  # debug
        my_path = cfg['_save_data_as_static_json']['path']
        if not cfg['debug'] and os.path.isfile(my_path):
            from json import load
            json_data_fp = open(my_path, 'r')
            data = load(json_data_fp)
            json_data_fp.close()
        else:
            from json import dump
            data = webs.json_data()
            static_json_db_fp = open(my_path, 'w')
            dump(data, static_json_db_fp, sort_keys=True, indent=2)
            static_json_db_fp.close()
    else:
        data = webs.json_data()
    from json import dumps
    return dumps(data, sort_keys=True, indent=2)


if __name__ == '__main__':
    app.run(debug=True)

# with app.test_request_context():
#     ...  print url_for('index')
#     ...  print url_for('login')
#     print url_for('login', next='/')
#     ...  print url_for('profile', username='John Doe')
