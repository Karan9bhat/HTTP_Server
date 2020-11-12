from socket import *
from _thread import *
import threading
from datetime import *
import sys
import os
import time
import zlib, gzip
import mimetypes
from config import *
import base64
import logging

socket = socket(AF_INET, SOCK_STREAM)
thread_list = []
file_extensions = {'': 'text/plain', 'html': 'text/html', 'txt': 'text/plain', 'png': 'image/png', 'jpg': 'image/jpg', 'php': 'application/x-www-form-urlencoded', 'mp3': 'audio/mpeg'}
cookie_count = 0
code = 0
close = False
stop = False
restart = True
c_get = False
logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)-15s: %(filename)s: %(message)s')

def last_modified(element):
	l = time.ctime(os.path.getmtime(element)).split(' ')
	for i in l:
		if len(i) == 0:
			l.remove(i)
	l[0] = l[0] + ','
	string = (' ').join(l)
	string = 'Last-Modified: ' + string
	return string

def extension(slash) :
	ext = slash.split('.')[-1]
	if ext in file_extensions.keys() :
		return file_extensions[ext]
	else :
		return None

def getdatetime() :
	t = time.ctime().split(' ')
	# print(t)
	# print(t)
	t[1], t[2] = t[2], t[1]
	t[4], t[3] = t[3], t[4]
	t.pop(2)
	t[0] = t[0] + ','
	string = (' ').join(t)
	string += " GMT"
	# print(string)
	string = 'Date: ' + string
	return string

def month(d) :
	switch = {
		"Jan": 1,
		"Feb": 2,
		"Mar": 3,
		"Apr": 4,
		"May": 5,
		"Jun": 6,
		"Jul": 7,
		"Aug": 8,
		"Sep": 9,
		"Oct": 10,
		"Nov": 11,
		"Dec": 12
	}
	return switch.get(d, 11)

def modify(file_path, check) :
	time = check.split(' ')
	hour, minute, second = int(time[0]), int(time[1]), int(time[2])
	m = int(month(time[1]))
	modified_time = datetime.datetime(int(time[4]), m, int(time[2]), hour, minute, second)
	hsec = int(time.mktime(modified_time.timetuple()))
	fsec = int(os.path.getmtime(file_path))
	if hsec == fsec :
		return True
	else :
		return False

def error_message(code):
	query = status_code(code)

	response=""
	response+="<html>\n"
	response+="<head><title>"+query[13:]+"</title></head>\n"
	response+="<body>\n"
	response+="<h1>"+query[9:]+"</h1>\n"

	if code==304:
		response+="<p>The entity was not modified on the server.</p>\n"
	elif code==400:
		response+="<p>The server was unable to understand your request.</p>\n"
	elif code==405:
		response+="<p>The server was unable to solve your query due to unfamilier method.</p>\n"
	elif code==500:
		response+="<p>Some internal server error occured.</p>\n"
	elif code==415:
		response+="<p>The entity had Unsupported Media Type not available on server.</p>\n"
	elif code==404:
		response+="<p>The requested entity is not available.</p>\n"
	elif code==505:
		response+="<p>The HTTP version is not supported by the server.</p>\n"

	response+="</body>\n"
	response+="</html>"

	return response

#returns the proper status code
def status_code(code):
	if code==200:
		return "HTTP/1.1 200 OK"
	elif code==201:
		return "HTTP/1.1 201 Created"
	elif code==202:
		return "HTTP/1.1 202 Accepted"
	elif code==204:
		return "HTTP/1.1 204 No Content"
	elif code==304:
		return "HTTP/1.1 304 Not Modified"
	elif code==400:
		return "HTTP/1.1 400 Bad Request"
	elif code==405:
		return "HTTP/1.1 405 Method Not Allowed"
	elif code==404:
		return "HTTP/1.1 404 Not Found"
	elif code==403:
		return "HTTP/1.1 403 Forbidden"
	elif code==415:
		return "HTTP/1.1 415 Unsupported Media Type"
	elif code==505:
		return "HTTP/1.1 505 HTTP Version Not Supported"
	else:
		return "HTTP/1.1 500 Internal Server Error"

