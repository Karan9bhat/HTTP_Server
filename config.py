import os

SIZE = 10000

ROOT = os.getcwd()

MAX_REQUEST = 100

LOG = ROOT + '/server_log.txt'

POST_RESPONSE = os.getcwd() + '/post.html'

if os.path.exists(POST_RESPONSE) :
    pass
else :
    f = open(POST_RESPONSE, 'w')
    data = '<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charset="utf-8"><title>response</title></head><body><h1>RECORD SAVED</h1></body></html>'
    f.write(data)
    f.close()

DATA = ROOT + '/logfile.txt'
f = open(DATA, "a")
f.close()

USERNAME = 'karan123'

PASSWORD = 'Karan@123'

COOKIE = 'Set-Cookie: id='
MAXAGE = '; max-age=1000'