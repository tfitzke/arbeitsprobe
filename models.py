from arbeitsprobe_server import db


taggedImages = db.Table(
    'taggedImages',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.photo_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'))
)

# pagsOfTag = db.Table(
#     'pagsOfTag',
#     db.Column('pag_id', db.Integer, db.ForeignKey('pag.pag_id')),
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'))
# )

class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
#    photoName = db.Column(db.String(80), unique=True, nullable=False)
    photoPath = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, path):
 #       self.photoName = name
        self.photoPath = path

    def __repr__(self):
        return '<Photo %r>' % self.photoPath


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tagName = db.Column(db.String(80), unique=True, nullable=False)
    taggedImages = db.relationship(
        'Photo',
        secondary=taggedImages,
        backref=db.backref('photoTags', lazy='dynamic'))
#     pagsOfTag = db.relationship(
#         'Pag',
#         secondary=pagsOfTag,
#         backref="TagsOfPag")
# #  uselist=False,

    def __init__(self, name):
        self.tagName = name

    def __repr__(self):
        return '<Tag %r>' % self.tagName


# class Pag(db.Model):
#     pag_id = db.Column(db.Integer, primary_key=True)
#     pagName = db.Column(db.String(80))
#     pagThumbnail = db.Column(db.String(80))
#     pagUrl = db.Column(db.String(80))

#     def __init__(self, name, thumbnail, url):
#         self.pagName = name
#         self.pagThumbnail = thumbnail
#         self.pagUrl = url

#     def __repr__(self):
#         return '<Pag %r>' % self.pagName
