from . import db

class User(db.Model):
    __tablename__ = 'User'  # Table name

    firebaseID = db.Column(db.Integer, primary_key=True)  # Primary Key
    shippingAddress = db.Column(db.String(100), nullable=True)  # Shipping Address
    invoiceAddress = db.Column(db.String(100), nullable=True)  # Invoice Address
    idCartItem = db.Column(db.Integer, db.ForeignKey('CartItem.idCartItem'), nullable=True)  # Foreign Key

    # Relationships
    #cart_item = db.relationship('CartItem', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.firebaseID}', '{self.shippingAddress}', '{self.invoiceAddress}', '{self.idCartItem}')"


class Disc(db.Model):
    __tablename__ = 'disc'  

    idDisc = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    label = db.Column(db.String(100), nullable=True) 
    title = db.Column(db.String(100), nullable=True)  
    format = db.Column(db.String(100), nullable=True)  
    price = db.Column(db.Integer, nullable=True)  

    def __repr__(self):
        return f"Disc('{self.idDisc}', '{self.label}', '{self.title}', '{self.format}', {self.price})"

