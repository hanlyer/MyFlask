import cx_Oracle
from config.jdbc import DBAdict


class connOracle:
    """
    :param sql: sql语句
    :param username:
    :param password:
    :param host:
    """
    # 连接oracle数据库
    # conn = cx_Oracle.connect(username+'/'+password+'@'+host)
    #def __init__(self, username='dubai_fs', password='dubai_fs1024', host='192.168.3.55:1521/zjporttest') :
    def __init__(self, DBATYPE):
        # self.username = username
        # self.password = password
        # self.host = host
        #self.connect = cx_Oracle.connect(username+'/'+password+'@'+host)
        self.connect = cx_Oracle.connect( DBATYPE['username']+ '/' + DBATYPE['password'] + '@' + DBATYPE['host'])
        self.cursor = self.connect.cursor()  # 得到可以执行sql的光标

    def search(self,sql):
        #查询sql语句
        self.cursor.execute(sql)
        res =self.cursor.fetchone()
        return res

    def chmod(self,sql_source,sql_search):
        #插入sql语句
        try:
            self.cursor.execute(sql_source)
            self.connect.commit()
            print("执行成功")
            res = self.search(sql_search)
            print(res)
            return res

        except Exception as e:
            print("执行失败")
            print(e)
            self.connect.rollback()
            return False


    def close(self):
        self.cursor.close()
        self.connect.close()



if __name__ == '__main__':
    con = connOracle()

    con.close()

