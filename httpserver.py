import requests
import json

import thread
import socketserver

class connhandler(socketserver.BaseRequestHandler):
	context = []#active session context
	#model = tf.keras.saving.load_model("model.keras")

	def generate_output(self):
		req = requests.post("http://localhost:11434/api/chat", data=json.dumps({"model":"llama3.2:1b", "messages":self.context, "stream":False}), stream=False, timeout=9999)#ollama request
		try:
			v = req.json()["message"]#information about who generated the text and what text
			self.context.append(v)
			print(v["content"])
		except KeyError:
			print(str(req.text))

	def handle(self):
		i = self.request.recv(4098).decode()#on request with text, pull text from HTTP req, save for context and send to LLM, send reqult
		i = i[i.rfind(":")+2:-2]
		print(i)
		if(i == "rs"):
			context = []
		else:
			self.context.append({"role":"user", "content":i})
			self.generate_output()
			self.request.send(self.context[-1]["content"].encode())
		

with socketserver.TCPServer(("", 80), connhandler) as httpd:#run HTTP server permanently, socketserver so it can multithread
	httpd.serve_forever()
