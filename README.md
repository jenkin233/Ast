# Ast
构建Python程序AST,计算相似度
## 文件夹及文件说明
* data 文件夹内存放所计算出的连续commit和连续release之间的余弦相似度以及编辑距离。
* pic 文件夹内存放由data文件夹内存储的结果所画的图标
* flask-sqlalchemy 和 responder是本次两个测试对象，他们的访问地址：

    flask-sqlalchemy https://github.com/mitsuhiko/flask-sqlalchemy.git

    responder https://github.com/kennethreitz/responder.git
* build.py 用来读取python文件，然后返回每个文件对应的AST,入口函数为get_asts(file_list)
* commits.txt 和 release_commits.txt 分别存储了所测试项目的所有commit和release版本号
* main.py 为本次项目的主体，负责计算所有连续的commit和release之间AST的相似度，结果保存到文件中
* plot.py 主要用来根据生成的结果绘制图表
