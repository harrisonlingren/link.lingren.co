from flask import Flask, request, redirect, render_template, abort
from urllib.parse import urlparse
import links, json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shortlink = make_shortlink(request.form['link'])
        #print('SHORTLINK: %s' % shortlink)
        if shortlink:
            return render_template('/index.html', new_link=shortlink)
        else:
            return render_template('/index.html', error='URL must be valid!')
    else:
        return render_template('/index.html')

@app.route('/<link_id>')
def link_redirect(link_id):
    redir_link = links.click_link(link_id)
    #print('redir: %s' % redir_link)
    if redir_link:
        return redirect(redir_link['uri'])
    else:
        return abort(404), 404

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    if request.method == 'POST':
        link = request.form['link']
        if 'https://fastl.ink' in link:
            link_id = link.split('/')[-1]
            if len(link_id) == 6:
                link_obj = links.find_link(link_id)
                return render_template('/stats.html', stats_link=link_obj)
            else:
                return render_template('/stats.html', error="Looks like that isn't a valid fastlink!")
        else:
            return render_template('/stats.html', error="Looks like that isn't a valid fastlink!")
    elif request.method == 'GET':
        return render_template('/stats.html')

@app.route('/stats/<link_id>')
def stats_by_id(link_id):
    link_obj = links.find_link(link_id)
    return render_template('/stats.html', stats_link=link_obj)

@app.route('/api/new', methods=['POST'])
def api_create():
    req_body = request.get_json(force=True)
    try:
        req_url = req_body['url']
    except KeyError:
        return abort(400), 400
    return ( 'https://fastl.ink/' + make_shortlink(req_url) )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def make_shortlink(link_str):
    if verify_url(link_str):
        result = links.new_link(link_str)
        return result
    else:
        return None

def verify_url(x):
    print('checking %s...' % x)
    result = urlparse(x)
    if result.scheme == '':
        print('  invalid URI %s!' % str(result))
        return False
    elif result.scheme in ['http', 'https']:
        if result.netloc == '':
            print('  invalid http/s: %s!' % str(result))
            return False
        else:
            print('  valid URI!', [result.scheme, result.netloc, result.path])
            return True
    else:
        if result.path == '':
            print('  invalid URI %s!' % str(result))
            return False
        else:
            print('  valid URI!', [result.scheme, result.netloc, result.path])
            return True

if __name__ == '__main__':
    app.run()
