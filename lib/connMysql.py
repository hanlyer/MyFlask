
import pymysql


class connMysql:
    def __init__(self,host='192.168.3.235', user='wtb', password='Wtb1210', database='wtb'):
        # self.host = host
        # self.user = user
        # self.password = password
        # self.database = database
        # self.charset = 'utf-8'
        self.connect = pymysql.connect(host=host,user=user,password=password,database=database,charset='utf8')
        self.cursor =self.connect.cursor()

    def chmod(self,sql_source,sql_search):
        try:
            self.cursor.execute(sql_source)
            self.connect.commit()  # 提交事务
            print("执行成功")
            res = self.search(sql_search)
            print("datas:", res)
            return res

        except Exception as e:
            self.connect.rollback()  # 异常 回滚事务
            print(e)
            print("执行失败")
            return False


    def search(self,sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
       # print(res)
        return res

    def close(self):
        self.cursor.close()
        self.connect.close()

# def connMysql():
#     # 连接mysql数据库
#     conn = pymysql.connect(host='192.168.3.235', user='wtb', password='Wtb1210', database='wtb', charset='utf8')
#     cursor = conn.cursor()  # 得到可以执行sql的光标
#     # 商户备案埋数据  sql：统一社会信用代码
#     sql = """
#        insert into enterprise_info (uniscId,legalPerson,companyName,CERTNO,companyAddr)
#        values (CONCAT('92330782JUYT86',round(round(rand(),4)*10000)),CONCAT('名测',floor(rand()*10000)),
#        CONCAT('公司名称测试',floor(rand()*10000)),CONCAT('33011020000101',round(round(rand(),4)*10000)),
#        CONCAT('公司地址测试',floor(rand()*10000)))
#     """
#
#     # 插入mysql数据库数据，并查询
#     # sql = '''
#     # insert into enterprise_info(uniscId,legalPerson,companyName,CERTNO,companyAddr)
#     # values('923111116JEKIXE820','佛彩虹111','佛山彩虹外贸公司111','110113199207220812','佛山外贸公司');
#     # '''
#
#     try:
#         cursor.execute(sql)
#         conn.commit()  # 提交事务
#         print("数据插入成功")
#     except Exception as e:
#         conn.rollback()  # 异常 回滚事务
#         print("数据插入失败")
#     # 查询刚刚插入的数据
#     #sqltest = "select t.*,t.rowid from dubai_regist_record_info  t order by t.id desc"
#     sql_select = "SELECT * from enterprise_info order by id desc"
#     cursor.execute(sql_select)
#     res = cursor.fetchone()
#     print(res)
#     print(res[0])
#
#     cursor.close()
#     conn.close()
#     return res




if __name__ == '__main__':
    connMysql()

