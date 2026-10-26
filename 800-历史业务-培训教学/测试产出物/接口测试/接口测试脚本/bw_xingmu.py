import requests,unittest
from ddt import ddt,data



"""项目首页抓取URL"""
class bawei(unittest.TestCase):
    headers = {
        "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA"
    }
    def setUp(self) -> None:
        print('=====================================')
        
    def tearDown(self) -> None:
        print('=====================================')
        
    def test_xiangmu_01(self):

        url = "http://sx.baway.tech:8060/dev-api/sxpt/label/selectMajorStationList"
        # url1 ="http://sx.baway.tech:8060/dev-api/sxpt/label/selectTradeList"
        res = requests.get(url=url, headers= bawei.headers)
        print(res.json())
        
    def test_xiangmu_02(self):
        url1 ="http://sx.baway.tech:8060/dev-api/sxpt/label/selectTradeList"
        res = requests.get(url=url1, headers= bawei.headers)
        print(res.json())

    def test_xiangmu_03(self):
        url2 = "http://sx.baway.tech:8060/dev-api/sxpt/project/selectProjectList?isAsc=desc&pageNum=1&pageSize=10&sxtype=0&status=0&proName=&newProjectList=0"
        res = requests.get(url=url2, headers=bawei.headers)
        print(res.json())


if __name__ == '__main__':
    unittest.main()










