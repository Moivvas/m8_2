from mongoengine import *

connect(host="mongodb+srv://moivvas:moivvaspassword@cluster0.4mzl2qs.mongodb.net/?retryWrites=true&w=majority")

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(max_length=50)
    confirm = BooleanField(default=False)