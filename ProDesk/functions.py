from ProDesk.models import *


def assign_item(item_id,user_id):
    update_item=Inventory.query.filter_by(id=item_id).first()
    update_item.user_id=user_id
    db.session.commit()


assign_item(2,1)
user_1= Inventory.query.filter_by(user_id=1).all()


counter=1
for all in user_1:
    print(all.name)
    counter+=1
