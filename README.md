# Database_Midterm_Project

数据库实验班期中项目

使用Django框架实现一个简单的博客系统

# 运行前的准备

- conda环境配置见env.yaml
- 数据库：mysql 8.0.21
- 在数据库中创建一个用户（或者用root用户也行）

  - 将用户名、密码写在mysite/settings.py中（如下）
  - 创建一个数据库 `create database Midterm_Django;`
  - ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'Midterm_Django', # 本项目使用的数据库名字
            'USER': 'Midterm_Django', # 用户名
            'PASSWORD': '12345678', # 密码
            'HOST': '127.0.0.1',
            'PORT': '3306', # 看你的mysql运行在哪个端口上
        }
    }
    ```

## 运行方法

进入根目录

- 首次运行时，先运行以下两个命令：
  `python manage.py makemigrations`

  `python manage.py migrate`

  目的是建立数据库以及你定义的表（表的定义见blog/models.py）。
  这时数据库中应该有了你定义的几个表，以及一大堆django定义的表

  > 每次修改models.py后（相当于你对数据库的定义变了），都要重新运行一遍这两个命令。
  >
- （由于django框架定义的cascade并没有体现在sql文件中，所以我们还得手动修改：

  - init.sql是django建立数据库时自动运行的sql脚本，这里存下来
  - 在init.sql中给所有外键都增加cascade
  - 在mysql中运行该脚本
- settings.sql用于在数据库中应用数据库特性（视图、trigger等），需要自己手动运行一次
- 然后运行 `python manage.py runserver`，浏览器访问 `127.0.0.1:8080/<你定义的url>即可。`

## 注意

根目录下的init.sql和test.sql不需要运行

- test.sql用于测试一些sql语句，debug用
