from datetime import datetime

from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from django.core.exceptions import ObjectDoesNotExist

from task.serializers import (
    TaskRegistrationSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
    SubTaskRegistrationSerializer,
    SubTaskCompleteSerializer,
    SubTaskUpdateSerializer,
    SubTaskListSerializer,
)
from task.models import Task, SubTask
from task.pagination import TaskPagination


class TaskRegistrationCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    pagination_class = TaskPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskRegistrationSerializer
        return TaskListSerializer

    def get_queryset(self):
        return Task.objects.filter(
            Q(create_user=self.request.user)
            | Q(subtasks__team=self.request.user.team)
        )

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
            'content': request.data['content'],
            'teams': request.data['teams']
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

    def list(self, request, *args, **kwargs):
        """
        URL: GET https://<server>/api/task/
        요청자가 생성한 task와 요청자의 team에 할당된 subtask가 있는 task 조회.
        :param request:
            cursor          str. Query start point.
        :param args:
        :param kwargs:
        :return:
            {
                "next": "<uri>?cursor=bz0xJnA9MjAyMy0wOS0yNCswMSUzQTIzJTNBMTMuODI0NTc2JTJCMDAlM0EwMA%3D%3D",
                "previous": "<uri>?cursor=cj0xJnA9MjAyMy0wOS0yNCswMSUzQTIzJTNBMTAuMzYwNzA0JTJCMDAlM0EwMA%3D%3D",
                "results": [
                    {
                        "id": 52,
                        "subtasks": [
                            {
                                "id": 23,
                                "team": <team>,
                                "is_complete": false,
                                "completed_date": null
                            },
                            {
                                "id": 24,
                                "team": <team>,
                                "is_complete": false,
                                "completed_date": null
                            }
                        ],
                        "create_user": {
                            "id": 9,
                            "username": "dong9",
                            "team": <team>
                        },
                        "team": <team>,
                        "title": "title-list4",
                        "content": "description",
                        "is_complete": false,
                        "completed_date": null,
                        "create_at": "2023-09-24T01:23:10.360704Z",
                        "modified_at": "2023-09-24T01:23:10.360704Z"
                    }, ...
                ]
            }
        """
        self.serializer_class = TaskListSerializer()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskUpdateAPIView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = SubTaskUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Task.objects.get(
            id=self.kwargs.get('pk'),
            create_user=self.request.user.id
        )

    def patch(self, request, *args, **kwargs):
        """
        URL: PATCH https://<server>/api/task/<task_id>
        :param request:
            teams           list. task에 업데이트 할 team list.
        :param args:
        :param kwargs:
        :return:
            {
                "teams": [
                    "단비",
                    "블라블라"
                ],
                "delete": [],
                "create": []
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teams: list = serializer.data['teams']
        try:
            task = self.get_queryset()
        except ObjectDoesNotExist:
            return Response({"error": "Not Found Task"}, status=status.HTTP_400_BAD_REQUEST)

        ret: dict = {
            "teams": teams,
            "delete": [],
            'create': []
        }

        # team 변경에 따른 subtask 수정.
        for team in serializer.data['all_teams']:
            subtask = task.subtasks.filter(team=team).first()
            if subtask:
                # task 팀에서 제외되고 완료가 안되어 있으면 삭제.
                if team not in teams and not subtask.is_complete:
                    subtask_ser = SubTaskRegistrationSerializer(data={'team': team, 'task': task.id})
                    subtask_ser.is_valid(raise_exception=True)
                    ret['delete'].append(subtask_ser.data)
                    subtask.delete()
            else:
                # substack이 없지만 task 팀에 있으면 추가.
                if team in teams:
                    subtask_ser = SubTaskRegistrationSerializer(data={'team': team, 'task': task.id})
                    subtask_ser.is_valid(raise_exception=True)
                    subtask_ser.save()
                    ret['create'].append(subtask_ser.data)
        return Response(ret, status=status.HTTP_200_OK)


class SubTaskCompleteAPIView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = SubTaskCompleteSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return SubTask.objects.get(
            id=self.kwargs.get('pk'),
            team=self.request.user.team,
            is_complete=False
        )

    # def patch(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     subtask = self.get_queryset()
    #
    #     return Response(serializer.data,)

    def update(self, request, *args, **kwargs):
        """
        subtask를 완료처리하는 로직. 모든 subtask가 완료되면 부모task도 완료.
        URL: PATCH https://<server>/api/subtask/
        :param request:
            is_complete             bool.
        :param args:
        :param kwargs:
        :return:
            {
                "id": 18,
                "team": "블라블라",
                "is_complete": true,
                "completed_date": "2023-09-24T09:06:44.403702Z",
                "created_at": "2023-09-24T01:22:58.704225Z",
                "modified_at": "2023-09-24T09:06:44.410047Z",
                "task": 49
            }
        """
        kwargs['partial'] = True

        # is_complete가 False 면 에러 응답.
        if not request.data['is_complete']:
            return Response({"error": "Can not restore complete."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['completed_date'] = datetime.utcnow()
        try:
            serializer = self.get_serializer(self.get_queryset(), data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({"error": "Not Found Task"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("****", serializer.data)

        return Response(serializer.data)

