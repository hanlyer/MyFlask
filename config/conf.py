from datetime import datetime

"""
公共配置项
"""
#查询短信验证码sql
SQL_SMS = "select t.captcha from dubai_sms_captcha  t order by t.create_time desc"

TIME = datetime.now()  # 获取当前时间
TIME_TO_STR = datetime.strftime(TIME, '%Y%m%d%H%M%S')  # 将当前时间转换为字符串
CODE_TO_TEN = TIME_TO_STR[2:-2]  # 截取后十位作为海关十位编码
CURRENT_DATE = datetime.strftime(TIME, "%Y-%m-%d")  # 当天日期

#数据源插入enterprise_info 到mysql数据库
# SQL_SOURCE_MYSQL = '''
#    insert into enterprise_info (uniscId,legalPerson,companyName,CERTNO,companyAddr)
#    values (CONCAT('910K',date_format(now(), '%Y%m%d%H%i%s')),CONCAT('名测',floor(rand()*10000)),
#    CONCAT('公司名称测试',floor(rand()*10000)),CONCAT('33011020000101',floor(rand()*10000)),
#    CONCAT('公司地址测试',floor(rand()*10000)))

SQL_SEARCH_MYSQL = """
select * from enterprise_info order by id desc
"""

#义乌数据表
#数据源插入hnlv_dzkasj，结汇主体类型（结汇个人）
# SQL_PERSON_ORACLE =  """
# insert into hnlv_dzkasj(QYMC,uniscid,zt,zs,fddbr,sfzjhm)
# values('义乌公司名称测试'||trunc(dbms_random.value(0,10000)),'922H'||(select to_char(sysdate,'yyyymmddhh24miss') from dual),
# 'K','浙江省义乌市','法人测试'||trunc(dbms_random.value(0,10000)),'33010219770327'||trunc(dbms_random.value(0,10000)) )
# """

#数据源插入hnlv_dzkasj ,企业类型（小微企业，外商）
# SQL_COM_ORACLE =  """
# insert into hnlv_dzkasj(QYMC,uniscid,zt,zs,fddbr,sfzjhm)
# values('义乌公司名称测试'||trunc(dbms_random.value(0,10000)), '912G'||(select to_char(sysdate,'yyyymmddhh24miss') from dual),
# 'K','浙江省义乌市','法人测试'||trunc(dbms_random.value(0,10000)),'33010320770327'||trunc(dbms_random.value(0,10000)) )
# """

SQL_SEARCH_YW = "select t.*,t.rowid from hnlv_dzkasj  t order by t.id desc"

#青岛台州绍兴数据表
# SQL_SOURCE_TZ = '''
# insert into dubai_regist_record_info(ID,SOCIAL_CODE,PERSON_NAME,PERSON_CREDIT_CARD,COMPANY_NAME,DELETE_FLAG,ADDRESS,CREATE_TIME)
# values(SEQ_REGIST_RECORD_INFO.Nextval,'913G'||(select to_char(sysdate,'yyyymmddhh24miss') from dual),'王刚'||SEQ_REGIST_RECORD_INFO.Nextval,'3301032020080400'||SEQ_REGIST_RECORD_INFO.Nextval,'台庆进出口有限公司'||SEQ_REGIST_RECORD_INFO.Nextval,0,'经营地址',SYSDATE)
#  '''
SQL_SEARCH_TZ = "select t.*,t.rowid from dubai_regist_record_info  t order by t.id desc"



