**注意！**

第一次运行后端时，要这样迁移数据库：

```
./manage.py makemigrations file judge problem submission user
./manage.py migrate
./manage.py runserver
```

`makemigrations`后面要带上app的名字，否则默认会给`django_admin`建表，导致admin的用户模型会取代我们自己写的用户模型……
