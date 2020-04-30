import requests

import os, sys
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'orderly_test.settings'
import django
django.setup()
from crawler.models import Crawler


target_website = 'https://tw.yahoo.com/'
res = requests.get(target_website)
text = res.text

count = text.count('台灣')
print(count)

Crawler.objects.create(occurencies=count)