from punchstarter import app, db
from punchstarter.models import Member, Project, Pledge
from flask import render_template, redirect, request, flash, url_for
import datetime


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/projects/create/', methods=['GET', 'POST'])
def create():
	if request.method == "POST":
		
		# Hardcode guest creator member
		guest_creator = db.session.query(Member).filter_by(id=1).one()
		now = datetime.datetime.now()

		new_project = Project(
			member_id = guest_creator.id,
			project_name = request.form.get("project_name"),
			short_description = request.form.get("short_description"),
			long_description = request.form.get("long_description"),
			goal_amount = request.form.get("funding_goal"),
			time_created = now,
			time_start = now,
			time_end = datetime.datetime.strptime(request.form.get("funding_end_date"), "%Y-%m-%d"),
		)
		db.session.add(new_project)
		message = "Your project has been succesfully created!"
		try:
			db.session.commit()
		except Exception, e:
			db.session.rollback()
			message = "An error has occurred while creating your project."
			if app.config["DEBUG"]:
				message += str(e)
			flash(message)
			return redirect(url_for('create'))
		else:
			flash(message)
			return redirect(url_for('project_detail', project_id=new_project.id))			

	elif request.method == "GET":
		return render_template('create.html')

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
	project = db.session.query(Project).filter_by(id=project_id).one()

	return render_template('project_detail.html', project=project)