# RestfulAPI_Demo  学习环境准备
pip install virtualenv

新建一个文件夹，然后cd到新文件夹路径下
运行：

virtualenv.exe flask
cd 到flask文件夹下
pip install flask

然后到打开该文件夹 拷贝app.py到这个文件夹， 运行
Python app.py

登录http://127.0.0.1:5000/api/v1/allapis 查看API





请求带上基础认证， auth=("user1","password1")



带建议数据库的环境安装

pip install Flask-SQLAlchemy

首先运行app_data.py创建数据库， 重新运行即可恢复原来的数据

然后运行app.py启动webserver


