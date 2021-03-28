# -*- coding:utf-8 -*-
__author__ = 'yuyonghang'

import dataset
from config import database_url



# data access object
class NoteInfoDao:
    #                     协议     账号  密码                ip   : 端口 / db_name
    db = dataset.connect(database_url)

    @classmethod
    def get_note_list_by_uid(cls, uid):
        res = cls.db.query('select * from note_info where uid = :uid;', {"uid": uid})
        res = [dict(item) for item in res]
        return res

    @classmethod
    def get_uid_by_note_id(cls, note_id):
        res = cls.db.query('select * from note_info where tid = :note_id;', {"note_id": note_id})
        res = [dict(item) for item in res]
        if res:
            note = res[0]
            uid = note['uid']
            return uid
        return None

    @classmethod
    def get_note_by_id(cls, note_id):
        res = cls.db.query('select * from note_info where tid = :note_id', {"note_id": note_id})
        res = [dict(item) for item in res]
        if res:
            return res[0]
        return None



    @classmethod
    def create_note(cls, uid, create_time, title, content):
        sql = 'insert into note_info (uid, create_time, title, content) values (:uid, :create_time, :title, :content)'
        params = {
            'uid': uid,
            'create_time': create_time,
            'title': title,
            'content': content
        }
        cls.db.query(sql, params)

    @classmethod
    def delete_note_by_id(cls, note_id):
        res = cls.db.query('delete from note_info where tid = :note_id', {"note_id": note_id})



