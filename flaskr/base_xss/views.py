from flask import render_template, request, render_template_string, redirect, current_app
from multiprocessing import Process
from ..main import db
from . import base_xss
from . import phantom
from .models import Xss
flag1 = 'lectureCTF{wasnt-that-hard-was-it}'

@base_xss.route('/f4b79862d3dbfcc2c45ae07df16d0d6f')
def xss_set_flag_cookie():
    redirect_to_index = redirect('/')
    response = current_app.make_response(redirect_to_index)
    response.set_cookie('totally_not_the_flag', value=flag1)
    return response


@base_xss.route('/<xss_id>')
def xss_post_page(xss_id):
    if xss_id == '404':
        return render_template_string('')

    xss = Xss.query.filter_by(id=xss_id).scalar()
    if xss is None:
        return render_template_string("404")
    print('[+] XSS Payload Request: ID: ', xss_id, xss.content, '|', xss.id,
          '|', xss.title)
    return render_template('post.html', xss=xss)


@base_xss.route('/', methods=['GET', 'POST'])
@base_xss.route('/create', methods=['GET', 'POST'])
def xss_create_page():
    if request.method == 'GET':
        message = 'hello'
        return render_template('create.html', message=message)
    elif request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        # process payload here if you want to do anything with it
        title = xss_filter(title)
        content = xss_filter(content)
        new_xss = Xss(title=title, content=content)
        db.session.add(new_xss)
        db.session.commit()
        if "PhantomJS" not in request.headers['User-Agent']:
            print("Calling phantomJS")
            p = Process(
                target=phantom.xss_get,
                args=(request.url_root + str(new_xss.id), ))
            p.start()
        return render_template(
            'success.html', id=new_xss.id, title=title, content=content)


def xss_filter(payload):
    payload = payload.replace("script", "XSS ATTEMPT DETECTED")
    payload = payload.replace('<', '&lt;')
    payload = payload.replace('>', '&gt;')
    return payload
