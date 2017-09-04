from flask import Flask, request, redirect, url_for, render_template
from urllib.parse import urlparse
import links

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shortlink = make_shortlink(request.form['link'])
        print('SHORTLINK: %s' % shortlink)
        if shortlink:
            return render_template('/index.html.j2', new_link=shortlink)
        else:
            return render_template('/index.html.j2', error='URL must be valid!')
    else:
        return render_template('/index.html.j2')

@app.route('/<link_id>')
def link_redirect(link_id):
    redir_link = links.get_link(link_id)
    if redir_link:
        return redirect(redir_link)
    else:
        return render_template('/index.html.j2', error='Link not found!')

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

