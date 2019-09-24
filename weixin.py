# -*- coding: utf-8 -*-
import json
import requests
import baostock as bs


def get_wxtoken():
    """获取access_token corpid:企业ID corpsecret:应用Secret """
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': 'ww72a181a8d48a6201',
              'corpsecret': '1wdrOcUgRiFDZcqkhkdWrtUJM8CMsUiFCVegLnFoLSQ',
      }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]




def send_msg(msg):
    """发送消息
    touser:账号，发送给谁，填写账号，多个人以“|”分隔 toparty:部门ID
    agentid:应用AgentId
    content:发送的具体内容
    """


    url = "https://qyapi.weixin.qq.com/cgi- bin/message/send?access_token=" + get_wxtoken()
    values = """{"touser" : "0001" , "toparty":"FreeFly",
    "msgtype":"text", "agentid":"1000002", "text":{
         "content":Hello~~ lai "%s"
       },
    "safe":"0"
     }""" % (msg)
    requests.post(url, values.encode("utf-8").decode("latin1"))
    # 每次收到实时行情后，回调此方法
def callbackFunc(ResultData):
    pufa_bank = ResultData.data["sh.600000"]
    send_msg("sh.600000 当前价格小于10了")
    if float(pufa_bank[6]) < 10.0:
      send_msg("sh.600000 当前价格小于10了")
    if __name__ == '__main__':  # 登陆
      login_result = bs.login_real_time()
      print('login respond error_code:' + login_result.error_code)
      print('login respond error_msg:' + login_result.error_msg)
    # 订阅
    rs = bs.subscribe_by_code("sh.600000", 0, callbackFunc, "",
                          "user_params")
    if rs.error_code != '0':
       print("request real time error", rs.error_msg)
    else:
         # 使主程序不再向下执行。使用time.sleep()等方法也可以
         text = input("press any key to cancel real time \r\n")
    # 取消订阅
    cancel_rs = bs.cancel_subscribe(rs.serial_id)
    # 登出
    login_result = bs.logout_real_time()

if __name__ == '__main__': # 登陆
    login_result = bs.login_real_time()
    print('login respond error_code:' + login_result.error_code) print('login respond error_msg:' + login_result.error_msg)
    # 订阅
    rs = bs.subscribe_by_code("sh.600000", 0, callbackFunc, "",
    "user_params")
    if rs.error_code != '0':
       print("request real time error", rs.error_msg)
    else:
        # 使主程序不再向下执行。使用time.sleep()等方法也可以
     text = input("press any key to cancel real time \r\n") # 取消订阅
     cancel_rs = bs.cancel_subscribe(rs.serial_id)
     # 登出
     login_result = bs.logout_real_time()