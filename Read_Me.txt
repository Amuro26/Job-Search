此项目已具备基本的前端和后端，由于技术和时间原因，没能部署到互联网上，之后如果能有机会，我们准备将其部署到网络上。
经（我们）测试，此项目已经能在本地完整运行。

此web项目后端使用python语言，如果需要运行，需要有以下的语言包的支持：
python 3.5
flaskflask_sqlalchemy
flask_script
flask_login
flask_migrate
flask_whooshalchemyplus
flask_wtf
wtforms


项目文件中已经包含数据库创建、迁移的脚本，
且已经包含一个有一些测试数据的数据库。

如果数据库无法运行，请删除app.db文件、db_repository文件夹和search.db文件夹，并按顺序执行：
app/db_create.py
app/db_migrate.py

启动时，运行 app/run.py， 然后在浏览器中登陆本地端口（在我的电脑上测试时是   127.0.0.1:500）
如果无法运行，根目录下有一些效果图，可以粗略地查看效果。

谢谢您。
