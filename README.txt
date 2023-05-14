This file is supposed to help you with a first successful setup of the django app.


First, you need do have python installed to run the application.
https://www.python.org/downloads/


While optional, we recommend using a virtual environment to install dependencies. Install it through a packagemanager such as pip.
	
	pip install virtualenv

Setting up the project, inside the kanban directory execute the following commands:

	virtualenv env					# creating the virtual environment
	env/scripts/activate			# activating the environment
	pip install django				# installing django
	pip install -r requirements.txt	# isntalling requirements as listed in requirements.txt
	python manage.py runserver		# running the server

That's it!