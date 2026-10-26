import unittest,requests



"""问答列表"""
"""问答管理"""

class wenda(unittest.TestCase):
    headers = {
        "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA"
    }
    def setUp(self) -> None:
        print('=====================================')
    def tearDown(self) -> None:
        print('=====================================')
    def test_wenda_list_01(self):
        url ="http://sx.baway.tech:8060/dev-api/sypt/answer/list?isAsc=desc&pageNum=1&pageSize=8&type=&questionTitle=&quality=&authentication= "
        r = requests.get(url=url, headers=wenda.headers)
        print(r.json())

    def test_wenda_list_02(self):
        url ="http://sx.baway.tech:8060/dev-api/sypt/answer/reply"
        r = requests.get(url=url, headers=wenda.headers)
        print(r.json())

    def test_wenda_guanli_01(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/classPlan/getClassInfo"

        r = requests.get(url=url, headers=wenda.headers)
        print(r.json())

    def test_wenda_guanli_02(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/answer/wait?pageNum=1&pageSize=10&classId=9&searchTitle=&status="
        r = requests.get(url=url, headers=wenda.headers)
        print(r.json())


if __name__ == '__main__':
    unittest.main()




















