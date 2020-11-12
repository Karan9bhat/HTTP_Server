from socket import *
from config import *
from multiprocessing import Pool
import sys, threading, time

# servername = '127.0.0.1'
# port = int(sys.argv[1])

# count = 0

# def handle_requests() :
#     global count
#     count += 1
#     r = requests.get(f'http://{servername}:{port}')
#     print(f'Response: {r.status_code}, Thread Count: {threading.active_count()}')
#     r.close()

# if __name__ == '__main__' :
#     for i in range(100) :
#         t = threading.Thread(target=handle_requests, )
#         t.start()

servername = '127.0.0.1'
port = int(sys.argv[1])

count = 0

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((servername, port))

headers = []

headers1="GET /file.html HTTP/1.1\r\n"
headers1+=f"Host: {servername}:{port}\r\n"
headers1+="Content-Type: text/html\r\n"
headers1+="User-Agent: Mozilla\r\n"
headers1+="Accept-Language: en-US\r\n"
headers1+="Accept-Encoding: */*\r\n\r\n"
headers1 = bytes(headers1, "utf-8")
message1=headers1

headers.append(message1)

headers2="GET /form.html HTTP/1.1\r\n"
headers2+=f"Host: {servername}:{port}\r\n"
headers2+="Content-Type: text/html\r\n"
headers2+="User-Agent: Mozilla\r\n"
headers2+="Accept-Language: en-US\r\n"
headers2+="Accept-Encoding: */*\r\n\r\n"
headers2 = bytes(headers2, "utf-8")
message2=headers2

headers.append(message2)

headers3="GET /image.png HTTP/1.1\r\n"
headers3+=f"Host: {servername}:{port}\r\n"
headers3+="Content-Type: image/png\r\n"
headers3+="User-Agent: Mozilla\r\n"
headers3+="Accept-Language: en-US\r\n"
headers3+="Accept-Encoding: */*\r\n\r\n"
headers3 = bytes(headers3, "utf-8")
message3=headers3

headers.append(message3)

headers4="GET /image2.jpeg HTTP/1.1\r\n"
headers4+=f"Host: {servername}:{port}\r\n"
headers4+="Content-Type: image/jpeg\r\n"
headers4+="User-Agent: Mozilla\r\n"
headers4+="Accept-Language: en-US\r\n"
headers4+="Accept-Encoding: */*\r\n\r\n"
headers4 = bytes(headers4, "utf-8")
message4=headers4

headers.append(message4)

headers5="GET /test HTTP/1.1\r\n"
headers5+=f"Host: {servername}:{port}\r\n"
headers5+="Content-Type: text/html\r\n"
headers5+="User-Agent: Mozilla\r\n"
headers5+="Accept-Language: en-US\r\n"
headers5+="Accept-Encoding: */*\r\n\r\n"
headers5 = bytes(headers5, "utf-8")
message5=headers5

headers.append(message5)

headers6="GET /put HTTP/1.1\r\n"
headers6+=f"Host: {servername}:{port}\r\n"
headers6+="Content-Type: image/png\r\n"
headers6+="User-Agent: Mozilla\r\n"
headers6+="Accept-Language: en-US\r\n"
headers6+="Accept-Encoding: */*\r\n\r\n"
headers6 = bytes(headers6, "utf-8")
message6=headers6

headers.append(message6)

body1 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n karan666bhat@gmail.com\r\n;-----------------------------133100775917425215711097468907--\r\n'

l1 = len(body1)

headers7="POST /form.html HTTP/1.1\r\n"
headers7+=f"Host: {servername}:{port}\r\n"
headers7+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers7+="User-Agent: Mozilla\r\n"
headers7+="Accept-Language: en-US\r\n"
headers7+=f"Content-Length: {l1}\r\n"
headers7+="Accept-Charset: utf-8\r\n"
headers7+="Accept-Encoding: */*\r\n\r\n"
headers7 = bytes(headers7, "utf-8")
message7 = headers7+body1

headers.append(message7)

body2 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\Karan\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nBhat\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n karan9bhat@gmail.com\r\n; \r\nContent-Type: text/html\r\n\r\n-----------------------------133100775917425215711097468907--\r\n'

l2 = len(body2)

headers8="POST /form.html HTTP/1.1\r\n"
headers8+=f"Host: {servername}:{port}\r\n"
headers8+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers8+="User-Agent: Mozilla\r\n"
headers8+="Accept-Language: en-US\r\n"
headers8+=f"Content-Length: {l2}\r\n"
headers8+="Accept-Charset: utf-8\r\n"
headers8+="Accept-Encoding: */*\r\n\r\n"
headers8 = bytes(headers8, "utf-8")
message8 = headers8+body2

headers.append(message8)

body3 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\Annie\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nBhat\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n sneha9bhat@gmail.com\r\n; \r\nContent-Type: text/html\r\n\r\n-----------------------------133100775917425215711097468907--\r\n'

l3 = len(body3)

