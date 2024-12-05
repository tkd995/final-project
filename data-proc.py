import requests
import json

import spacy
nlp = spacy.load("en_core_web_lg")

from datasets import load_dataset#import from hugging face
#https://huggingface.co/datasets/npvinHnivqn/EnglishDictionary
dictionary = load_dataset("npvinHnivqn/EnglishDictionary", data_files="ee.csv")
#https://huggingface.co/datasets/fraug-library/synonyms_dictionnaries
synonyms = load_dataset("fraug-library/synonyms_dictionnaries", data_files="thesaurus_eng_US.csv")

print("Beginning word processing")
with open("dictionary.json", "w+") as f:
	ite = 0
	for i in dictionary["train"]:#iterate through dict and write to json file, information generated using spacy's NLP
		if ite%2000 == 0 and ite != 0:print(int(round(ite/len(dictionary["train"]), 2)*100))
		try:
			doc = nlp(i["word"])[0]#get various parts of speech with nlp
		except Exception:
			continue#catch None cases

		#i["lexeme"] = doc.lex
		i["lemma"] = doc.lemma_
		i["norm"] = doc.norm_
		i["pos"] = doc.pos_

		f.write(json.dumps(i)+"\n")
		ite+=1

	f.close()

with open("syns.json", "w+") as s:#iterate and write to file of synonyms
	syns = {}
	for i in synonyms["train"]:
		syns[i["word"]] = i["synonyms"]
		
	s.write(json.dumps(syns))
	s.close()

### Currently load dictionary english dict and english synonyms into maps
