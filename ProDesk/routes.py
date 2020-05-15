from ProDesk import app
from flask import render_template,url_for,flash,redirect,request,abort,jsonify
from flask_login import login_user,current_user,logout_user,login_required
from ProDesk.forms import *
from functools import wraps

from ProDesk import app,db,bcrypt,login_manager

from ProDesk.models import *


def login_required(role="ANY",department="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.role != role and current_user.department != department) and (role != "ANY" and department != "ANY")):
                print("HERE AGAIN")
                return redirect(url_for('unauthorized'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/unauthorized',methods=['GET','POST'])
def unauthorized():
    if current_user.role == 'ADMIN':
        page = 'admin_material_dashboard'
    elif current_user.role == 'USER':
        page = 'userManager'
    elif current_user.role == 'USER_DEPART_USER':
        page = 'userUser'
    elif current_user.role == 'TECH_DEPART_MANAGER':
        page = 'techManager'
    elif current_user.role == 'TECH_DEPART_TECH':
        page = 'techTech'
    return render_template('unauthorized.html',page=page)

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'ADMIN' and current_user.department=='MATERIAL':
            return redirect(url_for('admin_material_dashboard'))
        elif current_user.role == 'USER_DEPART_MANAGER':
            return redirect(url_for('userManager'))
        elif current_user.role == 'USER_DEPART_USER':
            return redirect(url_for('userUser'))
        elif current_user.role == 'TECH_DEPART_MANAGER':
            return redirect(url_for('techManager'))
        elif current_user.role == 'TECH_DEPART_TECH':
            return redirect(url_for('techTech'))
    form = LoginForm()
    if form.validate_on_submit():
        print("came here")
        user = Users.query.filter_by(email=form.email.data).first()

        # if bcrypt.check_password_hash(user.password,form.password.data):
        if user.password==form.password.data:
            login_user(user,remember=form.remember.data)
            if user.role == 'ADMIN' and user.department=='MATERIAL':
                return redirect(url_for('admin_material_dashboard'))
            elif user.role == 'USER_DEPART_MANAGER':
                return redirect(url_for('userManager'))
            elif user.role == 'USER_DEPART_USER':
                return redirect(url_for('userUser'))
            elif user.role == 'TECH_DEPART_MANAGER':
                return redirect(url_for('techManager'))
            elif user.role == 'TECH_DEPART_TECH':
                return redirect(url_for('techTech'))

        else:
            flash('Incorrect Credentials. Please try again!','danger')

    return render_template('login.html',title="Login",form=form)


#-------------------------------ADMIN DASHBOARD-------------------------------

@app.route("/admin_material/dashboard/")
@login_required(role="ADMIN",department="MATERIAL")
def admin_material_dashboard():
    inventory_items= Inventory.query.all()
    users=Users.query.all()
    count_users=0
    for all in users:
        count_users+=1
    count_inventory_unassigned=0
    count_inventory_assigned=0
    for all in inventory_items:
        if all.user_id=="":
            count_inventory_unassigned+=1
        else:
            count_inventory_assigned+=1

    return render_template("admin_material_dashboard.html",inventory_items=inventory_items,users=users,count_users=count_users,count_inventory_unassigned=count_inventory_unassigned,count_inventory_assigned=count_inventory_assigned)


#--------------------------------VIEW ALL INVENTORY ITEMS AND CREATE INVENTORY ITEMS--------------------------------

@app.route("/admin_material/inventory/",methods=['GET','POST'])
@login_required(role="ADMIN",department="MATERIAL")
def admin_material_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        inventory=Inventory(name=form.name.data,ip_address=form.ip_address.data,mac_address=form.mac_address.data,purchase_date=form.purchase_date.data,ageing_date=form.ageing_date.data)
        db.session.add(inventory)
        db.session.commit()
        flash("Form submitted successfully","success")
        return redirect(url_for('admin_material_inventory'))
    inventory_items= Inventory.query.all()
    users=Users.query.all()
    return render_template("admin_material_inventory.html",inventory_items=inventory_items,users=users,form=form)


#--------------------------------ASSIGN ITEMS TO USER--------------------------------

@app.route("/admin_material/inventory/<string:item_id>/users",methods=['GET','POST'])
@login_required(role="ADMIN",department="MATERIAL")
def admin_material_inventory_users(item_id):
    users = Users.query.all()
    items = Inventory.query.filter_by(id=item_id).first()
    if request.method=="POST":
        user= request.form['remove']
        print(user)
        item_object=Inventory.query.filter_by(id=item_id).first()
        item_object.user_id=user
        db.session.commit()
        flash("Item assigned to user","success")
        return redirect(url_for("admin_material_inventory"))
    return render_template('admin_material_inventory_users.html',users=users,items=items)


#--------------------------------USER REGISTRATION FORM AND USER VIEW--------------------------------

@app.route("/admin_material/users",methods=['GET','POST'])
@login_required(role="ADMIN",department="MATERIAL")
def admin_material_users():
    form = MaterialUserForm()
    users=Users.query.all()
    email_list=[]
    number_list=[]
    for all in users:
        email_list.append(all.email)
        number_list.append(all.number)

    if form.validate_on_submit():
        if (form.email.data not in email_list) and (form.number.data not in number_list):
            user_depart = request.form['remove']
            user=Users(f_name=form.f_name.data,l_name=form.l_name.data,email=form.email.data,number=form.number.data,department=user_depart,role=form.role.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash("Form submitted successfully","success")
                return redirect(url_for('admin_material_users'))
            except:
                flash("Duplicate key error", "danger")
        else:
            flash("Email or number already exists","Danger")
            return redirect(url_for('admin_material_users'))

    users = Users.query.all()
    return render_template("admin_material_users.html",users=users,form=form,email_list=email_list,number_list=number_list)


#--------------------------------ITEMS ASSIGNED TO PARTICULAR USER--------------------------------

@app.route("/admin_material/users/<string:user_id>",methods=['GET','POST'])
@login_required(role="ADMIN",department="MATERIAL")
def admin_material_users_inventory(user_id):
    users = Users.query.filter_by(id=user_id).first()
    items= Inventory.query.filter_by(user_id=user_id)
    if request.method=="POST":
        item= request.form['remove']
        print(item)
        item_object=Inventory.query.filter_by(id=item).first()
        item_object.user_id=""
        db.session.commit()
        flash("Item removed from User's custody","success")
    return render_template("admin_material_users_inventory.html",users=users,items=items)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

