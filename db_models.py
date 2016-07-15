from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model,self).to_dict()
		d['key'] = self.key.id()
		return d

class ThemeCamps(Model)
	name = ndb.StringProperty(required = True)
	participants = ndb.KeyProperty(repeated = True)
	meals = ndb.StringProperty(repeated = True)
	vehicles = ndb.StringProperty(repeated = True)
	jobs = ndb.StringProperty(repeated = True)
	tents = ndb.StringProperty(repeated = True)
	location = ndb.StringProperty(required = True)

	def to_dict(self):
		d = super(Participant,self).to_dict()
		d['participants'] = [p.id() for p in d['participants']]
		return d

class Participant(Model):
	name = ndb.StringProperty(required = True)
	email = ndb.StringProperty()
	age = ndbIntegerProperty()
	tent = ndb.StringProperty()
	vehicle = ndb.StringProperty()
	bringing = ndb.StringProperty(repeated = True)
	job = ndb.StringProperty(repeated = True)
