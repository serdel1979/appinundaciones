from app import login_manager, db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.helpers.util import hash_pass
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func, text

"""
Este es el modelo de usuario, donde se representa a los 
usuarios del sistema, junto con sus roles y permisos
"""


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, server_default='1', default=True)
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    created_at = db.Column(db.DateTime, server_default=func.now())
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    _roles = relationship("Role", secondary="user_role", backref='user')

    def __init__(self, username, first_name, last_name, email, password=None, roles=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if password:
            self.password = hash_pass(password)
        if roles:
            for r in roles:
                role = Role.query.get(r)
                self._roles.append(role)

    def __repr__(self):
        return str(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def find_by_email_and_pass(email, passw):
        usuario = User.query.filter_by(email=email).first()
        if usuario and usuario.password == passw:
            return usuario
        else:
            return None

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=bytes(username, 'utf-8')).first()

    @classmethod
    def all(cls, active, order_by):
        return cls.query.filter_by(active=active).order_by(text(order_by))

    def add_roles(self, roles):
        if roles:
            for r in roles:
                role = Role.query.get(r)
                self._roles.append(role)

    def add_existing_role_by_name(self, role_name):
        role = Role.query.filter_by(
            name=role_name).first()

        self._roles.append(role)

    def is_admin(self):
        return ('administrador' in self.roles)
    
    def is_google_user(self):
        # TODO: agregar un atributo al modelo User,
        # que defina si es un usuario regular o de google.
        # Por lo pronto para salir de apuros, sabemos que
        # un usuario de google tiene su contraseña nula
        return self.password is None

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @declared_attr
    def roles(self):
        return association_proxy('_roles', 'name')

    def get_permissions(self):
        permisos = []  # se retorna una lista de permisos
        for rol in self._roles:
            for p in rol.permissions:
                permisos.append(p.name)
        return permisos

    def toggle(self):
        self.active = not self.active
        self.save()

    @classmethod
    def by_username(cls, username, active, order_by):
        return cls.query.filter((cls.username.like("%{}%".format(username))) & (cls.active == active)).order_by(text(order_by))


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


"""
Modelo de roles
"""


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    users = relationship("User", secondary="user_role", backref="role")
    permissions = relationship(
        "Permission", secondary="role_permission", backref="role")

    def __init__(self, name):
        self.name = name.lower()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                name=permission).first()
            if not existing_permission:
                existing_permission = Permission(permission)
                existing_permission.save()
            self.permissions.append(existing_permission)

    def remove_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                name=permission).first()
            if existing_permission and existing_permission in self.permissions:
                self.permissions.remove(existing_permission)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


"""
Modelo que representa a permisos
"""


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    roles = relationship("Role", secondary="role_permission",
                         backref="permission")

    def __init__(self, name):
        self.name = name.lower()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


"""
Relación entre roles, usuarios y permisos
"""

rolePermission = db.Table('role_permission',
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('role_id', db.Integer,
                                    db.ForeignKey('role.id')),
                          db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


userRole = db.Table('user_role',
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
