import requests
import time
from config import BASE_URL
from logger_config import log
class APIClient:
    """封装公共请求方法"""
    def __init__(self):#__init__ 是“初始化方法”，就是“这个对象被创建时，自动执行的设置程序”,每次发请求前不用手动设置这些
        self.base_url = BASE_URL
        self.session = requests.Session()  # 复用连接，提高效率

    def post(self, endpoint, **kwargs):
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        start_time=time.time()

        log.info(f"📡发送POST请求: {url}")
        log.debug(f"请求参数:{kwargs}")

        try:
            response=self.session.post(url,**kwargs)
            elapsed=time.time() - start_time
            log.info(f"✅ 响应状态码: {response.status_code}, 耗时: {elapsed:.3f}s")
            return response
        except Exception as e:
            log.error(f"❌ 请求失败: {e}")
            raise
    #**kwargs 是"其他所有参数"的意思，像一个万能口袋。

    def get(self, endpoint, **kwargs):
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        start_time=time.time()
        log.info(f"📡发送GET请求: {url}")
        log.debug(f"请求头:{kwargs.get('headers',{})}")

        try:
            response = self.session.get(url, **kwargs)
            elapsed = time.time() - start_time
            log.info(f"✅ 响应状态码: {response.status_code}, 耗时: {elapsed:.3f}s")
            return response
        except Exception as e:
            log.error(f"❌ 请求失败: {e}")
            raise