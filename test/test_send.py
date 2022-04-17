from time import sleep

import requests
import yaml
from jsonpath import jsonpath
from datetime import date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSend:
    def get_forms(self):
        url = 'https://jinshuju.net/api/v1/forms'
        headers = {
            'Authorization': 'Basic RkFUS2VqbFlwUkdSSVFfVGM3T1gwUTpZMVRLYk1uNm42S0FlckVDM1Y4b0Rn'
        }
        res = requests.get(url, headers=headers)
        name = jsonpath(res.json(), "$.data..name")
        token = jsonpath(res.json(), "$.data..token")
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d").replace("-", "")
        form_dict = dict(zip(name, token))
        s1 = {}
        for i, k in form_dict.items():
            a = str(i).split("-")[0].strip()[-8:]
            if a.isdigit() and a == yesterday:
                s1.setdefault(k, i)
                print(s1)
        return s1

    def get_cookies(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=options)
        file = open('cookies.yaml', 'w', encoding="utf-8")
        yaml.dump(driver.get_cookies(), file)
        file.close()

    def load_cookies(self):
        return yaml.safe_load(open("cookies.yaml", encoding='utf-8'))

    def get_token(self):
        ID = 'wwf911a5604c031a07'
        SECRET = '0ZKm_0el5XSXnI3EhaivnJ-fl0jno9c8FkQfs5-CR5M'
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {'corpid': ID,
                  'corpsecret': SECRET}
        res = requests.get(url, params=params)
        # print(res.json())
        access_token = res.json()["access_token"]
        return access_token

    def get_message(self):
        access_token = self.get_token()
        filename_list = []
        base_url = 'https://jinshuju.net/forms'
        data = self.get_forms()
        form_token = [i for i in data.keys()]
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome()
        driver.maximize_window()
        # driver = webdriver.Chrome(options=options)
        driver.get('https://jinshuju.net/form_folders/m1LtU8')
        for cookie in self.load_cookies():
            driver.add_cookie(cookie)

        for i in form_token:
            url = f'{base_url}/{i}/entries'
            driver.get(url)
            driver.refresh()
            driver.save_screenshot(f'{data[i]}.png')
            filename = f'{data[i]}.png'
            filename_list.append(filename)
            print(filename_list)
            if filename == filename_list[-1]:

                upload_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg'
                params = {'access_token': access_token}
                payload = {
                    "filename": filename,
                    "type": "image"
                }
                files = [('media', (filename, open(filename, 'rb'), 'image/jpeg'))]
                res = requests.post(upload_url, params=params, data=payload,files=files)
                img_url = res.json()['url']
                print(img_url)
                print(img_url)
                print(res)
                url = "http://39.102.48.202:6001/api/message/send"
                data = {
                    "url": img_url, "chatId": "613983d9321ffd4874c0218b", "robotId": "5f966ad16010f5003347f30a",
                    "type": "image"
                }
                res = requests.post(url, json=data)
                print(res)
                print(res.json())


            # filename_list.append(f'{data[i]}.png')

            form_name = driver.find_element(By.XPATH, "//h4[@class='form-name']/span").text
            ele_list = driver.find_elements(By.CSS_SELECTOR, '.w2ui-col-header ')
            n = len(ele_list)
            ele_list2 = driver.find_elements(By.XPATH, f"//td[@col='{n - 3}']")
            for ele in ele_list2:
                if len(ele.text) > 25:
                    text = f'{form_name}{ele.text}'
                    print(text)
                    url = "http://39.102.48.202:6001/api/message/send"
                    data = {
                                    "text": text,
                                    "robotId": "5f966ad16010f5003347f30a",
                                    # "group_name": "测吧助教群2022",
                                    # "group_name": "test_image",
                                    "chatId":"613983d9321ffd4874c0218b",
                                    # "type": 0,
                                    "type": "text"
                                    }
                    res = requests.post(url, json=data)
                    print(res.json())
                else:
                    pass





if __name__ == '__main__':
    TestSend().get_message()





