#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import users
from ndbclasses import *
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import cgi

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
	
# using Handler from Videolesson		
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
		user = users.get_current_user()
		# Check if User is logged in and admin
		if users.is_current_user_admin():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			user_mail = user.email()
			user_nickname = user.nickname()
			user_userid = user.user_id()
			self.render('contentform.html', editnote = [""], pagetitle = TITLE, pagesubtitle = SUBTITLE, add = 1, 
											user=user_mail, loginurl = url, linktext = url_linktext)
		else:
			self.redirect("/")	
		
	def post(self):
		user = users.get_current_user()
		# Check if User is logged in and admin
		if users.is_current_user_admin():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			user_mail = user.email()
			user_nickname = user.nickname()
			user_userid = user.user_id()
			header = cgi.escape(self.request.get("header"))
			subheader = cgi.escape(self.request.get("subheader"))
			note = self.request.get("note")
			noteindex = int(cgi.escape(self.request.get("noteindex")))
			# Using Ancestor Queries, because of their strong consistensy
			note_name = DEFAULT_NOTES
			newarticle = Article(parent=note_key(note_name))
			newarticle.header = header
			newarticle.subheader = subheader
			newarticle.noteid = noteindex
			newarticle.note = note
			newarticle.put()
						
			self.render('contentform.html', editnote = [""], pagetitle = TITLE, pagesubtitle = SUBTITLE, saved = "Saved!", 
											add = 1, user=user_mail, loginurl = url, linktext = url_linktext)
		
	
app = webapp2.WSGIApplication([
	('/addcontent', AddContentHandler),
], debug=True)		