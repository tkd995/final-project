import requests
import json
import spacy
'''
https://www.gutenberg.org/cache/epub/29765/pg29765.txt
Webster's Unabridged Dictionary by Various
'''
nlp = spacy.load("en_core_web_lg")

from datasets import load_dataset#import above from hugging face

#https://huggingface.co/datasets/npvinHnivqn/EnglishDictionary?row=0
ds = load_dataset("npvinHnivqn/EnglishDictionary", data_files="ee.csv")

with open("dictionary.json", "w+") as f:
	ite = 0
	for i in ds["train"]:
		if ite%1000 == 0:print(ite/len(ds["train"]))
		i['similarities'] = {}
		for j in ds["train"]:#going to have to ignore the values on the diagnol
			if j["word"]:i["similarities"] = nlp(i["word"])[0].similarity(nlp(j["word"]))

		f.write(json.dumps(i, indent=4)+"\n")
		ite+=1

	f.close()

### Currently loads english dict, and pull similarity to other words from spacy(functional synonyms and antonyms)