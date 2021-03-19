# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'
import datetime
import uuid

from dao.user_info import UserInfoDao
from dao.user_token import UserTokenDao
from dao.note_info import NoteInfoDao


class UserService:
    @staticmethod
    def register(username, password, seconds=60*60*24):
        user = UserInfoDao.get_by_username(username)
        if user:
            raise Exception('用户已存在')
        UserInfoDao.create_user(username, password)
        user = UserInfoDao.get_by_username(username)
        uid = user['uid']
        token = uuid.uuid1().hex
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        UserTokenDao.create_token(uid, token, expire_time)
        return {
            'uid': uid,
            'username': username,
            'token': token,
            'expire_time': expire_time,
        }


    def login(username, password, seconds=60*60*24):
        user = UserInfoDao.get_by_username(username)
        if not user:
            raise Exception('用户不存在，请先注册')
        uid = user['uid']
        print(uid)
        username = user['username']
        if password != user['password']:
            raise Exception ('密码错误')
        token = uuid.uuid1().hex
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        UserTokenDao.create_token(uid, token, expire_time)
        return {
            'uid': uid,
            'username': username,
            'token': token,
            'expire_time': expire_time,
        }

    @staticmethod
    def get_user_info(token):
        token_info = UserTokenDao.get_token_info(token)
        if not token_info:
            raise Exception('token 不存在')

        if token_info['expire_time'] < datetime.datetime.now():
            raise Exception('token 已失效')

        user = UserInfoDao.get_by_uid(token_info['uid'])
        return {
            'uid': user['uid'],
            'username': user['username'],
            'token': token,
            'expire_time': token_info['expire_time'],
        }

    def createnote(uid, title, content):
        create_time = datetime.datetime.now()
        NoteInfoDao.create_note(uid, create_time, title, content)

    def get_notes(uid):
        notes = NoteInfoDao.get_note_list_by_uid(uid)
        return notes

    def get_uid_by_note_id(note_id):
        uid = NoteInfoDao.get_uid_by_note_id(note_id)
        return uid

    def update_Abbreviation(note_list):
        for note in note_list:
            content = note['content']
            if len(content) > 20:
                abbr = content[0: 20]
            else:
                abbr = content
            note['abbr'] = abbr
        return note_list

    def get_note_content(note_id):
        note = NoteInfoDao.get_note_by_id(note_id)
        return note

    def delete_note(note_id):
        NoteInfoDao.delete_note_by_id(note_id)




if __name__ == '__main__':
    user_info = UserService.get_user_info('587f717872c511eba1d8c4b301c35c35')
    print(user_info)