def delete(conn, path, header_list, request_data) :
	global code
	response = ""
	#print(header_list)
	for line in header_list :
		check = line.split(": ")[0]
		#print(check)
		if "Authorization" == check :
			string = line.split(": ")[1]
			string = string.split(' ')
			string = base64.decodebytes(string[1].encode())
			string = string.decode()
			string = string.split(":")
			#print(string[0], string[1])
			if string[0] == USERNAME and string[1] == PASSWORD :
				break
			else :
				code = 401
				response += "HTTP/1.1 401 Unauthorized\n"
				response += "WWW-Authenticate: Basic"
				response += "\r\n\r\n"
				conn.send(response.encode())
				conn.close()
				return
		else :
			code = 401
			response += "HTTP/1.1 401 Unauthorized\n"
			response += "WWW-Authenticate: Basic"
			response += "\r\n\r\n"
			conn.send(response.encode())
			conn.close()
			return
	path = os.getcwd() + path
	if os.path.exists(path) :
		if os.path.isfile(path) :
			code = 200
			os.remove(path)
			response += "HTTP/1.1 200 OK\n"
			response += "Server: 127.0.0.1\n"
			response += "Connection: keep-alive\n"
			response += getdatetime()
			response += "\r\n\r\n"
			# print(response)
			conn.send(response.encode('utf-8'))
			conn.close()
			return
		else :
			code = 403
	else :
		code = 400
	response += error_message(code) + "\n"
	response += "Server: 127.0.0.1\n"
	response += "Connection: keep-alive\n"
	response += getdatetime()
	response += "\r\n\r\n"
	# print(response)
	conn.send(response.encode('utf-8'))
	conn.close()

def put(conn, path, header_list, request_data) :
	global code
	data = b''
	response = ""
	newpath = os.getcwd() + path
	isfile = os.path.exists(newpath)
	#isdir = os.path.exists(newpath)
	# print(isfile)
	# print(isdir)
	for line in header_list :
		if line.split(': ')[0] == "Content-Length" :
			length = int(line.split(': ')[1])
	try :
		data += request_data
	except TypeError :
		request_data = bytes(request_data, 'utf-8')
		data += request_data
	recv_size = len(request_data)
	left_size = length - recv_size
	# print(recv_size)
	# print(left_size)
	while left_size > 0 :
		request_data = conn.recv(10000)
		try :
			data += request_data
		except TypeError :
			request_data = bytes(request_data, 'utf-8')
			data += request_data
		left_size -= len(request_data)
		# print(data, left_size)
		# print(len(request_data))
		# print('\n')
	if isfile :
		if os.access(newpath, os.W_OK) :
			# print(newpath)
			f = open(newpath, "wb")
			f.write(data)
			f.close()
		else :
			code = 403
	else :
		pass
	code = 204
	response += 'HTTP/1.1 204 No Content\n'
	response += 'Location: ' + path + '\n'
	response += 'Connection: keep-alive\r\n\r\n'
	# print(response)
	conn.send(response.encode('utf-8'))
	conn.close()

def post(conn, path, header_list, request_data) :
	global code
	msg = ""
	back = ""
	data = ""
	m = ""
	if os.access(LOG, os.W_OK) :
		pass
	else :
		code = 403
	# print(header_list)
	# print(request_data)
	if len(request_data) >= 1 :
		for line in request_data :
			data = str(line)
		d = data.split('&')
		#print(d)
		for i in d :
			if len(i.split('=')) > 1 :
				name = i.split('=')[0]
				value = i.split('=')[1]
				v = value.split('+')
				if len(v) > 1 :
					for p in v :
						m += p + ' '
					back += name + ": " + m + '\n'
				else :
					back += name + ": " + value + '\n'
			else :
				pass
			#print(back)
	# print(msg)
	if os.access(POST_RESPONSE, os.W_OK) :
		pass
		code = 200
	else :
		code = 403
	if os.path.exists(DATA) :
		f = open(DATA, "a")
		msg += status_code(code) + "\n"
		f.write(str(back) + '\n')
	else :
		f = open(DATA, "w")
		code = 201
		msg += status_code(code) + "\n"
		msg += "Location: " + str(DATA) + "\n"
		f.write(str(back) + '\n')
	f.close()
	# print(msg)
	msg += "Server: 127.0.0.1\n"
	msg += getdatetime() + '\n'
	ff = open(POST_RESPONSE, "rb")
	msg += "Content-language: en-US,en\n"
	msg += "Content-Length: " + str(sys.getsizeof(ff)) + '\n'
	msg += "Content-Type: text/html\n"
	msg += last_modified(POST_RESPONSE) +'\n'
	msg += "\r\n\r\n"
	conn.send(msg.encode())
	conn.sendfile(ff)
	conn.close()

