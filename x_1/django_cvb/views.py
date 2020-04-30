from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
import os
import random
import string
import json
import pandas as pd
import numpy as np
# Create your views here.


class Customer_View(View):
    def get(self, request, *args, **kwargs):
        """
        偵測特定目錄 (自行定義) 下是否存在一個 ilovecoffee 資料夾，若無則建立，有則略過。
        """
        try:
            os.makedirs('ilovecoffee')
            print("新建立資料夾")
        except FileExistsError:
            print('ilovecoffee已存在')
        except PermissionError:
            print('權限不足')

        self.create_csv()
        return HttpResponse('created')

    def create_csv(self, *args, **kwargs):
        """
        賦予此 CVB 一個 create_csv()，並需有一個 url pattern, 當進入 (GET) 此頁面時，會隨機寫入 500 筆客戶資料至 customers.csv
        """

        customer_list_length = 500
        name_list = ['tom', 'peter', 'hank', 'Jonothan', 'Nate',
                     'Jessica', 'Cindy', 'May', 'Alba', 'Christina']

        df = pd.DataFrame()
        
        df['customer_id'] = [name_generator()
                             for i in range(customer_list_length)]

        df['c_name'] = np.random.choice(name_list, df.shape[0])
        df['customer_name'] = df[['c_name', 'customer_id']].agg(
            '.'.join, axis=1)
        df.drop('c_name', axis=1, inplace=True)

        df['mobile'] = [mobile_generator()
                        for i in range(customer_list_length)]
        df['frequency'] = np.random.randint(0, 20, df.shape[0])

        col_names = list(df.columns)
        for col in col_names:
            df[col] = df[col].map('''"{}"'''.format)
        df.to_csv('ilovecoffee/customer_data.csv', index=False)
        

class Calculate_Csv(View):
    def get(self, request, *args, **kwargs):
        df = pd.read_csv('ilovecoffee/customer_data.csv')
        df = df.apply(lambda x:x.str.strip('"'))
        df = df.astype({'frequency': 'int32'})
        freq = df['frequency']

        ans = {
            '中位數' : '{:.5f}'.format(freq.median().item()),
            '眾數' : '{:.5f}'.format(freq.mode()[0].item()),
            '平均數' : '{:.5f}'.format(freq.mean().item()),
        }

        print(ans)
        return JsonResponse(ans, safe=False, json_dumps_params={'ensure_ascii': False})

def mobile_generator():
    '''
    回傳格式為+886 然後 9碼 的台灣電話號碼
    '''
    return '+886' + ''.join(random.sample(string.digits, 9))


def name_generator(id_length=6):
    '''
    回傳隨機客戶id 長度8, 由數字[0-9], 大寫[A-Z]，小寫[a-z]隨機組成，但開頭不可為數字
    '''
    letters = string.ascii_letters + string.digits
    return '{}{}'.format(''.join(random.sample(string.ascii_letters, 1)), ''.join(random.sample(letters, id_length)))

