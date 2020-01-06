from sqlalchemy import Integer, ForeignKey
from app import db
from app import login
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_user import login_required, UserManager, UserMixin
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


class CreateDatabase:
    """
    Database creation on postgresql by checking if a avp_db already exist.
    The name of the database created is 'avp_db'.
    """
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)

        print(database_exists(engine.url))


# Tables creation


class User(db.Model, UserMixin):
    """
    Creation of the User table.
    user_id : an unique int, used as primary_key,
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(255), nullable=False, server_default='')
    #email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    def is_active(self):
        return self.is_enabled

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User({self.id}, email={self.email}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


company_contact = db.Table('company_contact', db.Model.metadata,
                           db.Column('company_id', Integer, ForeignKey('company.id')),
                           db.Column('contact_id', Integer, ForeignKey('contact.id'))
                           )

company_service = db.Table('company_service', db.Model.metadata,
                           db.Column('company_id', Integer, ForeignKey('company.id')),
                           db.Column('service_id', Integer, ForeignKey('service.id'))
)


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), unique=True, index=True)

    contacts = db.relationship('Contact', secondary=company_contact, back_populates="companies")
    emails = db.relationship('Email', back_populates='company')
    phones = db.relationship('Phone', back_populates='company')
    follow_up = db.relationship('FollowUp', back_populates='company')
    quotes = db.relationship('Quote', back_populates='company')
    contractors = db.relationship('Contractor', back_populates='company')
    invoices = db.relationship('Invoice', back_populates='company')
    services = db.relationship('Service', secondary=company_service, back_populates="companies")

    def __repr__(self):
        return f'<Company (PK: {self.id}), company_name: {self.company_name}, count_contact: {len(self.contacts)}>'


class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    job_position = db.Column(db.String(255))
    contact_status = db.Column(db.Enum('Client', 'Prospect', 'Churner', 'Prestataire', 'Reperage',
                                       name='contact_status'))
    start_date = db.Column(db.DateTime, server_default=db.func.now())
    stop_date = db.Column(db.DateTime, default=None)

    companies = db.relationship('Company', secondary=company_contact, back_populates="contacts")
    emails = db.relationship('Email', back_populates='contact')
    phones = db.relationship('Phone', back_populates='contact')
    follow_up = db.relationship('FollowUp', back_populates='contact')
    contractors = db.relationship('Contractor', back_populates='contact')

    def __repr__(self):
        return f'<Contact({self.id}) {self.last_name}, {self.first_name}, {self.job_position},' \
            f'{self.contact_status}>'


class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    contact = db.relationship('Contact', back_populates='emails')
    company = db.relationship('Company', back_populates='emails')

    def __repr__(self):
        return f'<Email {self.id}, contact_id: {self.contact_id}, label: {self.label}, email: {self.email}>'


class Phone(db.Model):
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    label = db.Column(db.String(100))
    phone = db.Column(db.Unicode(10), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    contact = db.relationship('Contact', back_populates='phones')
    company = db.relationship('Company', back_populates='phones')

    def __repr__(self):
        return f'<Phone {self.id}, contact_id: {self.contact_id}, label: {self.label}, phone: {self.phone}>'


class FollowUp(db.Model):
    __tablename__ = 'follow_up'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note = db.Column(db.VARCHAR())
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    contact = db.relationship('Contact', back_populates='follow_up')
    company = db.relationship('Company', back_populates='follow_up')

    def __repr__(self):
        return f'<FollowUp {self.id}, note: {self.note}, contact_id: {self.contact_id}, company_id: {self.company_id}' \
            f'created_at: {self.created_at}>'


quote_service = db.Table('quote_service', db.Model.metadata,
                         db.Column('quote_id', Integer, ForeignKey('quote.id')),
                         db.Column('service_id', Integer, ForeignKey('service.id'))
                         )

quote_invoice = db.Table('quote_invoice', db.Model.metadata,
                         db.Column('quote_id', Integer, ForeignKey('quote.id')),
                         db.Column('invoice_id', Integer, ForeignKey('invoice.id'))
                         )


class Quote(db.Model):
    __tablename__ = 'quote'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_quote = db.Column(db.String)
    quote_status = db.Column(db.Enum('signed', 'sent', 'delay', 'refused', name='quotes_status'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    company = db.relationship('Company', back_populates='quotes')
    invoices = db.relationship('Invoice', secondary=quote_invoice, back_populates='quotes')
    services = db.relationship('Service', secondary=quote_service, back_populates="quotes")
    amount = db.relationship("Amount", uselist=False, back_populates="quote")

    def __repr__(self):
        return f'<Quote {self.id}, ref_quote: {self.ref_quote}, quote_status: {self.quote_status}, ' \
            f'created_at: {self.created_at}, company_id: {self.company_id}>'


contractor_service = db.Table('contractor_service', db.Model.metadata,
                              db.Column('contractor_id', Integer, ForeignKey('contractor.id')),
                              db.Column('service_id', Integer, ForeignKey('service.id'))
                              )


class Contractor(db.Model):
    __tablename__ = 'contractor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    expenses = db.Column(db.Float)
    contractor_payment_ht = db.Column(db.Float)
    contractor_payment_ttc = db.Column(db.Float)

    contact = db.relationship('Contact', back_populates='contractors')
    company = db.relationship('Company', back_populates='contractors')
    invoice = db.relationship('Invoice', back_populates='contractors')
    services = db.relationship("Service", secondary=contractor_service, back_populates="contractors")

    def __repr__(self):
        return f'<Contractor {self.id}, contact_id: {self.contact_id}, company_id: {self.company_id},' \
            f'invoice_id: {self.invoice_id}, expenses: {self.expenses}, ' \
            f'contractor_payment_ht: {self.contractor_payment_ht}, ' \
            f'contractor_payment_ttc: {self.contractor_payment_ttc}>'


class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_invoice = db.Column(db.String)
    invoice_type = db.Column(db.Enum("deposite invoice", "intermediate invoice", "invoice", "final invoice",
                                     name='invoices_type'))
    #quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    #amount_id = db.Column(Integer, ForeignKey('amount.id'))
    #amount = db.relationship('Amount', back_populates="invoices")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    contractors = db.relationship('Contractor', back_populates='invoice')
    quotes = db.relationship('Quote', secondary=quote_invoice, back_populates='invoices')
    company = db.relationship('Company', back_populates='invoices')

    def __repr__(self):
        return f'<Invoice {self.id}, ref_invoice: {self.ref_invoice}, invoice_type: {self.invoice_type},'
        f' company_id: {self.company_id}, created_at: {self.created_at}  >'


service_association_label = db.Table('service_association_label', db.Model.metadata,
    db.Column('service_id', Integer, ForeignKey('service.id')),
    db.Column('label_service_id', Integer, ForeignKey('label_service.id'))
)


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label_services = db.relationship(
        "Label_service",
        secondary=service_association_label,
        back_populates="services")
    # db.Enum('3d', 'direction artistique', 'drone', 'image bank', 'photo', 'photo sur site','post-production',
    # 'production', 'realite augmentee', 'surcyclage', 'video',name='quote_status')
    quotes = db.relationship('Quote', secondary=quote_service, back_populates="services")
    companies = db.relationship('Company', secondary=company_service, back_populates="services")
    contractors = db.relationship("Contractor", secondary=contractor_service, back_populates="services")

    def __repr__(self):
        return f'<Service({self.id}) nb_label={len(self.label_services)}>'


class Label_service(db.Model):
    __tablename__ = 'label_service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(100), unique=True)

    services = db.relationship(
        "Service",
        secondary=service_association_label,
        back_populates="label_services")

    def __repr__(self):
        return f'<Label_service ({self.id}) label={self.label}>'


class Amount(db.Model):
    __tablename__ = 'amount'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    quote_id = db.Column(Integer, ForeignKey('quote.id'))
    quote = db.relationship("Quote", back_populates="amount")

    ht_amount = db.Column(db.Float)
    ttc_amount = db.Column(db.Float)
    payment_status = db.Column(db.Enum('paid', 'waiting', name='payment_status'))
    paid_at = db.Column(db.DateTime)
    #invoice_id = db.Column(Integer, ForeignKey('invoice.id'))
    #invoices = db.relationship("Invoice", back_populates="amount")

    def __repr__(self):
        return '<Amount {}>'.format(self.ht_amount)
