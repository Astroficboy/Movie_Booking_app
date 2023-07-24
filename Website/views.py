from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Theaters, Bookings, showListing, Admin
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import base64 
import numpy as np
from io import BytesIO
from . import db


views = Blueprint('views', __name__)


# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     show_listing = showListing.query.filter_by()
#     # tasks = Task.query.filter_by(user_id = current_user.id)
#     # user = User.query.filter_by(id = current_user.id).first()
#     # tasks_by_lists = {}
#     # for t in tasks:
#     #     l = t.task_list_id
#     #     tasks = None
#     #     # tasks = tasks_by_lists[l]
#     #     if not l in tasks_by_lists.keys():
#     #         tasks = []
#     #         tasks_by_lists[l] = tasks
#     #     else:
#     #         tasks = tasks_by_lists[l]
#     #     tasks.append(t)

#     return(render_template('movies.html'))


# @views.route('/create_list', methods=['GET', 'POST'])
# def create_list():
#     user = User.query.filter_by(id = current_user.id).first()
#     list_name = request.form.get('listName')
#     update_task_list = Task_list(name=list_name, user_id = current_user.id)
#     if list_name is not None:
#         db.session.add(update_task_list)    
#         db.session.commit()
#     if request.method == 'POST':
#         flash('New list added.', category='success')
#         return((redirect(url_for('views.home'))))
#     return(render_template('create_list.html', user=user))
    

# @views.route('/create_task', methods=['GET', 'POST'])
# def create_task():
#     user = User.query.filter_by(id = current_user.id).first()
#     tasks_title = request.form.get('taskName')
#     description = request.form.get('description')
#     list_id = request.args.get('list_id')
#     status = request.form.get('status')
#     __status__= Task_status.Not_defined
#     if request.method == 'POST':
#         for s in Task_status:
#             if s.name==status:
#                 __status__=status
#         if description is None:
#             description = None
#         update_task = Task(task_list_id=list_id, user_id=current_user.id, title=tasks_title, 
#         description=description, status=__status__, end_date=datetime.now().date()+timedelta(2), 
#         completed_on_date=datetime.now().date()+timedelta(2))
#         if tasks_title is not None:
#             db.session.add(update_task)    
#             db.session.commit()
#             flash('New task added.', category='success')
#         return((redirect(url_for('views.home'))))
#     return(render_template('create_task.html', user=user, list_id=list_id))


# @views.route('/delete_list', methods=['POST', 'GET'])
# def delete_list():
#     user = User.query.filter_by(id = current_user.id).first()
#     list_id = request.args.get('list_id')
#     Task_list.query.filter_by(id=list_id).delete()
#     Task.query.filter_by(id=list_id).delete()
#     db.session.commit()
#     if request.method == 'POST':
#         flash('List deleted.', category='success')
#         return((redirect(url_for('views.home'))))
#     return(render_template('delete_list.html', user=user))

# @views.route('/edit_list', methods=['POST', 'GET'])
# def edit_list():
#     user = User.query.filter_by(id = current_user.id).first()
#     list_id = request.args.get('list_id')
#     changed_name = request.form.get('new_list_name')
  
#     get_list = Task_list.query.filter_by(id = list_id).first()
#     get_list1 = Task_list.query.filter_by(id = list_id)
#     current_name = get_list.name
#     get_list1.update(dict(name = changed_name))
#     db.session.commit()
#     if request.method == 'POST':
#         flash('List name changed.', category='success')
#         return((redirect(url_for('views.home'))))
#     return(render_template('edit_list.html', user=user, current_name = current_name))

    
# @views.route('/delete_task', methods=['POST', 'GET'])
# def delete_task():
#     user = User.query.filter_by(id = current_user.id).first()
#     task_id = request.args.get('task_id')
#     Task.query.filter_by(id=task_id).delete()
#     db.session.commit()
#     if request.method == 'POST':
#         flash('Task deleted.', category='success')
#         return((redirect(url_for('views.home'))))
#     return(render_template('delete_task.html', user=user))

