import requests
from config import BASE_URL

class APIClient:
    """封装公共请求方法"""

    def __init__(self):#__init__ 是“初始化方法”，就是“这个对象被创建时，自动执行的设置程序”,每次发请求前不用手动设置这些
        self.base_url = BASE_URL
        self.session = requests.Session()  # 复用连接，提高效率

    def post(self, endpoint, **kwargs):
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, **kwargs)
    #**kwargs 是"其他所有参数"的意思，像一个万能口袋。

    def get(self, endpoint, **kwargs):
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, **kwargs)
    #self代表“这个对象自己”。
    #self.base_url = "..." 意思是“这个快递员自己记住总部的地址”。
    #没有self，分不清这个变量是属于对象的，还是只是一个临时变量。

    #def 就是“定义这个快递员能干什么事”。
    #def post(self, ...)：定义“他能发 POST 请求”这个动作。
    #def是“定义函数/方法” 的关键字。意思是：“我要定义一个动作。”在类外面叫“函数”，在类里面叫“方法”。
    #def 后面的括号里写的是“执行这个动作需要什么参数”。
    #缩进里的内容就是“这个动作具体怎么做”。