headers9="POST /form.html HTTP/1.1\r\n"
headers9+=f"Host: {servername}:{port}\r\n"
headers9+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers9+="User-Agent: Mozilla\r\n"
headers9+="Accept-Language: en-US\r\n"
headers9+=f"Content-Length: {l3}\r\n"
headers9+="Accept-Charset: utf-8\r\n"
headers9+="Accept-Encoding: */*\r\n\r\n"
headers9 = bytes(headers9, "utf-8")
message9 = headers9+body3

headers.append(message9)

body2 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\Karan\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nBhat\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n karan9bhat@gmail.com\r\n; \r\nContent-Type: text/html\r\n\r\n-----------------------------133100775917425215711097468907--\r\n'

l2 = len(body2)

headers8="POST /form.html HTTP/1.1\r\n"
headers8+=f"Host: {servername}:{port}\r\n"
headers8+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers8+="User-Agent: Mozilla\r\n"
headers8+="Accept-Language: en-US\r\n"
headers8+=f"Content-Length: {l2}\r\n"
headers8+="Accept-Charset: utf-8\r\n"
headers8+="Accept-Encoding: */*\r\n\r\n"
headers8 = bytes(headers8, "utf-8")
message8 = headers8+body2

headers.append(message8)

body4 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\Sneha\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nBhat\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n bhat9sneha@gmail.com\r\n; \r\nContent-Type: text/html\r\n\r\n-----------------------------133100775917425215711097468907--\r\n'

l4 = len(body4)

headers10="POST /form.html HTTP/1.1\r\n"
headers10+=f"Host: {servername}:{port}\r\n"
headers10+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers10+="User-Agent: Mozilla\r\n"
headers10+="Accept-Language: en-US\r\n"
headers10+=f"Content-Length: {l4}\r\n"
headers10+="Accept-Charset: utf-8\r\n"
headers10+="Accept-Encoding: */*\r\n\r\n"
headers10 = bytes(headers10, "utf-8")
message10 = headers10+body4

headers.append(message10)

body5 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\Kartik\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nBhat\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="email"\r\n\r\n kartikbhat@gmail.com\r\n; \r\nContent-Type: text/html\r\n\r\n-----------------------------133100775917425215711097468907--\r\n'

l5 = len(body5)

headers11="POST /form.html HTTP/1.1\r\n"
headers11+=f"Host: {servername}:{port}\r\n"
headers11+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers11+="User-Agent: Mozilla\r\n"
headers11+="Accept-Language: en-US\r\n"
headers11+=f"Content-Length: {l5}\r\n"
headers11+="Accept-Charset: utf-8\r\n"
headers11+="Accept-Encoding: */*\r\n\r\n"
headers11 = bytes(headers11, "utf-8")
message11 = headers11+body5

headers.append(message11)

fd1 = open("image.png", 'rb')
d6 = fd1.read()
fd1.close()

body6 = b'-----------------------------133100775917425215711097468907\r\nname="myfile"; filename="image.png"\r\nContent-Type: image/png\r\n\r\n' + d6 + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l6 = len(body6)

headers12="POST /image.png HTTP/1.1\r\n"
headers12+=f"Host: {servername}:{port}\r\n"
headers12+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers12+="User-Agent: Mozilla\r\n"
headers12+="Accept-Language: en-US\r\n"
headers12+=f"Content-Length: {l6}\r\n"
headers12+="Accept-Charset: utf-8\r\n"
headers12+="Accept-Encoding: */*\r\n\r\n"
headers12 = bytes(headers12, "utf-8")
message12 = headers12+body6

headers.append(message12)

fd2 = open("image2.jpeg", 'rb')
d7 = fd2.read()
fd2.close()

body7 = b'-----------------------------133100775917425215711097468907\r\nname="myfile"; filename="image2.jpeg"\r\nContent-Type: image/jpeg\r\n\r\n' + d7 + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l7 = len(body7)

headers13="POST /image.png HTTP/1.1\r\n"
headers13+=f"Host: {servername}:{port}\r\n"
headers13+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers13+="User-Agent: Mozilla\r\n"
headers13+="Accept-Language: en-US\r\n"
headers13+=f"Content-Length: {l7}\r\n"
headers13+="Accept-Charset: utf-8\r\n"
headers13+="Accept-Encoding: */*\r\n\r\n"
headers13 = bytes(headers13, "utf-8")
message13 = headers13+body7

headers.append(message13)

fd3 = open("put/TMS.odt", 'rb')
body8 = fd3.read()
fd3.close()

l8 = len(body8)

headers14="PUT /put/TMS.odt HTTP/1.1\r\n"
headers14+=f"Host: {servername}:{port}\r\n"
headers14+="Content-Type: application/vnd.oasis.opendocument.document\r\n"
headers14+=f"Content-length: {l8}\r\n"
headers14+="User-Agent: Mozilla\r\n"
headers14+="Accept-Language: en-US\r\n"
headers14+="Accept-Encoding: */*\r\n\r\n"
headers14 = bytes(headers14, "utf-8")
message14=headers14+body8

