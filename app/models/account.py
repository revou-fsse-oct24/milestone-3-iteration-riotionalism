from app import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions_from = db.relationship('Transaction', 
                                      backref='from_account',
                                      foreign_keys='Transaction.from_account_id',
                                      lazy=True)
    transactions_to = db.relationship('Transaction',
                                    backref='to_account',
                                    foreign_keys='Transaction.to_account_id',
                                    lazy=True)

    def __repr__(self):
        return f'<Account {self.account_number}>'