# @views.route('/edit_task', methods=['POST', 'GET'])
# def change_status():
#     user = User.query.filter_by(id = current_user.id).first()
#     lists = Task_list.query.filter_by(user_id = current_user.id)
#     task_id = request.args.get('task_id')
#     get_task1 = Task.query.filter_by(id = task_id).first()
#     if request.method == 'POST':
#         changed_status = request.form.get('status')
#         changed_list = request.form.get('changed_list')
#         change_deadline = request.form.get('change_deadline')
#         datetime_object = datetime.strptime(change_deadline.replace("T"," "), '%Y-%m-%d %H:%M')
#         changed_list_id = 0
#         for list_name in lists:
#             if list_name.name == changed_list:
#                 changed_list_id = list_name.id
#         get_task = Task.query.filter_by(id = task_id)
#         get_task.update(dict(status = changed_status, task_list_id = changed_list_id))
#         if changed_status == "DONE":
#             get_task.update(dict(status = changed_status, task_list_id = changed_list_id,completed_on_date=datetime.now().date()))
#         for task in get_task:
#             if datetime_object != task.end_date:
#                 get_task.update(dict(end_date = datetime_object))
#         db.session.commit()
#         flash('Task updated.', category='success')
#         return((redirect(url_for('views.home'))))
#     if request.method == "GET":
#         return(render_template('edit_task.html', user=user, task_id=task_id, lists=lists, task_name = get_task1.title))

# @views.route('/change_name', methods=['GET', 'POST'])
# def change_name():
#     user = User.query.filter_by(id = current_user.id).first()
#     task_id = request.args.get('task_id')
#     get_task = Task.query.filter_by(id = task_id)
#     changed_name = request.form.get('changedName')
#     print(changed_name)
#     if request.method == "POST":
#         get_task.update(dict(title = changed_name))
#         flash('Task updated.', category='success')
#         db.session.commit()
#         return((redirect(url_for('views.home'))))
#     return(render_template('change_name.html', user=user, task_id=task_id))


# @views.route('/summary', methods=['GET'])
# def summary():
#     user = User.query.filter_by(id = current_user.id).first()
#     tasks = Task.query.filter_by(user_id = current_user.id)
#     lists = Task_list.query.filter_by(user_id = current_user.id)
#     completed_tasks = []
#     incomplete_tasks = []
#     tasks_on_time = []
#     lists_with_completed_tasks = []
    
#     for task in tasks:
#         if task.status == Task_status.DONE:
#             completed_tasks.append(task)
#             lists_with_completed_tasks.append(task.task_list_id)
#         elif task.completed_on_date !="NULL" and task.end_date > task.completed_on_date :
#             tasks_on_time.append(task)
#             completed_tasks.append(task)
#             lists_with_completed_tasks.append(task.task_list_id)
#         else:
#             incomplete_tasks.append(task)
#     def build_data(plot):
#         plot.seek(0)
#         return base64.b64encode(plot.getvalue()).decode()

#     def make_plot():
#         a = len(completed_tasks)
#         b = len(incomplete_tasks)
#         c = [a, b]
#         if a != 0 or b != 0:
#             plt.pie(c, labels = ["Completed tasks", "Incomplete tasks"], colors=["Green", "Orange"])
#         if (a) == 0 and (b) == 0:
#             flash("You do not have any tasks yet.", category='error')
#         plt.legend(loc='center')
#         plot = BytesIO()
#         plt.savefig(plot, format = 'png', bbox_inches  ='tight')
#         plt.clf()
#         return plot
    
#     data = build_data(make_plot())
#     set_of_lists = set(lists_with_completed_tasks)
#     number_of_lists = len(set_of_lists)
#     return(render_template('summary.html', user=user, completed_tasks=completed_tasks, incomplete_tasks=incomplete_tasks,
#                            tasks_on_time=tasks_on_time, lists=lists, lists_with_completed_tasks=lists_with_completed_tasks,
#                            data = data, number_of_lists = number_of_lists))


@views.route('/', methods=['GET'])
def home():
    user = User.query.filter_by().first()
    admin = Admin.query.filter_by().first()
    return render_template('movies.html', user=user, admin=admin)

@views.route('/bookings', methods=['GET'])
# @login_required
def booking():
    user = User.query.filter_by().first()
    return render_template('booking.html', user=user)

@views.route('/theaters', methods=['GET', 'POST'])
@login_required
def manage_theater():
    admin = Admin.query.filter_by().first()
    user = User.query.filter_by().first()
    return render_template('theaters.html', admin=admin, user=user)

@views.route('/summary', methods=['GET'])
def summary():
    admin = Admin.query.filter_by().first()
    user = User.query.filter_by().first()
    return render_template('summary.html', admin=admin, user=user)