def get(conn, method, path, header_list) :
	global cookie_count, c_get
	response_list = []
	headers = ''
	isdir = 0
	isfile = 0
	code = 200
	file_path = os.getcwd() + path
	if os.path.exists(file_path) :
		if os.path.isfile(file_path) :
			if os.access(file_path, os.R_OK) and os.access(file_path, os.W_OK) :
				f = open(file_path, "rb")
				#content_length = sys.getsizeof(file_path)
				data = f.read()
				f.close()
				isfile = 1
			else :
				code = 403
		elif os.path.isdir(file_path) :
			dir_list = os.listdir(file_path)
			isdir = 1
		else :
			code = 415
	else :
		code = 404
	#print(header_list)
	response_list.append(COOKIE + str(cookie_count) + MAXAGE + '\n')
	cookie_count += 1
	for line in header_list :
		check = line.split(': ')[0]
		#print(check)
		if check == "Host" :
			pass
		elif check == "User-Agent" :
			string = getdatetime() + '\n'
			response_list.append(string)
			s = "User-Agent: " + line.split(": ")[1] + '\n'
			response_list.append(s)
			#print(string)
			#print(s)
		elif check == "Accept" and len(check) == 6 :
			string = ""
			print(1)
			if isdir == 1 :
				string = "Content-Type: text/html" + '\n'
				response_list.append(string)
			elif isfile == 1 :
				file_ext = extension(path)
				if file_ext == None :
				    string = "Content-Type: text/plain" + '\n'
				    response_list.append(string)
				elif file_ext in file_extensions.keys() :
				    string = "Content-Type: " + str(file_extensions[file_ext]) + '\n'
				    response_list.append(string)
				#  print(5000)
				#ext = mimetypes.MimeTypes().guess_type(file_path)[0]
				#string = "Content-Type: " + str(ext)
			#response_list.append(string)
		elif check == "Accept-Language" and len(check) == 15 :
			string = "Content-Language: " + line.split(': ')[1] + '\n'
			response_list.append(string)
		elif check == "Accept-Encoding" :
			q = 0
			# string = ''
			# string = "Content-Encoding: " + line.split(': ')[1]
			# response_list.append(string)
			if isfile == 1 :
				encoding = line.split(': ')[1]
				a = '='
				for a in encoding :
					q += 1
				#print("1", encoding)
				q = 0
				try :
					equal = encoding.split("q")
					q = len(equal) - 1
					# print(equal, q)
				except :
					q = 0
				if q == 0 :
					# if len(encoding) == 0 :
					#     string += "Content-Encoding: identity"
					# else :
					#     data = gzip.decompress(data)
					#     string += "Content-Encoding: " + encoding
					# print(10000, encoding)
					string += "Content-Encoding: identity" + '\n'
					response_list.append(string)
				else :
					m = -1
					qline = encoding.split(', ')
					# print(qline)
					for l in qline :
						q_val = int(l.split('=')[1])
						# print(q_val, l)
						if q_val > m :
							encode = l.split(';')[0]
							m = q_val
							#print(encode, m)
					string += "Content-Encoding: " + encode + '\n'
					response_list.append(string)
			# print(string)
		elif check == "If-Modified-Since" :
			string = ''
			if code == 200 :
				if modify(file_path, check) :
					string = "Last Modified: " + last_modified(file_path) + '\n'
					c_get = modify(file_path, check)
					# print(c_get)
					response_list.append(string)
				else :
					code = 304
			#response_list.append(string)
		elif check == 'Cookie' :
			cookie_count -= 1
			response_list.remove(COOKIE + str(cookie_count) + MAXAGE + '\n')
		else :
			pass
	headers = status_code(code) + '\r\n'
	if code == 200 :
		if isdir == 1 :
			data = "<html>\n"
			data += "<head><title>Successful</title></head>\n"
			data += "<body>The following directory has:\n<ul>\n"
			for d in dir_list :
				link = "http://127.0.0.1:" + str(port) + file_path + "/" + d
				data += '<li><a href="' + link + '">' + d + '</a></li>'
			data += "</ul></body></html>"
			data = bytes(data, 'utf-8')
		elif isfile == 1 :
			pass
	else :
		data = bytes(error_message(code), 'utf-8')
	#headers += error
	for line in response_list :
		#print(line)
		headers += line
	#headers += error + '\n'
	headers += '\r\n'
	# print(c_get)
	# print(headers)
	if isdir == 1 and method == 'GET' :
		headers = bytes(headers, 'utf-8')
		headers += data
		#print(headers)
		conn.send(headers)
		conn.close()
	elif isfile == 1 and c_get == False and method == "HEAD" :
		headers = bytes(headers, 'utf-8')
		# print(headers)
		conn.send(headers)
		conn.close()
	elif isfile == 1 and c_get == False and method == "GET" :
		headers = bytes(headers, 'utf-8')
		headers += data
		#print(headers)
		conn.send(headers)
		conn.close()
	elif isfile == 1 and c_get == True and (method == "GET" or method == "HEAD") :
		code = 304
		data = bytes(error_message(304), 'utf-8')
		conn.send(data)
		conn.close()

