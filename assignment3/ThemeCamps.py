import webapp2
from google.appengine.ext import ndb
import db_models
import json

class ThemeCamps(webapp2.RequestHandler):
	def post(self):
		"""
		Creates Theme Camp entity

		POST Body Variables:
		name - Required. Theme Camp name
		participants[] - Array of participant ids
		meals[]- Array of meals to be served
		vehicles[] - Array of vehicles the camp is responsible for
		jobs[] - tasks needing to be done at the Theme Camp during the week of Burning Man
		tents[] - tents the camp is responsible for
		location - string location of camp at burning man
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		new_themecamp = db_models.ThemeCamps()
		name = self.request.get('name', default_value=None)
		participants = self.request.get('participants[]', default_value=None)
		meals = self.request.get('meals[]', default_value=None)
		vehicles = self.request.get('vehicles[]', default_value=None)
		jobs = self.request.get('jobs[]', default_value=None)
		tents = self.request.get('tents[]', default_value=None)
		location = self.request.get('location', default_value=None)
		if name:
			new_themecamp.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid Request"
		if participants:
			for participant in participants:
				new_themecamp.participants.append(ndb.Key(db_models.Participant, int(participant)))
		if meals:
			new_themecamp.meals = meals
		for meals in new_themecamp.meals:
			print meals
		if vehicles:
			new_themecamp.tent = vehicles
		for vehicles in new_themecamp.vehicles:
			print vehicles
		if jobs:
			new_themecamp.jobs = jobs
		for jobs in new_themecamp.jobs:
			print jobs
		if tents:
			new_themecamp.tents = tents
		for tents in new_themecamp.tents:
			print tents
		if location:
			new_themecamp.location = location
			print new_themecamp.location
		key = new_themecamp.put()
		out = new_themecamp.to_dict()
		self.resopnse.write(json.dumps(out))
		return

class CampParticipants(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		if 'cid' in kwargs:
			themecamp = ndb.Key(db_models.ThemeCamps, int(kwargs['cid'])).get()
			if not themecamp:
				self.response.status = 404
				self.response.status_message = "Theme Camp Not Found"
				return
		if 'pid' in kwargs:
			participant = ndb.Key(db_models.Participant, int(kwargs['pid']))
			if not themecamp:
				self.response.status = 404
				self.response.status_message = "Participant Not Found"
				return
		if participant not in themecamp.participants:
			themecamp.participants.append(participant)
			themecamp.put()
		self.response.write(json.dumps(themecamp.to_dict()))
		return