headers.append(message14)

fd4 = open("put/TMS.odt", 'rb')
body9 = fd4.read()
fd4.close()

l9 = len(body9)

headers15="PUT /put/paper.pdf HTTP/1.1\r\n"
headers15+=f"Host: {servername}:{port}\r\n"
headers15+="Content-Type: application/pdf\r\n"
headers15+=f"Content-length: {l9}\r\n"
headers15+="User-Agent: Mozilla\r\n"
headers15+="Accept-Language: en-US\r\n"
headers15+="Accept-Encoding: */*\r\n\r\n"
headers15 = bytes(headers15, "utf-8")
message15=headers15+body9

headers.append(message15)

fd5 = open("image.png", 'rb')
body10 = fd5.read()
fd5.close()

l10 = len(body10)

headers16="PUT /image.png HTTP/1.1\r\n"
headers16+=f"Host: {servername}:{port}\r\n"
headers16+="Content-Type: image/png\r\n"
headers16+=f"Content-length: {l10}\r\n"
headers16+="User-Agent: Mozilla\r\n"
headers16+="Accept-Language: en-US\r\n"
headers16+="Accept-Encoding: */*\r\n\r\n"
headers16 = bytes(headers16, "utf-8")
message16=headers16+body10

headers.append(message16)

fd6 = open("image2.jpeg", 'rb')
body11 = fd6.read()
fd6.close()

l11 = len(body11)

headers17="PUT /image.png HTTP/1.1\r\n"
headers17+=f"Host: {servername}:{port}\r\n"
headers17+="Content-Type: image/png\r\n"
headers17+=f"Content-length: {l11}\r\n"
headers17+="User-Agent: Mozilla\r\n"
headers17+="Accept-Language: en-US\r\n"
headers17+="Accept-Encoding: */*\r\n\r\n"
headers17 = bytes(headers17, "utf-8")
message17=headers17+body11

headers.append(message17)

fd7 = open("testcases.txt", 'rb')
body12 = fd7.read()
fd7.close()

l12 = len(body12)

headers18="PUT /testcases/txt HTTP/1.1\r\n"
headers18+=f"Host: {servername}:{port}\r\n"
headers18+="Content-Type: text/html\r\n"
headers18+=f"Content-length: {l12}\r\n"
headers18+="User-Agent: Mozilla\r\n"
headers18+="Accept-Language: en-US\r\n"
headers18+="Accept-Encoding: */*\r\n\r\n"
headers18 = bytes(headers18, "utf-8")
message18=headers18+body12

headers.append(message18)

headers19="HEAD /post.html HTTP/1.1\r\n"
headers19+=f"Host: {servername}:{port}\r\n"
headers19+="Content-Type: text/html\r\n"
headers19+="User-Agent: Mozilla\r\n"
headers19+="Accept-Language: en-US\r\n"
headers19+="Accept-Encoding: */*\r\n\r\n"
headers19 = bytes(headers19, "utf-8")
message19=headers19

headers.append(message19)

headers20="HEAD /image.png HTTP/1.1\r\n"
headers20+=f"Host: {servername}:{port}\r\n"
headers20+="Content-Type: image/jpg\r\n"
headers20+="User-Agent: Mozilla\r\n"
headers20+="Accept-Language: en-US\r\n"
headers20+="Accept-Encoding: */*\r\n\r\n"
headers20= bytes(headers20, "utf-8")
message20=headers20

headers.append(message20)

headers21="HEAD /put/paper.pdf HTTP/1.1\r\n"
headers21+=f"Host: {servername}:{port}\r\n"
headers21+="Content-Type: application/pdf\r\n"
headers21+="User-Agent: Mozilla\r\n"
headers21+="Accept-Language: en-US\r\n"
headers21+="Accept-Encoding: */*\r\n\r\n"
headers21 = bytes(headers21, "utf-8")
message21=headers21

headers.append(message21)

headers22="HEAD /put/TMS.odt HTTP/1.1\r\n"
headers22+=f"Host: {servername}:{port}\r\n"
headers22+="Content-Type: application/vnd.oasis.opendocument.document\r\n"
headers22+="User-Agent: Mozilla\r\n"
headers22+="Accept-Language: en-US\r\n"
headers22+="Accept-Encoding: */*\r\n\r\n"
headers22 = bytes(headers22, "utf-8")
message22=headers22

headers.append(message22)

def send_request(msg) :
    global count
    servername = '127.0.0.1'
    port = int(sys.argv[1])
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((servername, port))
    count += 1
    clientsocket.send(msg)
    ans = clientsocket.recv(SIZE)
    print("Response for request from ", clientsocket)
    try :
        print(ans.decode('utf-8'))
    except :
        print(ans)
    clientsocket.close()


if __name__ == '__main__' :
    for message in headers :
        print(message)
        msg = []
        msg.append(message)
        with Pool(5) as p :
            p.map(send_request, msg)
        # t = threading.Thread(target=send_request, args=(msg))
        # t.start()