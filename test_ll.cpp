#include <nlohmann/json.hpp>
#include <d99kris/spacy-cpp>

#include <zim/file.h>
#include <zim/fileiterator.h>

#include <string>
#include <vector>
#include <unordered_map>

#include <iostream>
#include <fstream>

using namespace std;

void connect_words_def(unordered_map<string, vector<*string>> &connections, auto doc){

	for(auto token: doc){
		if(token.pos_ == "DET" || token.pos_ == "ADP" || token.pos_ == "AUX" || token.pos_ == "CCONJ" || token.pos_ == "PART" || token.pos_ == "SCONJ" || token.pos_ == "X" || token.pos_ == "SYM" || token.pos_ == "PUNCT"){
			continue;
		}
		for(auto t: doc){
			if(t.text != token.text && !(t.pos_ == "DET" || t.pos_ == "ADP" || t.pos_ == "AUX" || t.pos_ == "CCONJ" || t.pos_ == "PART" || t.pos_ == "SCONJ" || t.pos_ == "X" || t.pos_ == "SYM" || t.pos_ == "PUNCT")){
				connections[token.text].pushback(*t);
			}
		}

	}

	return;
}

void connect_documents(unordered_map<string, vector<*string>> &connections, auto doc){
	string title = doc.getTitle();
	string article = std::string(blob.data(), blob.size());
	zim::Blob blob = doc.getData();

	do{

		string line = article.substr(article.find('\t'),article.find('\n'));
		connections[title].pushback(*line);

		auto doc = nlp(line);
		for(auto sent : doc.sents){
			connections[line].pushback(*sent.text);
			connect_words_def(connections, sent.text);
		}

	}while(article.find('\n') != article.end());

	if(token.pos_ == "DET" || token.pos_ == "ADP" || token.pos_ == "AUX" || token.pos_ == "CCONJ" || token.pos_ == "PART" || token.pos_ == "SCONJ" || token.pos_ == "X" || token.pos_ == "SYM" || token.pos_ == "PUNCT"){

	}
}

int main(){
	Spacy::Spacy spacy;
	spacy.prefer_gpu();
	auto nlp = spacy.load("en_core_web_lg");

	string line;
	fstream file("");

	vector<string> words;
	unordered_map<string, vector<*string>> connections;

	while(getline(file, line)){
		auto json = nlohmann::json::parse(line);

		words.pushback(json["word"]);
	}

	file.clear();
	file.seekg(0);

	while(getline(file, line)){
		auto json = nlohmann::json::parse(line);
		string word = json["word"];

		if(json["def"].find(";") != json["def"].end()){
			string s = json["def"]
			do{
				auto doc = nlp.parse(s.substr(0, s.find(";")));
				connect_words_def(connections, doc);

				s = s.substr(s.find(";"), s.end());
			}while(s.find(";") != s.end())
		}
		else{
			auto doc = nlp.parse(json["def"]);
			connect_words_def(connections, doc);
		}
	}

	zim::File wikipedia(".zim");
	for(zim::File::const_iterator it = wikipedia.begin(); it != wikipedia.end(); ++it){
		connect_documents(connections, it);
	}

	return 0;
}
