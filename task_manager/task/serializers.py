from datetime import datetime

from rest_framework import serializers

from task.models import Task, SubTask
from user.serializers import UserRegistrationSerializer


common_teams = {'단비', '다래', '블라블라', '철로', '땅이', '해태', '수피'}


# task 등록.
class TaskRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    teams = serializers.ListField(write_only=True)

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team', 'title', 'content', 'teams')

    def validate(self, attrs):
        """
        생성하려는 task의 하위 teams 목록이 유효한지 확인.
        :param attrs:
        :return:
        """
        if set(attrs.get('teams')) - common_teams:
            raise serializers.ValidationError("Not matched team")
        del attrs['teams']
        return attrs


class SubTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'team', 'is_complete', 'completed_date']


# task select
class TaskListSerializer(serializers.ModelSerializer):
    subtasks = SubTaskListSerializer(many=True)
    # task 작성자의 정보(개인정보 은닉)
    create_user = UserRegistrationSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        depth = 2


# task update
class TaskUpdateSerializer(serializers.ModelSerializer):
    teams = serializers.ListField(write_only=True)

    class Meta:
        model = Task
        fields = ('teams',)


# subtask 등록.
class SubTaskRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SubTask
        fields = ('team', 'task', 'id')


# subtask 삭제.
class SubTaskDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('team', 'task')


# subtask 삭제.
class SubTaskUpdateSerializer(serializers.ModelSerializer):
    teams = serializers.ListField()
    all_teams = serializers.ListField(read_only=True)

    class Meta:
        model = SubTask
        fields = ('teams', 'all_teams')

    def validate(self, attrs):
        """
        생성하려는 task의 하위 teams 목록이 유효한지 확인.
        :param attrs:
        :return:
        """
        if set(attrs.get('teams')) - common_teams:
            raise serializers.ValidationError("Not matched team")
        attrs['all_teams'] = common_teams
        return attrs


class SubTaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        task = instance.task
        if not task.subtasks.filter(is_complete=False):
            task.is_complete = True
            task.completed_date = datetime.utcnow()
            task.save()
        return instance





