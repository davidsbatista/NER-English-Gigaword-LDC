#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ner
import sys
import cStringIO
import fileinput
from nltk.tokenize import sent_tokenize
from datetime import datetime
from xml.dom.minidom import parse, parseString

tagger = ner.SocketNER(host='shinra', port=9191)
punctuation = [".",",","!","?",";",":"]

def main():
    f_out_tagged = open(sys.argv[1] + '.tagged','w')
    f_out_errors = open(sys.argv[1] + '.errors','w')
    count = 0
    fi = fileinput.FileInput(sys.argv[1],openhook=fileinput.hook_encoded("UTF-8"))
    for line in fi:
        if not (line.startswith("(BEGIN OPTIONAL TRIM) ") or line.startswith("(END OPTIONAL TRIM) ") or line.startswith("(MORE)")):
            # tag text, one sentence at the time
            labeled_text =  getLabels(line)
            tagged_text = addTags(line,labeled_text,f_out_errors)

            # writes tagged content to file
            try:
                f_out_tagged.write(tagged_text+'\n')
            except Exception, e:
                f_out_errors.write(line+'\t'+"writing output"+'\t'+e.message+'\n')

            count+=1
            if (count % 500 == 0):
                f_out_tagged.flush()
                f_out_errors.flush()
                print sys.argv[1],datetime.now(),'\t',count

    f_out_tagged.close()
    f_out_errors.close()



def addTags(line,labeled_tokens,f_out_errors):

            tokens = labeled_tokens.split()
            tagged_text =  cStringIO.StringIO()
            insideLOC = False
            insidePER = False
            insideORG = False
            insideMISC = False

            for i in range(0,len(tokens)):
                t = tokens[i]
                parts = t.split("/")
                token = parts[:-1]
                label = parts[-1]
                if len(token)==1:
                    token = parts[:-1][0]
                else:
                    token = '/'.join(parts[:-1])

                if label=='O':
                    if insideLOC:
                        tagged_text.write("</LOC> ")
                        insideLOC = False
                    if insidePER:
                        tagged_text.write("</PER> ")
                        insidePER = False
                    if insideORG:
                        tagged_text.write("</ORG> ")
                        insideORG = False
                    if insideMISC:
                        tagged_text.write("</MSC> ")
                        insideMISC = False
                    tagged_text.write(token.encode("utf8")+' ')

                if label=='LOCATION':
                    if insideLOC == False:

                        if insideORG == True:
                            tagged_text.write("</ORG> ")
                            insideORG = False;
                        if insideMISC == True:
                            tagged_text.write("</MSC> ")
                            insideMISC = False;
                        if insidePER == True:
                            tagged_text.write("</PER> ")
                            insidePER = False;

                        insideLOC = True
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] != 'LOCATION':
                            tagged_text.write("<LOC>"+token.encode("utf8"))
                        else:
                            tagged_text.write("<LOC>"+token.encode("utf8")+' ')
                    else:
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] == 'O':
                            tagged_text.write(token.encode("utf8"))
                        else:
                            tagged_text.write(token.encode("utf8")+' ')


                if label=='PERSON':
                    if insidePER == False:

                        if insideORG == True:
                            tagged_text.write("</ORG> ")
                            insideORG = False;
                        if insideLOC == True:
                            tagged_text.write("</LOC> ")
                            insideLOC = False;
                        if insideMISC == True:
                            tagged_text.write("</MSC> ")
                            insideMISC = False;

                        insidePER = True
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] != 'PERSON':
                            tagged_text.write("<PER>"+token.encode("utf8"))
                        else:
                            tagged_text.write("<PER>"+token.encode("utf8")+' ')
                    else:
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] == 'O':
                            tagged_text.write(token.encode("utf8"))
                        else:
                            tagged_text.write(token.encode("utf8")+' ')

                if label=='ORGANIZATION':
                    if insideORG == False:

                        if insideMISC == True:
                            tagged_text.write("</MSC> ")
                            insideMISC = False;
                        if insideLOC == True:
                            tagged_text.write("</LOC> ")
                            insideLOC = False;
                        if insidePER == True:
                            tagged_text.write("</PER> ")
                            insidePER = False;

                        insideORG = True
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] != 'ORGANIZATION':
                            tagged_text.write("<ORG>"+token.encode("utf8"))
                        else:
                            tagged_text.write("<ORG>"+token.encode("utf8")+' ')
                    else:
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] == 'O':
                            tagged_text.write(token.encode("utf8"))
                        else:
                            tagged_text.write(token.encode("utf8")+' ')

                if label=='MISC':
                    if insideMISC == False:

                        if insideORG == True:
                            tagged_text.write("</ORG> ")
                            insideORG = False;
                        if insideLOC == True:
                            tagged_text.write("</LOC> ")
                            insideLOC = False;
                        if insidePER == True:
                            tagged_text.write("</PER> ")
                            insidePER = False;

                        insideMISC = True
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] != 'MISC':
                            tagged_text.write("<MSC>"+token.encode("utf8"))
                        else:
                            tagged_text.write("<MSC>"+token.encode("utf8")+' ')
                    else:
                        if (i<len(tokens)-1) and tokens[i+1].split("/")[-1] == 'O':
                            tagged_text.write(token.encode("utf8"))
                        else:
                            tagged_text.write(token.encode("utf8")+' ')

                i+= 1

            return tagged_text.getvalue()

        #except Exception, e:
        #    print e
        #    sys.exit(0)



def getLabels(text):
    try:
        tagged_text = tagger.tag_text(text)
        return tagged_text
    except Exception, e:
        print e


if __name__ == "__main__":
    main()
