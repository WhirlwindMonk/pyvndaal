import socket
import ssl
import sys
import json

class VNDAAL:
	TCP_IP = 'api.vndb.org'
	TCP_PORT = 19535
	BUFFER_SIZE = 4096
	TIMEOUT = 15
	HOSTNAME = "api.vndb.org"
	LOGIN_MESSAGE = 'login {"protocol":1,"client":"pyvndaal_by_WhirlwindMonk","clientver":0.1}\u0004'

	def open_connection(self):
		context = ssl.create_default_context()

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(self.TIMEOUT)
		self.SSL_SOCK = context.wrap_socket(s, server_hostname=self.HOSTNAME)
		self.SSL_SOCK.connect((self.TCP_IP, self.TCP_PORT))
		cert = self.SSL_SOCK.getpeercert()
		if ssl.match_hostname(cert, self.HOSTNAME) != None:
			return "ERROR: HOSTNAME/CERTIFICATE MISMATCH"
		return "CONNECTION: SUCCESS"
		# self.SSL_SOCK.send(self.LOGIN_MESSAGE.en
	
	def login(self):
		self.SSL_SOCK.send(self.LOGIN_MESSAGE.encode())
		data1 = self.SSL_SOCK.recv(self.BUFFER_SIZE)
		if data1 != b'ok\x04':
			print(data1)
			return "ERROR: LOGIN FAILED"
		return "LOGIN: SUCCESS"
	
	def _query(self, query):
		query = query + '\u0004'
		self.SSL_SOCK.send(query.encode())
		response = ""
		while 1:
			data = self.SSL_SOCK.recv(self.BUFFER_SIZE)
			try:
				response += data.decode()
			except UnicodeDecodeError:
				print("OS error:", sys.exc_info()[0])
				self.close_connection()
				return
			except:
				print("Unexpected error:", sys.exc_info()[0])
				self.close_connection()
				return
			
			# print(response)
			if '\u0004' in response:
				break
		if "error" in response:
			print(response)
			return "ERROR00: QUERY INVALID"
		response = response[8:-1]
		return json.loads(response)
	
	def get_vn_by_id(self, id):
		query = 'get vn basic,details,anime,relations,tags,stats,screens (id = ' + str(id) + ')'
		response = self._query(query)
		if "ERROR00" in response:
			return response
		elif response['num'] == 0:
			return "ERROR: NO RESULTS FOUND"
		return VN(response['items'][0])
	
	def get_vn_by_name(self, name):
		query = 'get vn basic,details,anime,relations,tags,stats,screens (search ~ "' + name + '")'
		response = self._query(query)
		if "ERROR00" in response:
			return response
		elif response['num'] == 0:
			return "ERROR: NO RESULTS FOUND"
		# print(response)
		return VN(response['items'][0])
		
	def get_vns_by_name(self, name):
		vn_list = []
		query = 'get vn basic,details,anime,relations,tags,stats,screens (search ~ "' + name + '")'
		response = self._query(query)
		if "ERROR00" in response:
			return response
		elif response['num'] == 0:
			return "ERROR: NO RESULTS FOUND"
		for item in response['items']:
			vn_list.append(VN(item))
		return vn_list
	
	def close_connection(self):
		self.SSL_SOCK.close()
		
class VN:
	data = {}
	
	def __init__(self, response):
		self.data = dict(zip(response.keys(), response.values()))
		
	def get_vndb_link(self):
		return "https://vndb.org/v" + str(self.data['id'])