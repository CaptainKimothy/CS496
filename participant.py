import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Participant(webapp2.RequestHandler):
	def post(self):
			""" Creates Participant entity

			POST Body Variables:
			name - Required
			email - email
			age - not required
			tent - what tent they'll sleep in
			vehicle - which vehicle they'll ride in
			bringing - what items they will bring
			job - what their responsibilites will be
			"""

			if 'application/json' not in self.request.accept:
				self.resonse.status = 406
				self.response.status_message = "API only supports JSON"
				return

			new_participant = db_models.Participant()
			name = self.request.get('name', default_value=None)
			email = self.request.get('email', default_value=None)
			age = self.request.get('age', default_value=None)
			tent = self.request.get('tent', default_value=None)
			vehicle = self.request.get('vehicle', default_value=None)
			bringing = self.request.get('bringing', default_value=None)
			job = self.request.get('job', default_value=None)

			if name:
				new_participant.name = name
			else:
				self.response.status = 400
				self.response.status_message = "Invalid Request"
			if email:
				new_participant.email = email
			if age:
				new_participant.age = age
			if tent:
				new_participant.tent = tent
			if vehicle:
				new_participant.vehicle = vehicle
			if bringing:
				new_participant.bringing = bringing
			if job:
				new_participant.job = job
			key = new_participant.put()
			out = new_participant.to_dict()
			self.response.write(json.dumps(out))
			return

	def get(self, **kwargs):
			if 'application/json' not in self.request.accept:
				self.resonse.status = 406
				self.response.status_message = "API only supports JSON"
				return
			if 'id' in kwargs:
				out = ndb.Key(db_models.Participant, int(kwargs['id'])).get().to_dict()
				self.response.write(json.dumps(out))
			else:
				q = db_models.Participant.query()
				keys = q.fetch(keys_only=True)
				results = { 'keys' : [x.id() for x in keys]}
				self.response.write(json.dumps(results))

class ParticipantSearch(webapp2.RequestHandler):
	def post(self):
		"""
		Search for participants

		POST Body Variables:
		name - String. Full name
		email - String. 
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		q = db_models.Participant.query()
		if self.request.get('name',None):
			q = q.filter(db_models.Participant.name == self.request.get('name'))
		if self.request.get('email',None):
			q = q.filter(db_models.Participant.email == self.request.get('email'))
		keys = q.fetch(keys_only=True)
		results = {'keys' : [x.id() for x in keys]}
		self.response.write(json.dumps(results))