def client(conn, addr) :
	global close, restart, stop, code, thread_list, socket
	while restart and (not close) and (not stop) :
		msg = conn.recv(SIZE)
		try :
			msg = msg.decode('utf-8')
			request = msg.split('\r\n\r\n')
		except UnicodeDecodeError :
			request = msg.split(b'\r\n\r\n')
			request[0] = request[0].decode(errors = 'ignore')
		# print(msg)
		request_data = []
		header_list = request[0].split('\r\n')
		method = header_list[0].split()[0]
		path = header_list[0].split()[1]
		version = header_list[0].split()[2]
		#print(request[1])
		if method == "PUT" :
			request_data = request[-1]
		else :
			for i in range(1, len(request)) :
				try :
					request_data.append(request[i].split('\n')[0])
				except TypeError :
					pass
				# print(request_data)
		if version == 'HTTP/1.1' :
			header_list.pop(0)
			if path != '' :
				if method == 'GET' or method == 'HEAD' :
					get(conn, method, path, header_list)
				elif method == 'POST' :
					post(conn, path, header_list, request_data)
				elif method == 'PUT' :
					put(conn, path, header_list, request[-1])
				elif method == 'DELETE' :
					delete(conn, path, header_list, request_data)
			# f = open(LOG, "a")
			# string = getdatetime() + '	server:{}	port:{}	socket:{}	filepath:{}	status-code:{}\n'.format(addr[0], addr[1], conn, path, code)
			# print(string)
			# f.write(str(string))
			# f.close()
			logging.info('	server: {}	port: {}	socket: {}	filepath: {}	status-code: {}\r\n'.format(addr[0], addr[1], conn, path, code))
	if close :
		print(thread_list)
		thread_list.remove(conn)
		conn.close()

def manage() :
	global close, stop, restart
	while True :
		string = str(input())
		if string == 'stop' :
			stop = True
		elif string == 'restart' :
			restart = True
			stop = False
		elif string == 'close' :
			close = True
			stop = False
			restart = True


if __name__ == '__main__' :
	port = int(sys.argv[1])
	socket.bind(('', port))
	socket.listen(40)
	print("HTTP server started")
	start_new_thread(manage, ())
	while not close :
		while not stop :
			if close :
				break
			else :
				connection, address = socket.accept()
				thread_list.append(connection)
				if len(thread_list) < MAX_REQUEST :
					start_new_thread(client, (connection, address))
				else :
					code = 503
					connection.close()
	#connection.close()
	socket.close()
	sys.exit()
	#client(connection, address)
