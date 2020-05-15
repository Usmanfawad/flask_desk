from ProDesk.models import *


user_1 = Users(f_name="Usman", l_name="Fawad",email="usman@gmail.com",password="$2b$12$qvA0U9BfwJsydMaLT/IBheiyQdZ4JW1u39KvVDW85gJU//KUunLF6",number="0123",department="SUPER",role="ADMIN")
user_2 = Users(f_name="Hamdan", l_name="Fawad",email="h@gmail.com",password="123",number="0123322",department="MATERIAL",role="ADMIN")


item_1=Inventory(name="CPU",ip_address="12345",mac_address="123455",purchase_date="12/02/2020",ageing_date="12/02/2024")
item_2=Inventory(name="Monitor",ip_address="123456",mac_address="1234556",purchase_date="12/02/2020",ageing_date="12/02/2024")

db.session.add(user_2)
# db.session.add(item_2)
# db.session.add(item_1)
db.session.commit()
print("added")