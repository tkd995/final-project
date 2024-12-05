import tensorflow as tf
from evolutionary_keras.models import EvolModel
from evolutionary_keras.optimizers import NGA
import numpy as np

import spacy
from bs4 import BeautifulSoup
import libzim
import json

dictionary = open("dictionary.json", "r")#load processed files and wikipedia zim

zim = libzim.Archive("wikipedia_en_all_nopic_2024-06.zim")
searcher = libzim.Searcher(zim)
extracted_zim = open("extracted_zim.json","w+")

#nlp = spacy.load("en_core_web_lg")

training = []
scanned = []
ite = 0
wordlen = len(dictionary.readlines())
prev = 0
dictionary.seek(0)

for i in dictionary:
	i = json.loads(i)
	
	ite+=1
	if ite/wordlen >= prev+1:#print each ~1% progress
		prev = ite/wordlen
		print(round(ite/wordlen, 2))
	#if i["pos"] != "NOUN" and i["pos"] != "PROPN":continue

	training.append(i["word"]+":"+i["definition"])
	
	s = searcher.search(libzim.Query().set_query(i["word"])).getResults(0, 1000)#read top articles for each word, standard NLP processing
	for page in s:
		doc = zim.get_entry_by_path(page)
		while doc.is_redirect:#if reference to another page get to that one
			doc = doc.get_redirect_entry()

		html_page = (doc.get_item().content.tobytes()).decode()
		bs = BeautifulSoup(html_page, 'html.parser')#convert webpage displayed to plaintext
		
		main = bs.find_all(attrs={"class":"content"}, recursive=True)[0]
		title = main.find_all("h1", recursive=True)[0].text#title of article

		if title in scanned:continue
		print(doc.path)

		text = ""
		div = ""
		for elem in main.find_all("div"):
			div = elem
			if div.has_attr("class") and div["class"] == "mw-content-ltr":
				print("hit")
				break

		for paragraph in div.find_all("p", recursive=False):
			text += paragraph.text+"\n"#find all paragraphs in article, does cutout all tables and such

		extracted_zim.write(text+"######DELIMITER#####\n")#incase/when crashes

		training.append(text)
		scanned.append(title)

#paramaters for model
#everything south never had the chance to get tested
vocab_size = len(training)+1
embed = 128
max_seq_len = 50 #make way longer later
ltsm_units = 256

training = tf.keras.utils.pad_sequences(np.array(training), maxlen = max_seq_len)
output = np.array(training[1:])

model = EvolModel([
		tf.keras.layers.Embedding(vocab_size, embed, input_length=max_seq_len),
		tf.keras.layers.LSTM(ltsm_units),
		tf.keras.layers.Dense(output, activation="softmax")
	])

model.compile(NGA(population_size = 100, mutation_rate = .2), metrics=["accuracy"], loss="sparse_cateforical_crossentropy")
model.fit(training, output, epochs=10, batch_size=32)
model.save("test1.h5")
