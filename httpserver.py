import thread
import http, socketserver

import tensorflow as tf


class connhandler(http.server.BaseHTTPRequestHandler):
	context = []
	model = tf.keras.saving.load_model("model.keras")

	def generate_output():
		return self.model.predict(context)

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
			self.request.send(generate_output())
		

with socketserver.TCPServer(("", 888), connhandler) as httpd:
	httpd.serve_forever()
