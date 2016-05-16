# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

def convert(word):
    word = word.lower()
    temp = ''
    word = word.split()
    for i in word:
        i = i.strip(string.punctuation)
        temp += i + ' '
    return temp[:-1]

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link
                 


#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word):
         self.word = convert(word)
        
    def is_word_in(self, string, word):
        string = convert(string)
        string = string.split()
        for n in string:
            if n == word:
                return True
            if n[-2:] == "'s":
                if n[:-2] == word:
                    return True
            if n[-1] == 's':
                if n[:-1] == word:
                    return True
        return False

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        self.word = convert(word)
    
    def evaluate(self, story):
        title = story.get_title()
        return self.is_word_in(title, self.word)

class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        self.word = convert(word)
    
    def evaluate(self, story):
        subj = story.get_subject()
        return self.is_word_in(subj, self.word)

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        self.word = convert(word)
        
    def evaluate(self, story):
        summary = story.get_summary()
        return self.is_word_in(summary, self.word)


class NotTrigger(Trigger):
    def __init__(self, Trigger):
        self.anti = trigger
    
    def evaluate(self, text):
        return not self.anti.evaluate(text)
    
class AndTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.t1 = Trigger1
        self.t2 = Trigger2

    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.t1 = Trigger1
        self.t2 = Trigger2

    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t1.evaluate(story)


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

##    def phrase_in_text(self, phrase, text):
##        tip = len(phrase)
##        start = 0
##        while tip <= len(text):
##            if phrase == text[start:tip]:
##                return True
##            else:
##                start += 1
##                tip += 1
##        return False

    def evaluate(self, story):
        return self.phrase in story.get_title() or \
               self.phrase in story.get_summary() or \
               self.phrase in story.get_subject()

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    filtered = []
    for s in stories:
        for t in triggerlist:
            if t.evaluate(s) is True:
                if s not in filtered:
                    filtered.append(s)
    return filtered
    

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    triggerlist = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    for l in lines:
        l = l.split()
        if l[0] == 'ADD':
            
        l[1] = l[1].title()
        
        


##import thread

##def main_thread(p):
##    # A sample trigger list - you'll replace
##    # this with something more configurable in Problem 11
##    t1 = SubjectTrigger("Obama")
##    t2 = SummaryTrigger("MIT")
##    t3 = PhraseTrigger("Supreme Court")
##    t4 = OrTrigger(t2, t3)
##    triggerlist = [t1, t4]
##    
##    # TODO: Problem 11
##    # After implementing readTriggerConfig, uncomment this line 
##    #triggerlist = readTriggerConfig("triggers.txt")
##
##    guidShown = []
##    
##    while True:
##        print "Polling..."
##
##        # Get stories from Google's Top Stories RSS news feed
##        stories = process("http://news.google.com/?output=rss")
##        # Get stories from Yahoo's Top Stories RSS news feed
##        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))
##
##        # Only select stories we're interested in
##        stories = filter_stories(stories, triggerlist)
##    
##        # Don't print a story if we have already printed it before
##        newstories = []
##        for story in stories:
##            if story.get_guid() not in guidShown:
##                newstories.append(story)
##        
##        for story in newstories:
##            guidShown.append(story.get_guid())
##            p.newWindow(story)
##
##        print "Sleeping..."
##        time.sleep(SLEEPTIME)
##
##SLEEPTIME = 60 #seconds -- how often we poll
##if __name__ == '__main__':
##    p = Popup()
##    thread.start_new_thread(main_thread, (p,))
##    p.start()
##
##
##
koalas = NewsStory(012, 'Koalas run amok!', 'koalas, carnage', 'Koalas have \
escaped from the city zoo and are terrorizing local residents.', 'blah blah blah')
koala = TitleTrigger('koala')
