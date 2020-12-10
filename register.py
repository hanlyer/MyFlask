# -*- coding: utf-8 -*-
# @Author  : hanly
# Software : PyCharm
# version： Python 3.8

import json
from flask import request
from flask import Flask
from werkzeug.utils import redirect
from lib.connMysql import connMysql
from lib.connOracle import connOracle
from config import conf
from config.jdbc import DBAdict

"""
调用方法为post
url为：http://192.168.180.76:5000/register
参数为：
   {
    "type":"wz"，
    "name":"张三",
    "identifyID":"330110201705051212",
    "socialCode":"910000000000000000",
    "company":"公司名称测试",
    "companyAddr":"公司地址测试"
    }
"""


app = Flask(__name__)

#flask 路由route
@app.route("/")
def hello_world():
    return "hello world"


#备案数据插入数据库
#http://122.224.230.26:20141/register
#http://192.168.3.46:5000/register
@app.route("/register",methods = ["POST"])
def register_post():
    """
    {
    "type":"wz",
    "name":"张三",
    "identifyID":"330110201705051212",
    "socialCode":"911111000000000000",
    "company":"公司名称测试",
    "companyAddr":"公司地址测试"
    }

    :return:
    """
    res_dict = {'flag':'Error'}
    register_json = request.get_json()
    print("客户即将插入数据为：",register_json)

    get_type = register_json.get("type")
    get_name = register_json.get("name")
    get_identifyID = register_json.get("identifyID")
    get_socialCode = register_json.get("socialCode")
    get_company = register_json.get("company")
    get_companyAddr = register_json.get("companyAddr")


    #all关键字判断是否所有的参数不为空None
    if all([get_type,get_name,get_identifyID,get_socialCode,get_company,get_companyAddr]):
        #温州、台州、湖州备案使用mysql
        if get_type in ('wz','hz','tz'):
            conn = connMysql()
            sql_mysql = '''
               insert into enterprise_info (uniscId,legalPerson,companyName,CERTNO,companyAddr)
               values ('%s', '%s', '%s', '%s', '%s')
             ''' % (get_socialCode, get_name, get_company, get_identifyID, get_companyAddr)
            datas = conn.chmod(sql_mysql,conf.SQL_SEARCH_MYSQL)
            conn.close()

        elif get_type == 'yw':

            conn = connOracle(DBAdict['ywhnl'])
            # 数据源插入hnlv_dzkasj
            sql_oracle = """
            insert into hnlv_dzkasj(QYMC,uniscid,zt,zs,fddbr,sfzjhm)
            values('%s', '%s', 'K','%s', '%s', '%s')
            """ % (get_company, get_socialCode, get_companyAddr, get_name, get_identifyID)

            datas = conn.chmod(sql_oracle, conf.SQL_SEARCH_YW)
            conn.close()

        elif get_type == 'hc' or get_type == 'sx' :
            conn = connOracle(DBAdict[get_type])
            # 数据源插入hnlv_dzkasj
            sql_oracle = """
            insert into dubai_regist_record_info(ID,SOCIAL_CODE,PERSON_NAME,PERSON_CREDIT_CARD,COMPANY_NAME,DELETE_FLAG,ADDRESS,CREATE_TIME)
            values(SEQ_REGIST_RECORD_INFO.Nextval,'%s', '%s', '%s','%s',0,'%s',SYSDATE)
            """ % (get_socialCode, get_name, get_identifyID, get_company,get_companyAddr)
            # conn.close()
            datas = conn.chmod(sql_oracle, conf.SQL_SEARCH_TZ)
            conn.close()

        else:
            res_dict['content'] = '地区错误'
            return json.dumps(res_dict,ensure_ascii=False)

        if datas == False:
            res_dict['content'] = '您提交的信用代码已被使用，请修改信用代码后重新申请'
            return json.dumps(res_dict,ensure_ascii=False)
        else:
            res_dict['flag'] = 'Success'
            res_dict['content'] = '数据源申请成功，可使用此数据源进行备案'
            return json.dumps(res_dict,ensure_ascii=False)

    else:
        res_dict['content'] = '输入参数不完整或者参数名称错误，请检查后重新输入'
        return json.dumps(res_dict, ensure_ascii=False)


