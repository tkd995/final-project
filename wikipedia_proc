from bs4 import BeautifulSoup

from libzim.reader import Archive
from libzim.search import Query, Searcher
from libzim.suggestion import SuggestionSearcher
#for wikipedia processing, training cut off june 2024
zim = Archive("wikipedia_en_all_nopic_2024-06.zim")
searcher = Searcher(zim)

import json
dictionary = open("dictionary.json", "r")
synonyms = json.load(open("syns.json", "r"))

visited = []
final_stage = open("final_stage.json", "w+")

while True:
	line = dictionary.readline()
	if line == "":break

	w = json.loads(line)
	
	#gets rid of the a and things like that
	if w["pos"] == "DET" and w["norm"] not in ["what", "where", "why", "how", "where", "which", "when"]:
		continue
	
	if w["pos"] == "NOUN" or w["pos"] == "PROPN":
		s = searcher.search(Query().set_query(w["word"])).getResults(0, 100)
		w["wiki pages"] = []
		try:
			w["synonyms"] = synonyms[w["word"]]
		except KeyError:
			w["synonyms"] = []

		print("Searching: " + w["word"])
		for page in s:
			doc = zim.get_entry_by_path(page)
			while doc.is_redirect:
				doc = doc.get_redirect_entry()

			pp = {}
			'''
			if doc.title in visited:
				break
			else:
				visited.append(doc.title)

			pp = {}
			html_page = (doc.get_item().content.tobytes()).decode()
			bs = BeautifulSoup(html_page, 'html.parser')			
			text_page = bs.get_text()
			for t in text_page:
				if t == "\n":del t
			'''
			pp["title"] = doc.title
			pp["page"] = doc.path

			w["wiki pages"].append(pp)
			final_stage.write(json.dumps(w) + "\n")
	'''else:
		tokens.append(w)'''

final_stage.close()
