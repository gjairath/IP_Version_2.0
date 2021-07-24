# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:39:37 2021

@author: garvi
"""

# Files
from ip_app import app
from ip_app.forms import Login, Register
from ip_app.models import db, User, Project, Task
from ip_app.forms import NewProjectForm, NewTaskForm
import ip_app.uutil as uutil
#from ip_app.forgot_email import send_password_reset_email

# Packages
from flask import request, render_template, make_response, redirect, flash, url_for
from datetime import datetime as dt
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import json


# This global variable is similar to current_user, however, it tracks what the current_project_name object is.

# I have no idea whether this is a safe thing to do lol
# BUT, it's cheaper to track the name not the object.
current_project_name = None

@app.route('/')
@app.route('/dashboard')
@login_required
def index():
    '''
    Show-Dashboard, at the dasboard, login required.
    '''
    project_list = Project.query.all() or None
    return render_template('dashboard.html', user=current_user, project_list=current_user.user_projects)

@app.route("/user/<username>")
@login_required
def profile(username):
    '''
    Profile, at the dashboard as a "dropdown", login required.
    '''
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@app.route('/dummy', methods = ["GET"])
@login_required
def show_users():
    '''
    Show all users, at the dashboard, login required.
    '''
    user_list = User.query.all()
    project_list = Project.query.all() or None

    # When this html file extends my base page, the base page has a var for user that isn't importer
    return render_template("user_test.html", users = user_list, user = current_user, projects=project_list)

@app.route('/new_task', methods = ["GET", "POST"])
@login_required
def new_task():
    '''
    After you navigate into a project, the new task route.
    '''
    return redirect(url_for("index"))
    
@app.route('/new_project', methods = ["GET", "POST"])
@login_required
def new_project():
    '''
    Make a new project when the user clicks "New project" on the sliced-view plane.
    '''
    
    # The Project() table holds all the relevant cols, that can be interacted with as an OOP object.
    
    new_project_form = NewProjectForm()
    
    if (new_project_form.validate_on_submit()):
        # Grab already validated data from the form
        project_name = new_project_form.project_name.data        
        project_desc = new_project_form.project_desc.data        

        this_user_projects = current_user.user_projects
        
        for project in this_user_projects:
            if (project.project_name == project_name):
                flash ("{} Already Exists!".format(project.project_name))
                return redirect(url_for("new_project"))
        
        # Lazy-loading works I think because ...?
        from datetime import datetime
        naive_dt = datetime.now()

        
        # Make a user object to add to the DB.
        new_project = Project(project_name = project_name,
                              project_desc = project_desc,
                              num_members = 0,
                              num_tasks = 0,
                              author = current_user,
                              project_created_at = naive_dt)        
        # Add the user
        db.session.add(new_project)
        flash("{} has been created!".format(project_name))
        # Commit the changes.
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("new_project.html", form = new_project_form)




@app.route('/post-task-method', methods = ['POST'])
def get_post_javascript_data():
    '''
    This method is used to post stuff to the TASK-DB when a user adds a task.
    JS -> PYTHON -> DB.
    
    Check: dashboard_project_in.html
    '''
    task_name = request.form['task_name']
    member_name = request.form['member_name']
    eta = request.form['eta']
    
    # figure out which project to post the data too. 1:many relationship wtih project:task
    project_name = request.form['project_name']
    
    # Which project to add this task to? current_user is courtesy of flask
    desired_project_obj = uutil.find_project_obj_by_name(project_name, current_user)
    

    new_task = Task(task_name = task_name,
                          assigned_to = member_name,
                          eta = eta,
                          project_created_by = desired_project_obj)
    
    # Update the columns after a new task is created.
    update_project_columns(desired_project_obj)
    
    flash("{} has been created!".format(task_name))
    
    db.session.add(new_task)
    db.session.commit()
    
    return task_name


def update_project_columns(desired_project_obj):
    # Update Num tasks and Num members based on new task.
    desired_project_obj.num_tasks = len(desired_project_obj.project_sub_tasks)
    
    unique_member_count = set()
    
    for task in desired_project_obj.project_sub_tasks:
        unique_member_count.add(task.assigned_to)
        
    desired_project_obj.num_members = len(unique_member_count)
    
    
    
    # Take date time and update "LAST_UPDATED" on dashboard.
    from datetime import datetime
    naive_dt = datetime.now()

    desired_project_obj.project_last_changed = naive_dt
    
    return


@app.route('/dashboard/<project_name>/get-python-task-data')
def get_python_data(project_name):
    '''
    This method passes the data from DB -> PYTHON -> JS
    
    It shows previously made tasks on the DB.
    '''
    print(current_project_name)
    desired_project_obj = uutil.find_project_obj_by_name(current_project_name, current_user)
    
    all_tasks = desired_project_obj.project_sub_tasks
    task_dict = {}
    final_dict = {}
    
    for idx, tasks in enumerate(all_tasks):
        # Get data takes all the metadata and puts it into an array.f
        task_dict["task{}".format(idx + 1)] = tasks.get_data()
        
        
    final_dict["tasks"] = task_dict
    return json.dumps(final_dict)


@app.route('/delete-task-method', methods = ['POST'])
def delete_javascript_data():
    '''
    This method deletes the task upon the click of "Delete-task"
    
    Check: dashboard_project_in.html
    '''
    
    task_id = int(request.form['which_row'])
    project_name = request.form['project_name']
    
    desired_project_obj = uutil.find_project_obj_by_name(project_name, current_user)
    
    task_array = desired_project_obj.project_sub_tasks

    flash("{} has been deleted!".format(task_array[task_id].task_name))

    db.session.delete(task_array[task_id])    
    db.session.commit()

        # Update the columns after a new task is deleted.
    update_project_columns(desired_project_obj)


    # Do 2 commits because 2 > 1. 
        # Also because if you dont the DB doesnt update and the function doesnt work.
    db.session.commit()


    return "Done"


@app.route('/dashboard/<project_name>')
def show_tasks_for_project(project_name):
    '''
    Show the new plane on the dashboard once you click a project.
    
    Params:
        projectname: name of project clicked.
    '''
    # Change the global variable everytime a new project is clicked.
    global current_project_name
    current_project_name = project_name
    return render_template("dashboard_project_in.html", user=current_user, project_name=project_name)


@app.route('/dashboard/<project_name>/gridview')
def show_grid_view_tasks_for_projects(project_name):
    global current_project_name
    current_project_name = project_name
    
    current_project = uutil.find_project_obj_by_name(current_project_name, current_user)
    all_tasks = current_project.project_sub_tasks
    
    unique_member_names = dict()
    for task in all_tasks:
        unique_member_names[task.assigned_to] = task.member_exists(task.assigned_to)
        
    
    return render_template("dashboard_project_in_grid_view.html", user=current_user, project_name=project_name,
                           member_names=unique_member_names)



@app.route('/delete_project/<project_name>')
@login_required
def delete_project(project_name):
    '''
    Delete project based on project-name, since objects cant be passed back from HTML, find it with uutil.
    I regret naming it uutil this is what I get for being clever.
    
    Paramsf
        project-name: name of the project being considered for deletion, table has unique-value so just find first.
    '''
    # The template cannot return the class object it returns class <Str> instead.
    # So find the user related object first via a query.

    desired_project_obj = uutil.find_project_obj_by_name(project_name, current_user)
    
    if (desired_project_obj == None):
        return render_template('404.html'), 404
    
    #Delete all the sub-tasks.
    for tasks in desired_project_obj.project_sub_tasks:
        db.session.delete(tasks)
    
    flash("{} has been deleted".format(desired_project_obj.project_name), category="dashboard")
    db.session.delete(desired_project_obj)
    db.session.commit()
    return redirect(url_for("index"))



@app.route('/Statistics')
@login_required
def show_stat_page():
    '''
    Show the statistics page after the user clicks Statistics.
    '''
    return render_template("Statistics.html", user=current_user, project_list=current_user.user_projects)


@app.route('/get-python-project-date-data')
def get_project_date_graph():
    '''
    Get the data of Projects Vs Time created For the Statistics page.
    
    
    Project-Creation-Frequency (Y-axis)
    Project-Created-AT         (X-axis)
    '''
    
    project_list = current_user.user_projects
    
    
    final_dict = {}
    
    # I made project X at july 22, 2021. That's 1.
    # I made project Y at july 23, 2021. That's 2.
    # ....
    
    # So if 30 projects were made on July 23, show 30 = July 23 2021.    
    for idx, project in enumerate(project_list):        
        final_dict[idx] = project.project_created_at.strftime("%d %B, %Y")
            
    from collections import Counter
    res = Counter(final_dict.values())

    print (res)
    
    return json.dumps(res)


@app.route('/get-python-project-task-data')
def get_project_task_graph():
    '''    
    Pie chart of projects by the tasks there are.    
    '''
    
    project_list = current_user.user_projects
    
    
    final_dict = {}
    
    for project in project_list:        
        final_dict[project.project_name] = len(project.project_sub_tasks)
            
    
    return json.dumps(final_dict)


@app.route('/get-python-project-num-member-data')
def get_project_num_members_graph():
    '''    
    Pie chart of projects by the tasks there are.    
    '''
    
    project_list = current_user.user_projects
    
    
    final_dict = {}
    
    for project in project_list:        
        final_dict[project.project_name] = project.num_members
            
    
    return json.dumps(final_dict)

    
    
@app.before_request
def before_request():
    '''
    Tracks the last time user logged on.
    before_request is a flask thing that triggers before views. Convinent. [is that how you spell it?]
    '''
    if (current_user.is_authenticated): 
        current_user.profile_last_login = datetime.utcnow()
        db.session.commit()
        
        
    '''
    Login functionality is below, Register, Login, Logout and adminstrative tools.
    -----------------------------------------------------------------------------------------------
    -----------------------------------------------------------------------------------------------
    '''




@app.route('/register', methods=['GET', 'POST'])
def register():
    registeration_form = Register()
    if (registeration_form.validate_on_submit()):
        # Grab already validated data from the form
        user_username = registeration_form.username.data        
        existing_user = User.query.filter(User.username == user_username).first()
        
        if (existing_user is not None):
            # User already exists.
            flash("Pick another username")
            return redirect(url_for("register"))
        
        user_email = registeration_form.email.data
        
        # Make a user object to add to the DB.
        new_user = User(username = user_username, email = user_email)
        new_user.set_password(registeration_form.password.data)
        
        # Add the user
        db.session.add(new_user)
        flash("Thanks for registering {}".format(new_user.username))
        # Commit the changes.
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form = registeration_form)

@app.route('/login', methods = ["GET", "POST"])
def login():
    login_form = Login()
    if (login_form.validate_on_submit()):        
        # Grab already validated data from the form
        user_username = login_form.username.data        
        existing_user = User.query.filter(User.username == user_username).first()
        
        if (existing_user is not None): 
            user_hash = existing_user.check_password(login_form.password.data)

        if (existing_user is not None and user_hash is True):
            # User has entered decent data for once.
            login_user(existing_user, remember = login_form.remember_me.data)  
            
            # IF the user was blocked by the login.login_view = 'login' redirect to this page.
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            # Wrong data. Either user is not found or hash didn't check out.
            flash("Incorrect Username or Password")
            return redirect(url_for("login"))
            
    return render_template('login.html', title='Sign In', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/delete/<username>')
@login_required
def delete_user(username):
    '''
    Params:
        user: object from models.py for the User db.
    Desc:
        Deletes the user based on given username.
        Only accessible after login for username == "admin"
        The conditional check above is handeled by the view template.
    '''
    
    # The template cannot return the class object it returns class <Str> instead.
    # So find the user related object first via a query.

    desired_user_obj = uutil.find_user_obj_by_name(username)
    
    
    flash("{} has been deleted admin".format(desired_user_obj.username), category="dashboard")
    db.session.delete(desired_user_obj)
    db.session.commit()
    return redirect(url_for("index"))
    