from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from task.serializers import (
    TaskRegistrationSerializer,
    TaskSelectSerializer,
    TaskUpdateSerializer,
    SubTaskRegistrationSerializer,
    SubTaskDeleteSerializer,
    SubTaskUpdateSerializer,
)


class TaskRegistrationCreateAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = TaskRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        URL: POST https://<server>/api/task/
        유저 생성 함수.
        :param request:
            teams           list.
            title           str.
            content         str.
        :param args:
        :param kwargs:
        :return:
            {
                'task': {
                    "id": <task_id>,
                    "create_user": <user_id>,
                    "team": <team>,
                    "title": <title>,
                    "content": <content>
                },
                'subtask': [
                    {
                        "team": <team>,
                        "task": <task_id>
                    }, ...
                ]
            }
        """
        # task 데이터 생성.
        task_data = {
            'create_user': request.user.id,
            'team': request.user.team,
            'title': request.data['title'],
            'content': request.data['content']
        }
        serializer = self.get_serializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        ret: dict = {
            'task': serializer.data,
            'subtask': []
        }

        # subtask 데이터 생성.
        for team in request.data.get('teams'):
            subtask_ser = SubTaskRegistrationSerializer(data={'team': team, 'task': serializer.data['id']})
            subtask_ser.is_valid(raise_exception=True)
            self.perform_create(subtask_ser)
            ret['subtask'].append(subtask_ser.data)

        headers: dict = self.get_success_headers(serializer.data)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)



