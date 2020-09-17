#!/user/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess
import pandas as pd
from pandas import json_normalize
import os
import io

if os.path.exists("c:/temp/embyjav/jav_final.csv"):
    os.remove("c:/temp/embyjav/jav_final.csv")
    print("jav_final.csv was deleted")
else:
    print("The file does not exist")

if os.path.exists("c:/temp/embyjav/scrap.csv"):
    os.remove("c:/temp/embyjav/scrap.csv")
    print("scrap.csv was deleted")
else:
    print("The file does not exist")

list_scrap_cmd = "gclone lsjson embyjav:scrap --dirs-only"
p = subprocess.Popen(list_scrap_cmd,
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
# To interpret as text, decode
out = stdout.decode('utf-8')
err = stderr.decode('utf-8')
dfscrap_raw = pd.read_json(out, orient='records')
dfscrap_work = dfscrap_raw.drop(['Name', 'Size', 'MimeType', 'ModTime', 'IsDir', 'ID'], axis=1)
print(dfscrap_work)
dfscrap_work.to_csv("c:/temp/embyjav/scrap.csv", index=False, encoding='utf-8-sig')
print("scrap.csv was created")


list_jav_cmd = 'Get-Content "C:\\temp\\embyjav\\scrap.csv" | Foreach-Object {Get-ChildItem -Path "I:\\Shared drives\\EMBY-JAV\\JAV_Final\\" -Directory -Recurse $_ | Select-Object -Property FullName}'
p = subprocess.Popen(['Powershell.exe', list_jav_cmd],
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
# To interpret as text, decode
out = stdout.decode()
err = stderr.decode()
print(out)
data = io.StringIO(out)
dfjav_raw = pd.read_csv(data, sep=",", encoding = 'utf8')

print(dfjav_raw)
print(dfjav_raw.columns)
dfjav_raw.columns = ['jav_final']
dfjav_work = dfjav_raw
dfjav_work.to_csv("c:/temp/embyjav/jav_final.csv", index=False, encoding='utf-8-sig')
