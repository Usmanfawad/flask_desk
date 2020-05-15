from ProDesk import db, login_manager, app
from sqlalchemy import ForeignKey
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=False)
    password = db.Column(db.String(50), nullable=False, default="123")
    number = db.Column(db.String(15), nullable=False, unique=True)
    department= db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    inventory_item= db.Column(db.String(100),nullable=True)


    def __repr__(self):
        return "USER({},{},{},{},{},{},{},{},{},{})".format(self.id, self.fname, self.lname, self.email, self.password, self.number, self.department, self.role,self.inventory_item)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    ip_address = db.Column(db.String(30), nullable=False,unique=True)
    mac_address = db.Column(db.String(30), nullable=False,unique=True)
    purchase_date = db.Column(db.String(15), nullable=False)
    ageing_date = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return "INVENTORY({},{},{},{},{},{},{})".format(self.id,self.name,self.ip_address,self.mac_address,self.purchase_date,self.ageing_date,self.user_id)

class Event(db.Model):
    id= db.Column(db.Integer, primary_key=True)






