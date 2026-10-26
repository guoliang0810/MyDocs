import unittest, requests


"""
 1. 面试记录
 2. 面试记录管理
 3. 面试排行榜
"""


class mianshi(unittest.TestCase):
    headers = {
        "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA"
    }

    def setUp(self) -> None:
        print('=====================================')

    def tearDown(self) -> None:
        print('=====================================')

    def test_mianshi_jilu_01(self):
        url ="http://sx.baway.tech:8060/dev-api/sxpt/station/selectStationLabel"
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())

    def test_mianshi_jilu_02(self):
        url = "http://sx.baway.tech:8060/dev-api/sypt/interview/interviewList?searchTitle=&status=&pageNum=1&pageSize=10"
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())

    def test_mianshi_guanli_01(self):
        url = "http://sx.baway.tech:8060/dev-api/sypt/interview/interviewManage?pageNum=1&pageSize=10&searchTitle= "
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())

    def test_mianshi_paihang_01(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/classPlan/getClassInfo"
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())

    def test_mianshi_paihang_02(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/blacking/blackList "
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())

    def test_mianshi_paihang_03(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/interview/interviewRecordRangkingTeacher?classId= "
        r = requests.get(url=url, headers=mianshi.headers)
        print(r.json())


if __name__ == '__main__':
    unittest.main()














