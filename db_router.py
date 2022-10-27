import os


class Router:
	"""
	A router to control all database operations on models in the
	the project.
	"""

	def db_for_read(self, model, **hints):
		ENV = os.getenv('ENV')
		if ENV is not None and ENV != '':
			return str(os.getenv('ENV'))
		else:
			return 'default'

	def db_for_write(self, model, **hints):
		ENV = os.getenv('ENV')
		if ENV is not None and ENV != '':
			return str(os.getenv('ENV'))
		else:
			return 'default'

	# def allow_relation(self, obj1, obj2, **hints):
		# pass

	# def allow_migrate(self, db, app_label, **hints):
		
