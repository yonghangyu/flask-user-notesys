# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

import dataset

db = dataset.connect('mysql://root:123123@127.0.0.1/get_start')


def get_by_uid(uid):
    res = db.query('select * from user_info where uid = :param1;', {"param1": uid})
    res = [dict(item) for item in res]
    if res:
        return res[0]
    return None


#resp = get_by_uid(1)
#print(resp)
