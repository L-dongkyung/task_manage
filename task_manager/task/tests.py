import json

from django.test import TestCase, Client

from user.models import User
from task.models import Task


client = Client()


class TaskTestCase(TestCase):
    def setUp(self):
        """Preparatory work to test the task"""
        data = {
            "username": 'unit_test',
            "team": "해태",
            "password": "asdf1234",
            "confirm_password": 'asdf1234'
        }
        res = client.post('/api/user/', json.dumps(data), content_type='application/json')
        res_body = res.json()
        self.user_id = res_body['id']
        self.headers = {
            'Authorization': f"Token {res_body['token']}"
        }

        task_data = {
            'teams': ["해태", "단비"],
            'title': 'unit_test_base',
            'content': "unit test base task"
        }
        task_res = client.post('/api/task/', json.dumps(task_data), content_type='application/json', headers=self.headers)
        task_body = task_res.json()
        self.task_id = task_body['task']['id']
        for subtask in task_body['subtask']:
            if subtask['team'] == '해태':
                self.subtask_id = subtask['id']


    def tearDown(self) -> None:
        ...

    def test_create_task(self):
        """Test that creates a task"""
        data = {
            'teams': ["해태", "단비"],
            'title': 'unit_test1',
            'content': "unit test task"
        }
        res = client.post('/api/task/', json.dumps(data), content_type='application/json', headers=self.headers)
        res_body = res.json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_body['task']['team'], "해태")

    def test_list_task(self):
        res = client.get('/api/task/', headers=self.headers)
        res_body = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(type(res_body['results']), list)
        self.assertEqual(len(res_body['results']), 1)

    def test_update_task(self):
        update_data = {
            'teams': ["단비", '철로']
        }
        res = client.patch(f'/api/task/{self.task_id}', json.dumps(update_data), content_type='application/json', headers=self.headers)

        self.assertEqual(res.status_code, 200)
        res_body = res.json()
        self.assertEqual(res_body['delete'][0]['team'], '해태')
        self.assertEqual(res_body['create'][0]['team'], '철로')

    def test_complete_subtask(self):
        res = client.patch(
            f'/api/subtask/{self.subtask_id}',
            json.dumps({"is_complete": True}),
            content_type='application/json',
            headers=self.headers
        )

        res_body = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_body['id'], self.subtask_id)
        self.assertEqual(res_body['is_complete'], True)
        self.assertEqual(res_body['task'], self.task_id)








