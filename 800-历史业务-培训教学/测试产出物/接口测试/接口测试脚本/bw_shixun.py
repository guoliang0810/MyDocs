import requests, unittest


'''
1. 实训计划
2. 实训进度
3. 实训答辩
'''


class shixun(unittest.TestCase):
    headers = {
        "Cookie": "Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjMxNDlmY2VmLWYyOTUtNDAxOS04NzdlLTE4ZjM0MjUzZTkyMiJ9._ri4_5sxEjPVLEuiyKrZ0Suwl0vGioXNMrXBWs3fUHBpXJs0LIrTLAN_iIW_QilAgD-j17pitKc2kL1u0oRdMA"
    }

    def setUp(self) -> None:
        print('=====================================')

    def tearDown(self) -> None:
        print('=====================================')

    def test_shixun_plan_01(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/classPlan/getClassInfo"
        r = requests.get(url=url,headers= shixun.headers)
        print(r.json())

    def test_shixun_plan_02(self):
        url = 'http://sx.baway.tech:8060/dev-api/sxpt/classPlan/getPlanList?classId=&searchName=&ifFinished=1&pageNum=1&pageSize=10'
        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())

    def test_shixun_jindu_01(self):
        url ="http://sx.baway.tech:8060/dev-api/sxpt/progress/selectClassPlan"
        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())

    def test_shixun_jindu_02(self):
        url="http://sx.baway.tech:8060/dev-api/sxpt/progress/selectClassPlanInit?classid=&classPlanid="
        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())

    def test_shixun_jindu_03(self):
        url = "http://sx.baway.tech:8060/dev-api/sxpt/progress/classRank?classid=&classPlanid="
        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())

    def test_shixun_dabian_01(self):
        url ="http://sx.baway.tech:8060/dev-api/sxpt/station/selectStationLabel"
        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())

    def test_shixun_dabian_02(self):

        url = "http://sx.baway.tech:8060/dev-api/sxpt/defence/getDefenceList?pageNum=1&pageSize=10&searchTitle=&defenceMjorId=&defenceStatus="

        r = requests.get(url=url, headers=shixun.headers)
        print(r.json())


if __name__ == '__main__':
    unittest.main()

















