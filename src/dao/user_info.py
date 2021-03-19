# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

import dataset


# data access object
class UserInfoDao:
    #                     协议     账号  密码                ip   : 端口 / db_name
    db = dataset.connect('mysql://root:123123@127.0.0.1/get_start')

    @classmethod
    def get_by_username(cls, username):
        res = cls.db.query('select * from user_info where username = :username;', {"username": username})
        res = [dict(item) for item in res]
        if res:
            return res[0]
        return None

    @classmethod
    def get_by_uid(cls, uid):
        res = cls.db.query('select * from user_info where uid = :uid;', {"uid": uid})
        res = [dict(item) for item in res]
        if res:
            return res[0]
        return None

    @classmethod
    def create_user(cls, username, password):
        sql = 'insert into user_info (username, password) values (:username, :password)'
        params = {
            'username': username,
            'password': password,
        }
        cls.db.query(sql, params)


if __name__ == '__main__':
    res = UserInfoDao.get_by_uid(1)
    print(res)
