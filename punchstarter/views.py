from punchstarter import app, db
from punchstarter.util import allowed_file
from punchstarter.models import Member, Project, Pledge
from flask import render_template, redirect, request, flash, url_for, abort
import datetime
import os
import cloudinary.uploader


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/projects/create/', methods=['GET', 'POST'])
def create():
	if request.method == "POST":
		
		# Hardcode guest creator member for now
		guest_creator = db.session.query(Member).filter_by(id=1).one()
		now = datetime.datetime.now()

		# Upload cover image
		cover_image = request.files['cover_image']
		if cover_image and allowed_file(cover_image.filename):
			uploaded_image = cloudinary.uploader.upload(
				cover_image,
				crop = 'limit',
				width = 680,
				height = 550,
			)
			image_filename = uploaded_image["public_id"]
		else:
			flash("Invalid cover photo file")
			return redirect(url_for('create'))


		if request.form.get("funding_end_date"):
			time_end = datetime.datetime.strptime(request.form.get("funding_end_date"), "%Y-%m-%d")
		else:
			time_end = now + datetime.timedelta(days=7)

		goal_amount = request.form.get("funding_goal") or 10000

		new_project = Project(
			member_id = guest_creator.id,
			project_name = request.form.get("project_name"),
			short_description = request.form.get("short_description"),
			long_description = request.form.get("long_description"),
			goal_amount = goal_amount,
			image_filename = image_filename,
			time_created = now,
			time_start = now,
			time_end = time_end,
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

@app.route('/projects/<int:project_id>/')
def project_detail(project_id):
	project = db.session.query(Project).get(project_id)
	if project is None:
		abort(404)

	return render_template('project_detail.html', project=project)

@app.route('/projects/<int:project_id>/pledge/', methods=['GET', 'POST'])
def pledge(project_id):
	project = db.session.query(Project).get(project_id)
	if project is None:
		abort(404)

	if request.method == "POST":
		
		# Hardcode guest pledgor member for now
		guest_creator = db.session.query(Member).filter_by(id=2).one()

		amount = request.form.get("amount")
		now = datetime.datetime.now()

		new_pledge = Pledge(
			member_id = guest_creator.id,
			project_id = project.id,
			amount = amount,
			time_created = now,
		)
		db.session.add(new_pledge)
		message = "You have successfully pledged $%s to %s!" % (amount, project.project_name)
		try:
			db.session.commit()
		except Exception, e:
			db.session.rollback()
			message = "An error has occurred while pledging."
			if app.config["DEBUG"]:
				message += str(e)
			flash(message)
			return redirect(url_for('pledge'), project_id=project.id)
		else:
			flash(message)
			return redirect(url_for('project_detail', project_id=project.id))			

	elif request.method == "GET":
		return render_template('pledge.html', project=project)

@app.route('/search/')
def search():
	query = request.args.get("q") or ""
	projects = db.session.query(Project).filter(Project.project_name.like('%'+query+'%')).all()
	project_count = len(projects)

	query_text = query if query != "" else "all projects"

	return render_template('search.html', 
		query_text=query_text,
		projects=projects,
		project_count=project_count
	)	