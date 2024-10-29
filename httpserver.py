import thread
import http, socketserver

class connhandler(http.server.BaseHTTPRequestHandler):
	context = []

	def pull_data(self, start):
		data = ""
		while True:
			t = self.request.readline()

			if data == "":
				self.context.append(data)
				break
			else:
				data+=t

	def do_GET(self):
		i = self.request.recv(1024)
		if(i == "rs"):
			context = []
		else:
			pull_data(i)
			self.request.send(generate_output(context[-1]))
		

with socketserver.TCPServer(("", 888), connhandler) as httpd:
	httpd.serve_forever()
