# -*- coding: utf-8 -*-
import json
import requests


def get_wxtoken():

    """获取access_token
    corpid:企业ID
    corpsecret:应用Secret """
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    #url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN'
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
    #url = "https://qyapi.weixin.qq.com/cgi- bin/message/send?access_token=" + get_wxtoken()
    url ="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww72a181a8d48a6201&corpsecret=1wdrOcUgRiFDZcqkhkdWrtUJM8CMsUiFCVegLnFoLSQ"+ get_wxtoken()
    values = """{"touser" : "0001" , "toparty":"FreeFly",
       "msgtype":"text",
       "agentid":"1000002",
       "text":{
         "content": "%s"
       },
    "safe":"0"
    }""" % (msg)
    requests.post(url, values.encode("utf-8").decode("latin1"))

if __name__ == '__main__':
    send_msg("BaoStock微信推送测试01")