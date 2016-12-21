# NER-English-Gigaword-LDC
Python scripts to parse the Gigaword collection and perform NER tagging with StanfordNER

- Run the [parse-gigaword-sgml.py](parse-gigaword-sgml.py) to transform a document from the Gigaword-LDC collection into text
- Download [StanfordNER](http://nlp.stanford.edu/software/CRF-NER.shtml)
- Run it on server mode as show in [start-server.sh](start-server.sh)
- Use the [ner-tag.py](ner-tag.py) to add named-entities tags (i.e., ORG, LOC, PER) the transformed document 
