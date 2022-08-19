import requests
import json
import os
import threading

repo_name = 'Multi-Agent-Transformer-4643'

class DownloadThread(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        file = parent_folder + self.path
        filename = file.split('/')[-1]
        folders = file[:-len(filename)]
        print(folders)
        os.makedirs(folders, exist_ok=True)
        res = requests.get(file_base_url + self.path, verify=False)
        with open(file, 'wb') as f:
            f.write(res.content)

def is_file(child):
    return 'size' in child

url = 'https://anonymous.4open.science/api/repo/'+repo_name+'/files/'

r = requests.get(url)

files = json.loads(r.text)
# print(files)
cur = files
parent_folder = repo_name
file_base_url = 'https://anonymous.4open.science/api/repo/'+repo_name+'/file'
threads = []

def get_files(cur, path):
    if is_file(cur):
        t = DownloadThread(path)
        t.start()
        threads.append(t)

    else:
        for child, v in cur.items():
            get_files(v, path + '/' + child)

get_files(files, '')

for tt in threads:
    tt.join()