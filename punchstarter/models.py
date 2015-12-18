from punchstarter import db, app
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
	project = db.relationship('Project', backref='creator', lazy='dynamic')
	pledges = db.relationship('Pledge', backref='member', lazy='dynamic', foreign_keys='Pledge.member_id')

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
	project_name = db.Column(db.String(64), nullable=False)
	short_description = db.Column(db.Text, nullable=False)
	long_description = db.Column(db.Text, nullable=False)
	goal_amount = db.Column(db.Integer, nullable=False)
	image_filename = db.Column(db.String(128), nullable=False)
	time_created = db.Column(db.DateTime(timezone=False), nullable=False)
	time_start = db.Column(db.DateTime(timezone=False), nullable=False)
	time_end = db.Column(db.DateTime(timezone=False), nullable=False)
	pledges = db.relationship('Pledge', backref='project', lazy='dynamic', foreign_keys='Pledge.project_id')

	@property
	def total_pledges(self):
		total_pledges = db.session.query(func.sum(Pledge.amount)).filter(Pledge.project_id==self.id).one()[0]
		if total_pledges is None:
			total_pledges = 0

		return total_pledges

	@property
	def num_pledges(self):
		return self.pledges.count()

	@property
	def num_days_left(self):
		now = datetime.datetime.now()
		num_days_left = (self.time_end - now).days

		return num_days_left

	@property
	def percentage_funded(self):
		return int(self.total_pledges  * 100 / self.goal_amount)

	@property
	def image_path(self):
	    return cloudinary.utils.cloudinary_url(self.image_filename)[0]

class Pledge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	time_created = db.Column(db.DateTime(timezone=False), nullable=False)