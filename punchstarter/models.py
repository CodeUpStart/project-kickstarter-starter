from punchstarter import db

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
	time_created = db.Column(db.DateTime(timezone=True), nullable=False)
	time_start = db.Column(db.DateTime(timezone=True), nullable=False)
	time_end = db.Column(db.DateTime(timezone=True), nullable=False)
	pledges = db.relationship('Pledge', backref='project', lazy='dynamic', foreign_keys='Pledge.project_id')

class Pledge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	time_created = db.Column(db.DateTime(timezone=True), nullable=False)