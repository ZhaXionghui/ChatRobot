import pymssql

def InserttDB(username,passwd,img,mibaoQ,mibaoA):
    try:
        conn = pymssql.connect(host='127.0.0.1', user='SA',database='DB_0',charset='utf8', password='skSK1234')
        cursor = conn.cursor()  # 创建游标
        conn.autocommit(True)   #指令立即执行，无需等待conn.commit()
        sql = "insert into UserInfo values('{}', '{}', '{}', '{}', '{}')".format(username,passwd,img,mibaoQ,mibaoA)
        cursor.execute(sql)
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        conn.autocommit(False) #指令关闭立即执行，以后还是等待conn.commit()时再统一执行
        cursor.close()
        conn.close()

# 获取表信息的函数，最终返回为列表
def GetAllTable():
    try:
        conn = pymssql.connect(host='127.0.0.1', user='SA',database='DB_0',charset='utf8', password='skSK1234')
        cursor = conn.cursor()  # 创建游标
        conn.autocommit(True)   #指令立即执行，无需等待conn.commit()
        sql = """
        SELECT * FROM UserInfo
            """
        cursor.execute(sql)
        #用一个rs变量获取数据
        rs = cursor.fetchall()
        return rs
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        conn.autocommit(False) #指令关闭立即执行，以后还是等待conn.commit()时再统一执行
        cursor.close()
        conn.close()

def Judge(TableName, colname, recol1, recol2, recol3):
    try:
        conn = pymssql.connect(host='127.0.0.1', user='SA',database='DB_0',charset='utf8', password='skSK1234')
        cursor = conn.cursor()  # 创建游标
        conn.autocommit(True)   #指令立即执行，无需等待conn.commit()
        sql="select {},{},{} from UserInfo where {}= '{}';".format(recol1, recol2, recol3, colname, TableName)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs:
            return {
            'code': 0,
            'msg': rs
        }
        else:
            return {
            'code': 4002,
            'msg': '用户名不存在'
        }
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        conn.autocommit(False) #指令关闭立即执行，以后还是等待conn.commit()时再统一执行
        cursor.close()
        conn.close()

#判断用户名是否已被注册
def Register_judge(TableName, colname):
    try:
        conn = pymssql.connect(host='127.0.0.1', user='SA',database='DB_0',charset='utf8', password='skSK1234')
        cursor = conn.cursor()  # 创建游标
        conn.autocommit(True)   #指令立即执行，无需等待conn.commit()
        sql="select * from UserInfo where {}= '{}';".format(colname, TableName)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs:
            return {
            'code': 0,    #用户名已被注册
            'msg': rs
        }
        else:
            return {
            'code': 4002, #用户名未被注册
            'msg': '用户名不存在'
        }
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        conn.autocommit(False) #指令关闭立即执行，以后还是等待conn.commit()时再统一执行
        cursor.close()
        conn.close()

#获取密保相关信息: mibaoQ , mibaoA , passwd
def Get_security_information(TableName, colname, recol4, recol5, recol2, recol1):
    try:
        conn = pymssql.connect(host='127.0.0.1', user='SA',database='DB_0',charset='utf8', password='skSK1234')
        cursor = conn.cursor()  # 创建游标
        conn.autocommit(True)   #指令立即执行，无需等待conn.commit()
        sql="select {},{},{},{} from UserInfo where {}= '{}';".format(recol4, recol5, recol2, recol1, colname, TableName)
        # print(sql)
        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs:
            return {
            'code': 0,
            'msg': rs  #得到了 mibaoQ ,mibaoA ,passwd
        }
        else:
            return {
            'code': 4002,
            'msg': '用户名不存在'
        }
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        conn.autocommit(False) #指令关闭立即执行，以后还是等待conn.commit()时再统一执行
        cursor.close()
        conn.close()