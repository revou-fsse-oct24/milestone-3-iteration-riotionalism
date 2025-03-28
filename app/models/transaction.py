from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(255), nullable=False)  # deposit, withdrawal, transfer
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(255), default='completed')  # pending, completed, failed

    def __repr__(self):
        return f'<Transaction {self.id} - {self.type}>'
