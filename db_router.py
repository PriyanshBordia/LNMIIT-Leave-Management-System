import os

class Router:
	"""
	A router to control all database operations on models in the
	the project.
	"""

	def db_for_read(self, model, **hints):
		return str(os.getenv('ENV'))

	def db_for_write(self, model, **hints):
		return str(os.getenv('ENV'))
