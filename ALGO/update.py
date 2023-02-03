import qa

if __name__ == '__main__':
    # 获取token并储存在txt文件中，定期更新
    with open(r'token.txt','a+',encoding='utf-8') as f:
     f.truncate(0)
    token=qa.token_get()
    with open("token.txt","w") as f:
     f.write(token)  

