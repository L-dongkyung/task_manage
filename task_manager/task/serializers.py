from rest_framework import serializers

from task.models import Task, SubTask


# task 등록.
class TaskRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'create_user', 'team', 'title', 'content')


# task select
class TaskSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# task update
class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'content', 'team', 'is_complete')


# subtask 등록.
class SubTaskRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('team', 'task')


# subtask 삭제.
class SubTaskDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('team', 'task')


# subtask 삭제.
class SubTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('team', 'task', 'is_complete')
