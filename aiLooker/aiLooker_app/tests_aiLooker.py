from django.test import TestCase
from django.contrib.auth.models import User
import json

test_user = {"username": "testuser1", "password": "testpassword1"}


class aiLookerTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(username=test_user["username"])
        new_user.set_password(test_user["password"])
        new_user.save()

    def get_token(self):
        res = self.client.post('/api/token/',
                               data=json.dumps({
                                   'username': test_user["username"],
                                   'password': test_user["password"],
                               }),
                               content_type='application/json',
                               )
        result = json.loads(res.content)
        self.assertTrue("access" in result)
        return result["access"]

    def test_add_aiLooker_forbidden(self):
        res = self.client.post('/api/aiLooker/',
           data=json.dumps({
               'advtno'     : 1,
               'advttpcd'   : "001",
               'advttitl'   : "test1",
               'advtstadate': "2021-07-24",
               'advtenddate': "2021-07-24",
               'advtdesc'   : "aaaa",
               'advtgrdcd'  : "1",
           }),
           content_type='application/json',
           )

        self.assertEquals(res.status_code, 401)

        res = self.client.post('/api/aiLooker/',
           data=json.dumps({
               'advtno'     : 1,
               'advttpcd'   : "001",
               'advttitl'   : "test1",
               'advtstadate': "2021-07-24",
               'advtenddate': "2021-07-24",
               'advtdesc'   : "aaaa",
               'advtgrdcd'  : "1",
           }),
           content_type='application/json',
           HTTP_AUTHORIZATION=f'Bearer WRONG TOKEN'
           )

        self.assertEquals(res.status_code, 401)

    def test_add_aiLooker_ok(self):
        token = self.get_token()
        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                'advtno'     : 1,
                                'advttpcd'   : "001",
                                'advttitl'   : "test1",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "aaaa",
                                'advtgrdcd'  : "1",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]

        self.assertEquals(result["advtno"     ], 1)
        self.assertEquals(result["advttpcd"   ], '001')
        self.assertEquals(result["advttitl"   ], 'test1')
        self.assertEquals(result["advtstadate"], '2021-07-24')
        self.assertEquals(result["advtenddate"], '2021-07-24')
        self.assertEquals(result["advtdesc"   ], 'aaaa')
        self.assertEquals(result["advtgrdcd"  ], '1')

    def test_add_aiLooker_wrong_data(self):
        token = self.get_token()
        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                    'advtno'     : "1",
                                    'advttpcd'   : "001",
                                    'advttitl'   : "test1",
                                    'advtstadate': "2021-07-24",
                                    'advtenddate': "2021-07-24",
                                    'advtdesc'   : "aaaa",
                                    'advtgrdcd'  : "1",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                'advtno'     : 1,
                                'advttpcd'   : "",
                                'advttitl'   : "test1",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "aaaa",
                                'advtgrdcd'  : "1",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

    #  -------------------------- GET RECORDS -------------------------------------------

    def test_get_records(self):
        token = self.get_token()
        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                'advtno'     : 2,
                                'advttpcd'   : "002",
                                'advttitl'   : "test2",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "bbbb",
                                'advtgrdcd'  : "2",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        advtno1 = json.loads(res.content)["data"]["advtno"]

        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                'advtno'     : 3,
                                'advttpcd'   : "003",
                                'advttitl'   : "test3",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "cccc",
                                'advtgrdcd'  : "2",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        advtno2 = json.loads(res.content)["data"]["advtno"]

        res = self.client.get('/api/aiLooker/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(len(result), 2)  # 2 records
        self.assertTrue(result[0]["advtno"] == advtno1 or result[1]["advtno"] == advtno1)
        self.assertTrue(result[0]["advtno"] == advtno2 or result[1]["advtno"] == advtno2)

        res = self.client.get(f'/api/aiLooker/{advtno1}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]

        self.assertEquals(result["advtno"     ], '2'    )
        self.assertEquals(result["advttpcd"   ], '002'  )
        self.assertEquals(result["advttitl"   ], 'test2')
        self.assertEquals(result["advtstadate"], '2021-07-24')
        self.assertEquals(result["advtenddate"], '2021-07-24')
        self.assertEquals(result["advtdesc"   ], 'dddd')
        self.assertEquals(result["advtgrdcd"  ], '1')

    #  -------------------------- PUT AND DELETE RECORDS --------------------------------------

    def test_put_delete_records(self):
        token = self.get_token()
        res = self.client.post('/api/aiLooker/',
                               data=json.dumps({
                                'advtno'     : 1,
                                'advttpcd'   : "001",
                                'advttitl'   : "test1",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "aaaa",
                                'advtgrdcd'  : "1",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        advtno = json.loads(res.content)["data"]["advtno"]

        res = self.client.put(f'/api/aiLooker/{advtno}/',
                               data=json.dumps({
                                'advtno'     : 1,                                   
                                'advttpcd'   : "001",
                                'advttitl'   : "test1",
                                'advtstadate': "2021-07-24",
                                'advtenddate': "2021-07-24",
                                'advtdesc'   : "aaaa",
                                'advtgrdcd'  : "1",
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["advttpcd"], '001')

        res = self.client.get(f'/api/aiLooker/{advtno}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["advtno"     ], '1'    )
        self.assertEquals(result["advttpcd"   ], '001'  )
        self.assertEquals(result["advttitl"   ], 'test1')
        self.assertEquals(result["advtstadate"], '2021-07-24')
        self.assertEquals(result["advtenddate"], '2021-07-24')
        self.assertEquals(result["advtdesc"   ], 'aaaa')
        self.assertEquals(result["advtgrdcd"  ], '1')

        res = self.client.delete(f'/api/aiLooker/{advtno}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 410)  # Gone

        res = self.client.get(f'/api/aiLooker/{advtno}/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 404)  # Not found



