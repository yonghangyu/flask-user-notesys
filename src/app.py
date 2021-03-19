# -*- coding:utf-8 -*-
__author__ = 'yuyonghang'
from flask import Flask, request, make_response, redirect, render_template

from service.user import UserService

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'hello, world!'


@app.route('/', methods=['GET'])
def welcome():
    token = request.cookies.get('token')
    if token:
        user = UserService.get_user_info(token)
    else:
        user = {}
    return render_template('welcome.html', user=user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.register(username, password)
        resp = make_response(redirect('/', '302'))
        resp.set_cookie('token', user['token'])
        return resp
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.login(username, password)
        resp = make_response(redirect('/', '302'))
        resp.set_cookie('token', user['token'])
        return resp
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect('/', '302'))
    resp.delete_cookie('token')
    return resp

@app.route('/createnote', methods=['GET', 'POST'])
def createnote():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        token = request.cookies.get('token')
        if token:
            user = UserService.get_user_info(token)
        uid = user['uid']
        UserService.createnote(uid, title, content)
        resp = make_response(redirect('/', '302'))
        return resp
    elif request.method == 'GET':
        return render_template('note.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    token = request.cookies.get('token')
    if token:
        user = UserService.get_user_info(token)
    uid = user['uid']
    note_list = UserService.get_notes(uid)
    note_list_update = UserService.update_Abbreviation(note_list)
    return render_template('notes.html', note_list = note_list_update)

@app.route('/notes/<note_id>', methods=['GET'])
def get_note_content(note_id):
    note = UserService.get_note_content(note_id)
    return render_template('content.html', note = note)

@app.route('/notes/<note_id>/delete', methods=['get'])
def delete(note_id):
    """uid = UserService.get_uid_by_note_id(note_id)
    UserService.delete_note(note_id)
    note_list = UserService.get_notes(uid)
    note_list_update = UserService.update_Abbreviation(note_list)
    return render_template('notes.html', note_list = note_list_update)"""
    UserService.delete_note(note_id)
    resp = make_response(redirect('/notes', '302'))
    return resp

















if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
