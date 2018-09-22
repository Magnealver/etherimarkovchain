import sys
import tkinter as tk
import praw
import markovify
import re
import spacy
import random
import os
from tkinter import *

nlp = spacy.load('en')


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class ExampleApp(tk.Tk):
    

    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top")
        self.winfo_toplevel().title("Etheri Markov Chain")
        
        b1 = tk.Button(self, text="Load Comments (slow)", command=self.fetchComments)
        b2 = tk.Button(self, text="Create Sentences", command=self.etheriSentences)
        b1.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="right")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="bottom", fill="x", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")
        

        #sys.stdout = TextRedirector(self.text, "stdout")
        #sys.stderr = TextRedirector(self.text, "stderr")



    def fetchComments(self):
        reddit = praw.Reddit(client_id='NVPJ4GAF_8dLhA',
                             client_secret='pQ5aVOkmM-j2eFTQoBKz84da61g',
                             user_agent='a cute bot',
                             username='magnosian',
                             password='QxNNG7LvsiI4')

        with open('comments.txt', 'w') as etheritext:
            for comment in reddit.redditor('etheri').comments.new(limit=None):
                noquote = re.split('(>[^\n\r]*)|([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})', comment.body)
                etheritext.write(noquote[0])

    def etheriSentences(self):
        with open('comments.txt') as sourcetext:
            text = sourcetext.read()
            text_model = markovify.Text(text)
            
        
        
            
        for i in range(1):
            self.text.delete(1.0, END)
            self.text.configure(font=("Verdana", 12))
            self.text.insert(END,text_model.make_sentence()+'\n-Etheri')

#class TextRedirector(object):
#    def __init__(self, widget, tag="stdout"):
#        self.widget = widget
#        self.tag = tag

#    def write(self, str):
#        self.widget.configure(font=("Verdana", 12), state="normal")
#        self.widget.insert("end", str, (self.tag,))
#        self.widget.configure(state="disabled")

app = ExampleApp()
app.mainloop()
