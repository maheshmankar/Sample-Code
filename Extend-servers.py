'''
Script to extend resources automtaically
This script will be executed every alternet day through crontab

Author - Mahesh Mankar
Date - 24/11/2016
'''
from AAA.ducttape.client import DucttapeClient
from datetime import datetime
import requests
import sys

sea_url = "http://ducttape-api.AAA.com/api/v1.0/clusters/{}/extend"
dur_url = "http://ducttape-api.AAB.com/api/v1.0/clusters/{}/extend"
OWNER_NAME = 'mmankar'
if len(sys.argv) > 1:
    OWNER_NAME = sys.argv[1]
dt_now = datetime.now()
#red_white = lambda x: Fore.RED + Back.WHITE + x + Style.RESET_ALL
def extend_id(url):
    #print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def extend(location=None):
    dt = DucttapeClient(server='ducttape-api.prod.sea1.west.isilon.com', user_agent='custom-app/42.0')
    req_url = sea_url
    LOC = 'S'
    if location is 'dur':
        dt = DucttapeClient(server='ducttape-api.prod.rdu1.west.isilon.com', user_agent='custom-app/42.0')
        req_url = dur_url
        LOC = 'D'
    vc_list = dt.get_clusters(owner=OWNER_NAME)
    for entt in vc_list:
        dtexpire = datetime.strptime(entt[u'expires'].split('T')[0], '%Y-%m-%d')
        diff_dt = dtexpire - dt_now
        str_out = "{3}:{0}:{5} {4}{1}\t{2}".format(entt[u'id'], ('['+entt[u'ips'][0]+']').ljust(14), entt[u'expires'][:10], entt[u'owner'], entt[u'type'].rjust(6), LOC)
        if entt[u'type'] == 'ONEFS':
            print str_out,
        else:
            print str_out,
        if diff_dt.days < 5:
            if extend_id(req_url.format(entt[u'id'])):
                one_cluster = dt.get_clusters(entt['id'])[0]
                one_dtexpire = one_cluster[u'expires']
                print 'EXTENDED:{}'.format(one_dtexpire[:10])
            else:
                print 'NOT EXTENDED'
        else:
            print 'NOT EXPIRING SOON'

print("-------------:"+str(dt_now)+":---------------------------")
## extend VCs from SEA
extend()
## extend VCs from DUR
extend('dur')
print("skipped")
