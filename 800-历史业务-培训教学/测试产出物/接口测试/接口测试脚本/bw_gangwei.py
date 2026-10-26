import unittest, requests
# from bw.set_headers import SetHeader
# h = SetHeader()
# headers = h.set_header()


class gangwei(unittest.TestCase):
    """岗位"""

    headers = {
        "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA"
    }

    def setUp(self) -> None:
        print('=====================================')

    def tearDown(self) -> None:
        print('=====================================')

    def test_gangwei_01(self):
        url ="http://sx.baway.tech:8060/dev-api/sxpt/station/selectStationLabel"
        r = requests.get(url=url, headers=gangwei.headers)
        print(r.json())

    def test_gangwei_02(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/station/selectStationVersionList?isAsc=desc&pageNum=1&pageSize=10&searchTitle=&majorId=&status=&isMyInfo=false"
        r = requests.get(url=url, headers=gangwei.headers)
        print(r.json())


if __name__ == '__main__':
    unittest.main()











