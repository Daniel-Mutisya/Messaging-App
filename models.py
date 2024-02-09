from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()

# Model for Users (optional expansion)
class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    Serialize_rules= ('-messages.user',)
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

    def _repr_(self):
        return f'<User {self.username}>'

# Model for Messages
class Message(db.Model,SerializerMixin):
    __tablename__ = 'messages'
    
    
    id = db.Column(db.Integer, primary_key=True)
    # customer_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    response = db.Column(db.String(1000), nullable=True)  # Optional response from the agent
    timestamp = db.Column(db.DateTime, nullable=False)

    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    agent_id= db.Column(db.Integer, db.ForeignKey('agents.id'))

    def _repr_(self):
        return f'<Message {self.id} from {self.customer_id}>'


class Agent(db.Model,SerializerMixin):
    __tablename__='agents'

    Serialize_rules= ('-agent.message',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    

    messages = db.relationship('Message', backref='agent', lazy=True)

    def _repr_(self):
        return f'<Agent {self.username}>'