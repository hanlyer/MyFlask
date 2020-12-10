
# -*- coding: utf-8 -*-
# @Author  : hanly
# Software : PyCharm
# version： Python 3.8
from flask import Flask, request, jsonify
from werkzeug.utils import redirect
from lib.connMysql import connMysql

"""
flask http 方法
get 查
post 增
put 改
delete 删
"""


app = Flask(__name__)

#flask 路由route
@app.route("/")
def hello_world():
    return "hello world"

@app.route("/hello/")
def hello_hello2():
    """"
    此函数中路由的url尾部有一个斜杠，行为表现类似一个文件夹，
    如果访问此url时尾部没有斜杠，则flask会自动重定向，在尾部加上一个斜杠
    这样URL不唯一
    """
    return "hello hello2"

@app.route("/hello")
def hello_hello():
    """"
    此函数中路由的url尾部没有斜杠，行为表现类似一个文件，
    如果访问此url时在尾部添加一个斜杠，就会报404错误
    这样可以保证URL唯一性，并帮助搜索引擎避免重复索引同一页面
    推荐此种写法
    """
    return "hello hello"

@app.route("/hey/<usr>")
def hey_usr(usr):
    return "hey %s" % (usr+usr)


@app.route("/person/<int:age>")
def person_age(age):
    return "person age is %d" % (age+age)


@app.route("/baidu")
def baidu():
    """
    重定向 redirect
    :return:
    """
    return redirect("https://www.baidu.com")


# @app.route("/personRes/",methods = ["POST"])
# def person_post():
#     """
#     {
#     "name":"张三",
#     "identifyID":"330110201705051212",
#     "uniscID":"910000000000000000"
#     }
#
#     :return:
#     """
#     person_json = request.get_json()
#     print(person_json)
#     get_name = person_json.get("name")
#     get_identifyID = person_json.get("identifyID")
#     get_uniscID = person_json.get("uniscID")
#     print(get_uniscID)
#     print(type(get_uniscID))
#     return jsonify(name = get_name)
#
@app.route("/register",methods = ["POST"])
def register_post():
    """
    {
    "type":"wz"，
    "name":"张三",
    "identifyID":"330110201705051212",
    "socialCode":"910000000000000000",
    "company":"公司名称测试",
    "companyAddr":"公司地址测试"
    }

    :return:
    """
    register_json = request.get_json()
    print(register_json)

    get_type = register_json.get("type")
    get_name = register_json.get("name")
    get_identifyID = register_json.get("identifyID")
    get_socialCode = register_json.get("socialCode")
    get_company = register_json.get("company")
    get_companyAddr = register_json.get("companyAddr")

    print(get_socialCode)
    print(type(get_socialCode))
    if get_type == 'wz':
        conn = connMysql()
        sql_mysql = '''
           insert into enterprise_info (uniscId,legalPerson,companyName,CERTNO,companyAddr)
           values ('%s', '%s', '%s', '%s', '%s')
         ''' % (get_socialCode,get_name,get_company,get_identifyID,get_companyAddr)
        print(sql_mysql)
        conn.insert(sql_mysql)


    return jsonify(name = get_name)


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug= True)