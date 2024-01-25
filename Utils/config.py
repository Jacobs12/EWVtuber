"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import os
import json
import subprocess

def path_config() -> str:
    path = 'Config/setting.txt'
    return path

def get_project_directory() -> str:
    path = path_config()
    if os.path.exists(path) is False:
        return 'Project/'
    with open(path) as f:
        content = f.read()
        f.close()
    data = json.loads(content)
    project_directory = data['project_directory']
    return project_directory

def set_project_directory(directory:str):
    path = path_config()
    data = {}
    if os.path.exists(path) is False:
        data = {}
    else:
        with open(path) as f:
            content = f.read()
        data = json.loads(content)
    data['project_directory'] = directory
    content = json.dumps(data)
    with open(path,'w') as f:
        f.write(content)
        f.close()

def get_speaker_array() -> []:
    cmd = ['edge-tts','--list']
    result = ''
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            result = result.stdout
    except FileNotFoundError:
        print('FileNotFoundError')
    except Exception:
        print('Exception')
    if result == '':
        return []
    temp_array = result.splitlines()
    original_array = []
    item = {}
    for obj in temp_array:
        if 'Name' in obj:
            item['name'] = obj.replace('Name: ','')
        if 'Gender' in obj:
            item['gender'] = obj.replace('Gender: ','')
            original_array.append(item)
            item = {}
    speaker_array = []
    for obj in original_array:
        name = obj['name']
        if 'zh-' not in name:
            continue
        speaker_array.append(obj)
    return speaker_array

def set_speaker(speaker:str):
    path = path_config()
    data = {}
    if os.path.exists(path) is False:
        data = {}
    else:
        with open(path) as f:
            content = f.read()
        data = json.loads(content)
    data['speaker'] = speaker
    content = json.dumps(data)
    with open(path, 'w') as f:
        f.write(content)
        f.close()







