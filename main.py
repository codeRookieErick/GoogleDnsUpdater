from requests import Session, Request, get
import json
import time

class JsonConfig:

    def __getitem__(self, index):
        if index in self.data:
            return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __init__(self, name):
        self.data = {}
        self.name = name
        self.reload()

    def save(self):
        with open(self.name, 'w') as f:
            f.write(json.dumps(self.data))

    def reload(self):
        try:
            with open(self.name, 'r') as f:
                self.data = json.loads(f.read())
        except:
            pass

    def __enter__(self): 
        return self

    def __exit__(self, a, b, c):
        self.save()

#Getting ip from ipify.org
def get_ip():
    result = ''
    try:
        result = get('https://api.ipify.org').text
    except Exception as e:
        print(e)
        pass 
    return result

def update_host(user, password, hostname, myip):
    s = Session()
    res = s.post(
        'https://{0}:{1}@domains.google.com/nic/update'.format(user, password),
        headers={'User-Agent':'Chrome/41'},
        data={'hostname':hostname, 'myip':myip, 'user':user, 'password':password}       
        ).text
    return

with JsonConfig('/scripts/python/google_dns_service/config.json') as data:
    while(True):
        try:
            data.reload()
            time.sleep(15)
            currentIp = get_ip()
            if data['lastIp'] != currentIp:
                print('updating ip...')
                data['lastIp'] = currentIp
                if data['hostList'] == None:
                    data['hostList'] = []
                for i in data['hostList']:
                    res = update_host(i['user'], i['password'], i['hostname'], currentIp)
                    print(res)
                data.save()
                print('ip updated!')
        except KeyboardInterrupt as e:
            break
        except:
            continue
