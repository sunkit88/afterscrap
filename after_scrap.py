#!/user/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess
import pandas as pd
from pandas import json_normalize
import os
import io

# if os.path.exists("c:/temp/embyjav/jav_final.csv"):
#     os.remove("c:/temp/embyjav/jav_final.csv")
#     print("jav_final.csv was deleted")
# else:
#     print("The file does not exist")
#
# if os.path.exists("c:/temp/embyjav/scrap.csv"):
#     os.remove("c:/temp/embyjav/scrap.csv")
#     print("scrap.csv was deleted")
# else:
#     print("The file does not exist")

remove_empty_cmd = "rclone rmdirs embyjav:scrap --leave-root"
p = subprocess.Popen(remove_empty_cmd,
                     shell=True)

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
dfscrap_work = dfscrap_raw.drop(['Size', 'MimeType', 'ModTime', 'IsDir', 'ID'], axis=1)

# dfscrap_work.to_csv("c:/temp/embyjav/scrap.csv", index=False, encoding='utf-8-sig')
# print("scrap.csv was created")

list_jav_cmd = "gclone lsjson embyjav:JAV_Final --dirs-only -R"
# 'Get-Content "C:\\temp\\embyjav\\scrap.csv" | Foreach-Object {Get-ChildItem -Path "I:\\Shared drives\\EMBY-JAV\\JAV_Final\\" -Directory -Recurse $_ | Select-Object -Property FullName}'
p = subprocess.Popen(list_jav_cmd,
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
# To interpret as text, decode
out = stdout.decode('utf-8')
err = stderr.decode('utf-8')
dfjav_raw = pd.read_json(out, orient='records')
dfjav_work = dfjav_raw.drop(['Size', 'MimeType', 'ModTime', 'IsDir', 'ID'], axis=1)

# dfjav_work.to_csv("c:/temp/embyjav/jav_final.csv", index=False, encoding='utf-8-sig')

dfscrap_work = dfscrap_work.rename(columns={"Path":"scrap_path"})
dfjav_work = dfjav_work.rename(columns={"Path":"jav_path"})
# print(dfscrap_work.columns)
# print(dfjav_work.columns)

dfmove = pd.merge(dfscrap_work, dfjav_work, on="Name")

for i in dfmove.index:
    move_cmd = 'rclone move embyjav:"scrap/' + dfmove["scrap_path"][i] + '/" embyjav:"JAV_Final/' + dfmove["jav_path"][i] + '/" -P -v --delete-empty-src-dirs'
    print(move_cmd)
    subprocess.Popen(move_cmd, shell=True)

clean_empty_cmd = 'rclone rmdirs embyjav:scrap --leave-root'
subprocess.Popen(clean_empty_cmd, shell=True)



print("Completed")
