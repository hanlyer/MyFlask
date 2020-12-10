# -*- coding: utf-8 -*-
# @Author  : bobo

import requests


url = 'http://192.168.181.39:5000/message/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

post_data = {
    'company_name': 'test_name',
    'company_code': '3301234567'
}

web_data = requests.post(url, headers=headers, data=post_data).text
print(web_data)
