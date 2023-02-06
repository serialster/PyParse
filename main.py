# import random
import openpyxl
import pandas as pd
import time
import warnings
import bs4
# from urllib3.exceptions import InsecureRequestWarning #added
import requests

# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
warnings.simplefilter('ignore')

url = 'https://www.goszakup.gov.kz/ru/registry/rqc'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

pagenum = 1
c = 0
res_dict = {}
while True:
    response = requests.get(url+'?count_record=50&page='+str(pagenum), headers=headers, verify=False)
    pagenum += 1
    soups = bs4.BeautifulSoup(response.text, 'html.parser')
    body = soups.find_all('tbody')
    for i in body:
        body2 = i.find_all('td')
    if len(body2) > 0:
        for i2 in range(0, int(len(body2)/4)):
            res_dict[body2[i2 * 4 + 2].text] = []
            if body2[i2*4+1].find('strong').text not in res_dict[body2[i2*4+2].text]:
                res_dict[body2[i2*4+2].text] = [body2[i2*4+1].find('strong').text]
                # print(body2[i2*4+1].find('strong').text)  # название фирмы
                url2 = body2[i2*4+1].find('a').get('href')
                # time.sleep(0.3+random.randint(10,20)/100)
                time.sleep(2)
                response2 = requests.get(url2, headers=headers, verify=False)
                soups2 = bs4.BeautifulSoup(response2.text, 'html.parser')
                print(f'Parsing {c} record')
                res_dict[body2[i2*4+2].text].append(soups2.find(text='ФИО').find_next().text)  # FIO
                res_dict[body2[i2 * 4 + 2].text].append(soups2.find(text='ИИН').next_element.next_element.text)  # IIN
                res_dict[body2[i2 * 4 + 2].text].append(soups2.find(text='Тип адреса').find_next('td').find_next('td').find_next('td').text.strip())  # адрес
            c += 1
    else:
        break

print(f'Найдено {len(res_dict)} записей')
df = pd.DataFrame.from_dict(res_dict, orient='index', columns=['Наименование организации','ФИО руководителя','ИИН руководителя','Полный адрес организации'])
df.to_excel('result.xlsx')
