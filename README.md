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
Name                                                             Stmts   Miss  Cover
------------------------------------------------------------------------------------
manage.py                                                           12      2    83%
task\__init__.py                                                     0      0   100%
task\admin.py                                                        1      0   100%
task\apps.py                                                         4      0   100%
user\apps.py                                                         4      0   100%
user\models.py                                                      36     16    56%
user\serializers.py                                                 17      1    94%
user\tests.py                                                        1      0   100%
user\urls.py                                                         4      0   100%
user\views.py                                                       24      2    92%
------------------------------------------------------------------------------------
TOTAL                                                              416     44    89%

```