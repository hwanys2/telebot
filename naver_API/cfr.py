import os
import sys
import requests
import json
from pprint import pprint

client_id = "LI0refndXUiudnjF36bN"
client_secret = "7CBFF93cq0"
# url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

files = {'image': open('/Users/jinhwan/Documents/python/naver_API/common.jpeg', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    # print (response.text)
    data = json.loads(response.text)
    pprint(data)
else:
    print("Error Code:" + rescode)