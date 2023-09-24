# task_manage
task를 생성하고 하위 task를 추가해서 팀원과 task를 공유하는 API입니다.

## Environments
```
python>=3.11
```
## Requirements
```
django==4.2.5
djangorestframework==3.14.0
markdown==3.4.4
django-filter==23.3
```

## Run
### clone
```
$ cd <target_path> 
$ git clone https://github.com/L-dongkyung/account_book.git
```
### Server start
```
$ cd ./task_manager
$ python manage.py runserver
```

## test coverage
```
Name                                                                                 Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------------
manage.py                                                                               12      2    83%
task\__init__.py                                                                         0      0   100%
task\admin.py                                                                            1      0   100%
task\apps.py                                                                             4      0   100%
task\migrations\0001_initial.py                                                          5      0   100%
task\migrations\0002_remove_task_subtask_subtask_task_task_create_user_and_more.py       6      0   100%
task\migrations\0003_alter_task_create_user.py                                           6      0   100%
task\migrations\0004_alter_subtask_task.py                                               5      0   100%
task\migrations\0005_alter_subtask_completed_date.py                                     4      0   100%
task\migrations\0006_alter_subtask_unique_together.py                                    4      0   100%
task\migrations\__init__.py                                                              0      0   100%
task\models.py                                                                          22      2    91%
task\pagination.py                                                                       4      0   100%
task\serializers.py                                                                     64      5    92%
user\serializers.py                                                                     17      1    94%
user\tests.py                                                                            1      0   100%
user\urls.py                                                                             4      0   100%
user\views.py                                                                           24      2    92%
--------------------------------------------------------------------------------------------------------
TOTAL                                                                                  416     43    90%

```