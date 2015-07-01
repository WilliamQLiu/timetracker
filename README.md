__timetracker__
=========

This was my first web application, a very simple time tracker.  The goal was to allow easy access and limited modification to database tables through a web interface.

__DOCUMENTATION__

*  Using Sphinx under datasite/docs/
*  Documentation is kept as website pages (e.g. under timesheet/datasite/docs/_build/html/index.html)

__OPERATIONS NOTES__

Login info (assuming a login name of _dsadmin_)

*  Ubuntu Server Host: 10.1.1.7
*  Login Name: dsadmin
*  You can login with ssh (Mac/Linux) or PuTTY (Windows).  E.g. `$ssh dsadmin@10.1.1.7`

Start Nginx

    $sudo service nginx start

Activate VirtualEnv

    $source /opt/mha_env/bin/activate

Start Gunicorn (assuming a database named _dataentry_ and binding say 5 workers)

    $sudo service gunicorn restart
    $gunicorn dataentry.wsgi:application --bind 10.1.1.7:8000 -w 5

__PROGRAMMING NOTES__

Use with virtualenvwrapper (mha_env) - see requirements.txt for environment setup using `pip install -r requirements.txt`

Git and GitHub

Use git to update the local repository through command line.  Remember to have the correct settings in `settings.py` when on local instead of production.
    
    git init  # Initialize a local git repository
    touch .gitignore  # Add a gitignore file
    git push origin <branchname> # Push the branch to your remote repo
    
    # Add files, commit changes
    git add .  # Adds all files or specify the specific files
    git commit -m "This is a git message for the commit"  # Commit with message
    
    # Create branches, checkout branches
    git branch features  # Create a branch called features
    git checkout features  # Check out a branch named features
    git checkout master  # Check out the master branch
    
    # Merge changes back to master
    git pull # Fetch and merge changes on the remote server to your working dir
    git merge features # Merge a different branch into your active branch
    
    # Stash
    git stash  # hide your current changes on branch
    git stash pop  # get your hidden changes on branch
    
    # Issues
    git diff # View all the merge conflicts
    git reset --hard origin/master # Undo a really bad merge

__TESTING__

*  Check functional test with: `manage.py functional_tests.py`
*  Check unit test coverage with: `coverage run manage.py test`
*  Run unit test coverage report with: `coverage html --include="timesheets/*.*"` and then look under folder 'htmlcov' > 'index.html'

__DATABASE NOTES__

We are using MySQL with South for database migrations

*  For South, first initialize with: `python manage.py migrate timesheets --initial`
*  After initialization (done), update with: `python manage.py timesheets --fake`
*  How to update: `manage.py schemamigration timesheets --auto`
*  Login to MySQL on command line: `mysql -u root -p`
*  Show and Use Database (assuming name is _dataentry_):
  -  `mysql> show databases;`
  -  `mysql> use dataentry;`
  -  `mysql> show tables;`


