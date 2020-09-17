'''
Created on May 30, 2019

@author: Conor Murphy
'''
import json
from flask import (render_template, request, flash, redirect)
from app import application
from app.forms import LoginForm, FilterDataForm, FavoritesForm
import runpy
from datetime import datetime
from user import User
import ast
import urllib.parse
''''''
''''''


@application.route('/', methods=['GET', 'POST'])
def login():
    # Get users.json data.
    with open('users.json', 'r+') as jsonfile:  # seperate function (users-r)
        users_data = json.loads(jsonfile.read())
        jsonfile.close()
    # Create login form for user
    form = LoginForm()
    user_data, password = None, None
    # validate user login info
    if form.validate_on_submit():
        flash("Login requested for {form.username.data}.")
        for user in users_data:
            if user["username"] == form.username.data:
                user_data = user
                password = user_data["password"]
                print(password == form.password.data)
                if password == form.password.data:
                    print("correct password")
                    print("pooping")
                    try:
                        # get jobs from websites
                        runpy.run_path("./pyproject.py")
                    except RuntimeError:
                        print("Something went wrong pulling jobs. Reload and try again.")
                    return redirect(f"/jobs/{user_data['ID']}")
        # if user does not exist redirect to account page
        if user_data is None:
            print("create account")
            flash("User does not exist for {form.username.data}")
            return redirect("/new_account")
    return render_template("login.html", title="Login", form=form, user_data=user_data)


@application.route('/new_account', methods=['GET', 'POST'])
def create_account():
    with open('users.json', 'r+') as jsonfile:  # seperate function (users-r)
        users_data = json.loads(jsonfile.read())
        jsonfile.close()
    form = LoginForm()
    new_account = User()
    no_user = False
    print(new_account.ID)
    # validate user login info
    if form.validate_on_submit():
        print(no_user)
        for user in users_data:
            if user == form.username.data:
                flash("User, {form.username.data}, already exists.")
                no_user = False
            else:
                no_user = True
        print(no_user)
        if no_user:
            new_account.username = form.username.data
            new_account.password = form.password.data
            # save to user json file
            with open('users.json', 'w') as jsonfile:  # seperate function (users-w)
                users_data.append(new_account.to_dict())
                jsonfile.write(json.dumps(users_data))
                jsonfile.close()
            print("pooping")
            try:
                # get jobs from websites
                runpy.run_path("./pyproject.py")
            except RuntimeError:
                print("Something went wrong pulling jobs. Reload and try again.")
            return redirect(f"/jobs/{new_account.ID}")
    return render_template("new_account.html", title="New Account", form=form, user_data=new_account)


def bookmark_jobs(jobs, user_data, users_data, forms, displaying_favorites, request_info):
    print("bookmark jobs function")
    favorites = [list(favorite.values())[:-5] for favorite in user_data["favorites"]]
    try:
        idx = int(request_info["id"])
        job = jobs[idx]
        if request_info["checked"] == "true":
            job["favorite"] = True
        elif request_info["checked"] == "false":
            job["favorite"] = False
        print("Job Selected")
        print(job)
        if job["favorite"] is True and list(job.values())[:-5] not in favorites:
            print("adding")
            # add to user favorites
            user_data["favorites"].append(job)
        elif job["favorite"] is False and list(job.values())[:-5] in favorites:
            print("removing")
            # remove from user favorites
            user_data["favorites"] = [favorite for favorite in user_data["favorites"] if list(favorite.values())[:-5] != list(job.values())[:-5]]
        if not displaying_favorites:
            # update job values
            jobs.pop(idx)
            jobs.insert(idx, job)
            with open('jobs.json', 'w') as jsonfile:  # seperate function (jobs-w)
                jsonfile.write(json.dumps(jobs))
                jsonfile.close()
        # modify users data
        users_data.append(user_data)
        with open('users.json', 'w') as jsonfile:  # seperate function (users-w)
            jsonfile.write(json.dumps(users_data))
            jsonfile.close()
    except Exception:
        pass


@application.route('/jobs/<int:user_id>', methods=['GET', 'POST'])
def display_jobs(user_id):
    # Get USER Data
    with open('users.json', 'r+') as jsonfile:  # seperate function (users-r)
        users_data = json.loads(jsonfile.read())
        jsonfile.close()
    for user in users_data:
        if user["ID"] == user_id:
            user_data = user
    user_idx = users_data.index(user_data)
    users_data.pop(user_idx)
    # Get JOB Data
    jobs = None
    with open("jobs.json", "r+") as jsonfile:  # seperate function (jobs-r)
        jobs = json.loads(jsonfile.read())
        jsonfile.close()
    job_count = len(jobs)
    # create forms for each jobs
    form = FilterDataForm()
    forms = []
    favorites = [list(favorite.values())[:-5] for favorite in user_data["favorites"]]
    for job in jobs:
        # adding forms for each job
        forms.append(FavoritesForm(prefix=str(job["idx"])))
        # check if jobs have been bookmarked/ favorited
        if list(job.values())[:-5] in favorites:
            job["favorite"] = True
        else:
            job["favorite"] = False
    # Handling requests for search input and bookmark inputs
    user_input = None
    request_info = request.form.to_dict()
    # SEARCH SECTION
    if request.method == "POST" and "searched" in list(request_info) and len(request_info["searched"]) > 0:
        print("here1")
        user_input = request_info["searched"]
        print(user_input)
        # change jobs depending on search criteria
        if len(user_input) == 2 and len(job["location"]) > 2:
            jobs = [job for job in jobs if user_input.lower() == job["location"][-2:].lower()]
        else:
            jobs = [job for job in jobs if user_input.lower() in job["title"].lower() or user_input.lower() in job["location"].lower() or user_input.lower() in job["company"].lower()]
        # jobs = list(filter(lambda job: user_input.lower() in job["title"].lower() or user_input.lower() in job["location"].lower() or user_input.lower() in job["company"].lower(), jobs))          
        job_count = len(jobs)
        # create forms for each job
        forms = []
        # for job in jobs:
        for job in jobs:
            forms.append(FavoritesForm(prefix=str(job["idx"])))
    # BOOKMARK SECTION
    elif request.method == "POST" and "checked" in list(request_info):
        print("here2")
        displaying_favorites = False
        bookmark_jobs(jobs, user_data, users_data, forms, displaying_favorites, request_info)

    return render_template("jobs.html", title="Entry-Level CS Jobs", form=form, user_input=user_input, user=user_data, jobs=jobs, job_count=job_count, forms=forms)


@application.route('/jobs/<int:user_id>/favorites', methods=['GET', 'POST'])
def display_favorites(user_id):
    # Get User Data
    with open('users.json', 'r+') as jsonfile:  # seperate function (users-r)
        users_data = json.loads(jsonfile.read())
        jsonfile.close()
    user_data = None
    for user in users_data:
        if user["ID"] == user_id:
            user_data = user
    jobs = user_data["favorites"]
    job_count = len(user_data["favorites"])
    # create forms for each job
    forms = []
    for i in range(job_count):
        forms.append(FavoritesForm(prefix=str(i)))
    print(request.form.to_dict())
    if request.method == "POST" and "checked" in list(request.form.to_dict()):
        print("editing favorites")
        request_info = request.form.to_dict()
        displaying_favorites = True
        update_jobs(jobs, user_data, users_data, forms, displaying_favorites, request_info)

    return render_template("favorites.html", title="Favorite Jobs", user=user_data, jobs=jobs, job_count=job_count, forms=forms)
