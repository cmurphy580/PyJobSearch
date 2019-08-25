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


def bookmark_jobs(jobs, user_data, users_data, forms, not_display_favorites):
    # function handles when a job is bookmarked. will write the date to user json file and jobs json file.
    favorites = list(map(lambda favorite: list(favorite.values())[:-3], user_data["favorites"]))
    # check if jobs have been bookmarked/ favorited
    for job in jobs:
        if list(job.values())[:-3] in favorites:
            job["favorite"] = True
        else:
            job["favorite"] = False

    try:
        if request.method == "POST" and "-csrf_token" in list(request.form.to_dict())[0]:
            # idx == index of job to be favorited - got index from request form
            idx = int((list(request.form.to_dict())[0]).split("-")[0])
            if idx == len(jobs):
                idx -= 1
            print(idx)
            print(len(jobs))
            job = jobs[idx]
            job["favorite"] = forms[idx].add_to_favorites.data
            print("Job Selected")
            print(job)

            if job["favorite"] is True and list(job.values())[:-3] not in favorites:
                print("adding")
                # add to user favorites
                user_data["favorites"].append(job)
            elif job["favorite"] is False and list(job.values())[:-3] in favorites:
                print("removing")
                # remove from user favorites
                user_data["favorites"] = [favorite for favorite in user_data["favorites"] if list(favorite.values())[:-3] != list(job.values())[:-3]]

            if not_display_favorites:
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
    with open("jobs.json", "r+") as jsonfile:  # seperate function (jobs-r)
        unfiltered_jobs = json.loads(jsonfile.read())
        jsonfile.close()

    # TEST
    '''
    TEST TEST TEST TEST
    '''

    req = request.get_json()
    print("TESTTESTTESTTESTTESTTESTTEST")
    print(req)

    '''
    TEST TEST TEST TEST
    '''
    # TEST


    # SEARCH SECTION
    form = FilterDataForm()
    user_input = None
    if request.method == "POST" and "submit" in list(request.form.to_dict()) and len(form.user_input.data) > 0:
        # if form.submit.data and form.validate():
        print("here1")
        user_input = form.user_input.data
        jobs = list(filter(lambda job: user_input.lower() in job["title"].lower() or user_input.lower() in job["location"].lower() or user_input.lower() in job["company"].lower(), unfiltered_jobs))
        job_count = len(jobs)
        # create forms for each job
        forms = []
        print(job_count)
        for job in jobs:
            forms.append(FavoritesForm(prefix=str(job["idx"])))

        # BOOKMARK SECTION
        not_display_favorites = True
        bookmark_jobs(jobs, user_data, users_data, forms, not_display_favorites)
    else:
        print("here2")
        jobs = unfiltered_jobs
        job_count = len(jobs)
        # create forms for each job
        forms = []
        print(job_count)
        for job in jobs:
            forms.append(FavoritesForm(prefix=str(job["idx"])))

        # BOOKMARK SECTION
        not_display_favorites = True
        bookmark_jobs(jobs, user_data, users_data, forms, not_display_favorites)

    return render_template("jobs.html", title="Entry-Level CS Jobs", form=form, user_input=user_input, user=user_data, jobs=jobs, job_count=job_count, forms=forms)


@application.route('/jobs/<int:user_id>/favorites', methods=['GET', 'POST'])
def display_favorites(user_id):
    # Get User Data
    with open('users.json', 'r+') as jsonfile:  # seperate function (users-r)
        users_data = json.loads(jsonfile.read())
        jsonfile.close()

    for user in users_data:
        if user["ID"] == user_id:
            user_data = user

    user_idx = users_data.index(user_data)
    users_data.pop(user_idx)
    jobs = user_data["favorites"]
    job_count = len(user_data["favorites"])
    # create forms for each job
    forms = []
    for i in range(job_count):
        forms.append(FavoritesForm(prefix=str(i)))

    not_display_favorites = False
    bookmark_jobs(jobs, user_data, users_data, forms, not_display_favorites)

    return render_template("favorites.html", title="Favorite Jobs", user=user_data, jobs=jobs, job_count=job_count, forms=forms)