@app.route('/settleSearch',methods = ["POST"])
def search_post():
    """
    查询结汇状态

    {
    "type":"wz",
    "identifyID":"330110201705051212",
    "socialCode":"911111000000000000"
    }

    :return:
    """
    register_json = request.get_json()
    print("客户即将修改的数据为：",register_json)

    get_type = register_json.get("type")
    get_identifyID = register_json.get("identifyID")
    get_socialCode = register_json.get("socialCode")

    if all([get_type,get_socialCode,get_identifyID]):

        if get_type == 'yw':
            conn = connOracle('dubaitest','dubaitest','192.168.1.55:1521/zhjport')

            # 数据源插入hnlv_dzkasj
            sql_oracle = """
                  select t.switchs,t.person_type, t.*,t.rowid from dubai_personal_info  t where t.social_credit_unified_code = '%s' and t.legal_person_idno = '%s'
                    """ % (get_socialCode,  get_identifyID)
            print(sql_oracle)
            res = conn.search(sql_oracle)
            print(res)
            if res is None:
                return '系统不存在该用户'
            else:
                if res[0] == '0':
                    return '当前用户的结汇状态为关闭'
                elif res[0] == '1':
                    return '当前用户的结汇状态为打开'
                else:
                    return '当前用户的结汇状态异常，请联系测试人员'
    else:
        return '参数数据不完整或参数名称输入有误，请检查后重新输入'


@app.route('/settleSwitch',methods = ["POST"])
def settle_post():
    """
    修改结汇状态
    {
    "type":"yw",
    "identifyID":"330102199007271221",
    "socialCode":"11330281979790281U",
    "switch":"1"
    }

    :return:
    """
    register_json = request.get_json()
    print("客户即将修改的数据为：",register_json)

    get_type = register_json.get("type")
    get_identifyID = register_json.get("identifyID")
    get_socialCode = register_json.get("socialCode")
    get_switch = register_json.get("switch")

    if all([get_type,get_identifyID,get_socialCode,get_switch]):

        if get_type == 'yw':
            conn = connOracle('dubaitest','dubaitest','192.168.1.55:1521/zhjport')


            sql_oracle = """
                    update dubai_personal_info t set t.switchs = %s  where t.social_credit_unified_code = '%s' and t.legal_person_idno = '%s'
                    """ % (get_switch, get_socialCode,  get_identifyID)
            print(sql_oracle)
            res = conn.chmod(sql_oracle)
            print(res)
            if res == True:
                return '结汇状态修改成功'
            else:
                return '结汇状态修改失败'
        #elif get_type == 'wz':



@app.route('/settleSearch/<localtype>/<identifyID>/<socialCode>')
def search_get(localtype,identifyID,socialCode):
    """
    查询结汇状态
    例：http://192.168.180.76:5000/settleSearch/yw/330102199007271221/11330281979790281U
"""
    if localtype == 'yw':
        conn = connOracle('dubaitest', 'dubaitest', '192.168.1.55:1521/zhjport')

        # 数据源插入hnlv_dzkasj
        sql_oracle = """
              select t.switchs,t.person_type, t.*,t.rowid from dubai_personal_info  t where t.social_credit_unified_code = '%s' and t.legal_person_idno = '%s'
                """ % (socialCode, identifyID)
        print(sql_oracle)
        res = conn.search(sql_oracle)
        print(res)
        if res is None:
            return '系统不存在该用户'
        else:
            if res[0] == '0':
                return '当前用户的结汇状态为关闭'
            elif res[0] == '1':
                return '当前用户的结汇状态为打开'
            else:
                return '当前用户的结汇状态异常，请联系测试人员'
    else:
        return '不是义乌的企业'


@app.route('/settleSwitch/<get_type>/<get_identifyID>/<get_socialCode>/<get_switch>',methods = ["GET"])
def settle_get(get_type,get_identifyID,get_socialCode,get_switch):
    """

    :return:
    """

    if get_type == 'yw':
        conn = connOracle('dubaitest','dubaitest','192.168.1.55:1521/zhjport')

        res_tmp = search_get(get_type,get_identifyID,get_socialCode)
        if res_tmp == '系统不存在该用户':
            return '系统不存在该用户，请检查输入参数是否有误'
        sql_oracle = """
                update dubai_personal_info t set t.switchs = %s  where t.social_credit_unified_code = '%s' and t.legal_person_idno = '%s'
                """ % (get_switch, get_socialCode,  get_identifyID)
        print(sql_oracle)
        res = conn.chmod(sql_oracle)
        print(res)
        if res is True:
            return '结汇状态修改为：%s'%( '关闭' if get_switch=='1' else '打开')
        else:
            return '结汇状态修改失败'
    else:
        return '不是义乌的企业'


@app.route('/smsSearch/<localtype>')
def sms_get(localtype):
    """
    查询验证码
    例：http://192.168.180.76:5000/smsSearch/wz
"""
    if localtype in('wz','yw','sx','fs','hz','hc','tz'):
        conn = connOracle(DBAdict[localtype])
        res = conn.search(conf.SQL_SMS)
        print(res)
        return "当前短信验证码为：%s"%res

    else:
        return '不是温州的查询'



if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug= True)