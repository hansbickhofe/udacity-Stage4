#!/usr/bin/env python

from google.appengine.api import users
from ndbclasses import *
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
import os
import cgi
from webapp2_extras import json

#Constants for this Stage 
TITLE = 'Stage4'
SUBTITLE = '"Allow Comments on your Page"'
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'jinja2_templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATES_DIR),autoescape = True)
DEFAULT_NOTES = 'Notes'

def note_key(note_name=DEFAULT_NOTES):
	"""Constructs a Datastore key for a Note entity.

	We use note_name as the key.
	"""
	return ndb.Key('Note', note_name)
	
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)
	
	def render_str(self, template, **params):
		t = JINJA_ENVIRONMENT.get_template(template)
		return t.render(params)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class AddContentHandler(Handler):
	def get(self):
		
		self.render('addcontentform.html', pagetitle = TITLE, pagesubtitle = SUBTITLE)
		
	def post(self):
		header = cgi.escape(self.request.get("header"))
		subheader = cgi.escape(self.request.get("subheader"))
		note = cgi.escape(self.request.get("note"))
		# Using Ancestor Queries, because of their strong consistensy
		note_name = DEFAULT_NOTES
		newarticle = Article(parent=note_key(note_name))
		newarticle.header = header
		newarticle.subheader = subheader
		newarticle.note = note
		newarticle.put()
					
		self.render('addcontentform.html', pagetitle = TITLE, pagesubtitle = SUBTITLE, saved = "Saved!")
		
	
app = webapp2.WSGIApplication([
	('/addcontent', AddContentHandler),
], debug=True)		