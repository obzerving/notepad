from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import dropbox # Python SDK for Dropbox API v2
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import logging

import sys

SESSION_STATE = "state"
SESSION_NPNAME = "npname"

app = Flask(__name__)
ask = Ask(app, "/alexa")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# text2int published by Adnan Umer in
# http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
def text2int (textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    textnum = textnum.replace('-', ' ')
    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)
            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else:
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
    if onnumber:
        curstring += repr(result + current)
    return curstring
    
@ask.launch
def launch():
    state = 0 ## Initialize state engine
    session.attributes[SESSION_STATE] = state
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome).reprompt(reprompt)
    
@ask.intent('CatchAllIntent')
def workflow(anythinga,anythingb,anythingc,anythingd,anythinge,anythingf,anythingg,anythingh,anythingi,anythingj,anythingk,anythingl,anythingm,anythingn,anythingo):
    anything = ''
    if anythinga is not None:
        anything = anythinga
    if anythingb is not None:
        anything = anything + ' ' + anythingb
    if anythingc is not None:
        anything = anything + ' ' + anythingc
    if anythingd is not None:
        anything = anything + ' ' + anythingd
    if anythinge is not None:
        anything = anything + ' ' + anythinge
    if anythingf is not None:
        anything = anything + ' ' + anythingf
    if anythingg is not None:
        anything = anything + ' ' + anythingg
    if anythingh is not None:
        anything = anything + ' ' + anythingh
    if anythingi is not None:
        anything = anything + ' ' + anythingi
    if anythingj is not None:
        anything = anything + ' ' + anythingj
    if anythingk is not None:
        anything = anything + ' ' + anythingk
    if anythingl is not None:
        anything = anything + ' ' + anythingl
    if anythingm is not None:
        anything = anything + ' ' + anythingm
    if anythingn is not None:
        anything = anything + ' ' + anythingn
    if anythingo is not None:
        anything = anything + ' ' + anythingo
    if session.attributes[SESSION_STATE] is None:
        state = 0 # User launched us with the name of the notepad
        session.attributes[SESSION_STATE] = state
    state = session.attributes[SESSION_STATE]
    if state == 0: # get name of notepad
        session.attributes[SESSION_NPNAME] = anything.lower()
        state = 1;
        session.attributes[SESSION_STATE] = state
        prompt = render_template('askentry')
        reprompt = render_template('reaskentry')
        return question(prompt).reprompt(reprompt)
    elif state == 1: # get entry
        cvt = text2int(anything)
        npname = session.attributes[SESSION_NPNAME] + '.txt'
        dbx = dropbox.Dropbox('Your_Token_Here')
        dbx.files_download_to_file(npname, '/'+npname, None)
        f = open(npname, 'a')
        f.write(cvt)
        f.close()
        f = open(npname, 'r')
        dbx.files_upload(f.read(), '/'+npname, mode=WriteMode('overwrite'))
        f.close()
        prompt = render_template('askmore')
        reprompt = render_template('reaskmore')
        return question(prompt).reprompt(reprompt)
        
def cancel():
    ## close_user_session()
    return statement(render_template('cancel'))
    
@ask.intent('AMAZON.StopIntent')
def stop():
    ## close_user_session()
    return statement(render_template('stop'))
    
@ask.session_ended
def session_ended():
    ## close_user_session()
    return "", 200
    
if __name__ == '__main__':
    app.run(debug=True)
