
def allowed_file(filename):
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS