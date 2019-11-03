import re
import time

import scrapy
from selenium import webdriver


class DangdangSpiderMiddleware(object):

    def process_request(self, request, spider):

        # self.driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        if re.match(r'http://product.dangdang.com/[0-9]*.html', request.url) != None:
            self.driver = webdriver.PhantomJS(
                executable_path=r'D:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            self.driver.get(request.url)
            # for x in range(1, 11):
            # i = float(x) / 10
            # js = "document.documentElement.scrollTop = document.documentElement.scrollHeight*%f"% i
            js = "window.scrollTo(0, document.body.scrollHeight)"
            self.driver.execute_script(js)
            time.sleep(1)  # 需要设置等待时间1秒，不然加载缓慢的话，不出数据
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)

        else:
            return None
