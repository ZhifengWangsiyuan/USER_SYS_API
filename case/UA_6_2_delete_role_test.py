import unittest
import requests
import os, sys
from common import urlbase
import time
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db.mysql_db import DB


class emp_delete_role(unittest.TestCase):
    ''' 删除角色接口 '''

    def setUp(self):

        table_name = "ua_role"
        data = {'ROLE_CODE':'ROLE01','ROLE_NAME': '测试角色α', 'PINYIN': 'AERFA','STATUS': '1'}
        sdata = {'ROLE_NAME': '测试角色α'}
        db = DB()
        db.insert(table_name=table_name, table_data=data)

        self.s1 = db.select(table_value='id', table_name=table_name, table_data=sdata)
        print("id:" + str(self.s1))
        db.close()

        self.base_url_login = urlbase.sit_emp() + "/login"
        self.base_url = urlbase.sit_emp() + "/role/delRole.htm"
        head = {'Content-Type': 'application/x-www-form-urlencoded'}
        ##以x-www-form-urlencoded
        payload = {'username': 'ceshi', 'password': '123456', 'verifyCode': '0000'}
        self.s = requests.Session()
        r1 = self.s.post(self.base_url_login, data=payload, headers=head)

    def test_correct_all(self):
        ''' 正确的参数_all'''

        payload = {"roleId": self.s1}
        r2 = self.s.get(self.base_url, params=payload)
        self.result = r2.json()
        self.te = r2.text
        self.assertEqual(self.result['result'], True)
        self.assertEqual(self.result['resultObject'], None)

        time.sleep(1)

    def test_roleid_incorrect(self):
        ''' 错误的的参数_roleid'''

        payload = {"roleId": 9999}
        r2 = self.s.get(self.base_url, params=payload)
        self.result = r2.json()
        self.te = r2.text
        self.assertEqual(self.result['result'], False)
        self.assertEqual(self.result['resultObject'], None)

        time.sleep(1)


    def test_allnull(self):
        ''' 错误的参数_null'''

        payload = {"roleId":None}
        r2 = self.s.get(self.base_url, params=payload)
        self.result = r2.json()
        self.te = r2.text
        self.assertEqual(self.result['result'], False)
        self.assertEqual(self.result['resultObject'], None)

        time.sleep(1)


    def tearDown(self):

        self.table_name = "ua_role"
        self.data = {'ROLE_NAME': '测试角色α'}
        db = DB()
        db.clear(table_name=self.table_name,table_data=self.data)
        db.close()

        print(self.te)



if __name__ == '__main__':
##    test_data.init_data()  # 初始化接口测试数据

    unittest.main()