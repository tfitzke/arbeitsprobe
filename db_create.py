from arbeitsprobe_server import db
from models import *
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func


#create the database
db.create_all()

#insert
# tag1 = Tag("Mountains")
# pag1 = Pag("Mt. Everest")
# photo1 = Photo("Till", "kik")

# db.session.add(tag1)
# db.session.add(pag1)
# db.session.add(photo1)
#FFFFFFFF

# db.session.commit()

# photo1.taggedPhotos.append(tag1)

# db.session.commit()