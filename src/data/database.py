from gino import Gino

db = Gino()


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.BigInteger, primary_key=True)
    full_name = db.Column(db.String(250), default=None)
    vk_url = db.Column(db.String(250), default=None)
    email = db.Column(db.String(100), default=None)


class Coordinator(db.Model):
    __tablename__ = "coordinator"
    telegram_id = db.Column(db.BigInteger, primary_key=True)
    full_name = db.Column(db.String(250), default=None)


class Manager(db.Model):
    __tablename__ = "manager"
    telegram_id = db.Column(db.BigInteger, primary_key=True)
    full_name = db.Column(db.String(250), default=None)
    coordinator = db.Column(db.BigInteger, db.ForeignKey("coordinator.telegram_id"))


class Tariff(db.Model):
    __tablename__ = "tariff"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(100), default=None)


class Month(db.Model):
    __tablename__ = "month"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(100), default=None)
    column = db.Column(db.SmallInteger, default=None)


class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(100), default=None)


class SaleType(db.Model):
    __tablename__ = "sale_type"
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(250), default=None)


class Subscription(db.Model):
    __tablename__ = "subscription"
    user = db.Column(db.BigInteger, db.ForeignKey("student.id"))
    tariff = db.Column(db.SmallInteger, db.ForeignKey("tariff.id"))
    month = db.Column(db.SmallInteger, db.ForeignKey("month.id"))
    subject = db.Column(db.SmallInteger, db.ForeignKey("subject.id"))
    sale_type = db.Column(db.SmallInteger, db.ForeignKey("sale_type.id"))
