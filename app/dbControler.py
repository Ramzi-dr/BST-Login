from app import db
from app.models import User
from sqlalchemy import select, update, delete, values

sql1 = delete(User).where(User.name.in_(['bst-admin','ramzi']))


db.session.execute(sql1)
db.session.commit()


print(User.query.all())
print(User.query.first())

import os
print(os.environ.get('EMAIL_USER'))

