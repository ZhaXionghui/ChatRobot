from flask import Flask, request
from flask_cors import CORS
import requests
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../DataBase')))
import main as DB
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ALGO')))
from qa import token_get, ask_q, key_word, news_answer, answer1, answer2, answer 


'''
'code': 0,
'msg': '登录成功',

'code': 0,
'msg': '数据存在',

'code': 0,
'msg': '注册成功',

状态码
'code': 4000,
'msg': '用户名错误'

'code': 4001,
'msg': '密码错误'

'code': 4002,
'msg': '用户名不存在'

'code':4003,
'msg': '注册用户名已存在'

'code': 4004,
'msg': '确认密码错误'

'code': 4005,
'msg': '答案错误'

'''



app = Flask(__name__)
# 设置可以跨域访问
CORS(app, supports_credentials=True)

'''
FB/DB
登录接口
'''
# 登录接口
@app.route('/login', methods=['POST', 'GET'])
def login():
    
    '''
    DB
    TODO 后期将username,与password的参数传到数据库进行对比
    '''
    # 获取客户端发送的用户名、密码参数
    username = request.json.get('username')
    password = request.json.get('password')
    # TODO 正确做法：去数据库中查询用户名、密码是否正确
    x =DB.Judge(username,'username', 'passwd','img','id')
    print(x)
    if x['code'] == 4002:
        return x
    else:
        if x['msg'][0] == password:
            return x
        else:
            return {
            'code': 4001,
            'msg': '密码错误'
            }


'''
FB/DB
TODO 注册
'''

@app.route('/signup', methods=['POST'])
def signup():
    #首先获取用户注册时的用户名和密码，调用数据库中的Register_judge函数判断是否已经注册
    #若已被注册，返回'code': 0，'msg': '用户名已存在'；
    #若未被注册，判断密码和确认密码输入是否相同，若不相同，返回'code': 4004, 'msg': '确认密码错误'；
    #若相同，调用数据库中的InserttDB函数，将用户输入的用户名，密码，密保信息存储到数据库中
    username = request.json.get('username')
    password = request.json.get('password')
    mibao_question = request.json.get('mibao_question')
    mibao_answer = request.json.get('mibao_answer')
    img = ''

    judge_username_exist = DB.Register_judge(username, 'username')
    if judge_username_exist['code'] == 0:
        return {
            'code': 4003,
            'msg': '用户名已存在'
        }
    else:
        DB.InserttDB(username, password, img, mibao_question, mibao_answer)
        secret_information = DB.Get_security_information(username, 'username', 'mibaoQ', 'mibaoA', 'passwd', 'id')
        t_id = secret_information['msg'][3]
        return {
            'code': 0,
            'msg': {
                'msg': '注册成功',
                't_id': t_id
                }
        }


'''
FB\DB
TODO 忘记密码
'''
@app.route('/pwdforget', methods=['POST'])
def pwdforget():
    #首先查询输入的用户名是否存在,调用数据库中的Register_judge函数
    username = request.json.get('username_secret')
    mibao_answer = request.json.get('mibao_answer')
    secret_information = DB.Get_security_information(username, 'username', 'mibaoQ', 'mibaoA', 'passwd', 'id')
    mibaoQ = secret_information['msg'][0]
    mibaoA = secret_information['msg'][1]
    passwd = secret_information['msg'][2]
    t_id = secret_information['msg'][3]
    print(secret_information)
    if not mibao_answer:
            if secret_information['code'] == 4002:
                return secret_information
            if secret_information['code'] == 0:
                return {
                    'code': 0,
                    'msg': {
                        'mibao_question': mibaoQ
                    }
                }
        #用户名存在，进而查询用户的密保问题，密保信息，以及密码
        #将密保问题作为'msg'返回到前端，获取用户输入的密保答案，进行比较，若一致，返回密码；
        #若不一致，返回'code': 4005, 'msg': '答案错误'
    if mibao_answer:
        if secret_information['code'] == 0:
            if mibao_answer == mibaoA:
                return {
                    'code': 0,
                    'msg': {
                        'passwd': passwd,
                        't_id': t_id
                    }
                }
            if mibao_answer != mibaoA:
                return {
                    'code': 4005,
                    'msg': '答案错误'
                }


'''
FB
TODO 调用算法
'''
@app.route('/algo', methods=['POST'])
def algo():
    # 获取客户端数据
    question = request.json.get('message_info')
    t_id = request.json.get('t_id')
    print(question)
    with open("/root/Dev/ALGO/token.txt", "r") as f:
        token = f.read()  
    #获取关键词
    key = key_word(question)
    print(key)
    
    #return 返回答案，文字答案均为列表格式，还需进一步处理
    a = answer(x = key,question = question,token = token,t_id=t_id, s_id="", l_id=t_id)
    print(a)
    print(len(a))
    
    return {
        'code': 0,
        'msg': a
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
