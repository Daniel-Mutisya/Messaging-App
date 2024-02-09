
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os
from models import db, User, Message, Agent

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Hello our Esteemed client! Help us know how we can assist you!",
        }
        return jsonify(response_dict)



@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.serialize() for user in users])
    elif request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return jsonify(user.serialize())
    elif request.method == 'PUT':
        data = request.json
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify(user.serialize())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 204


# Define routes for Messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        return jsonify([message.serialize() for message in messages])
    elif request.method == 'POST':
        data = request.json
        new_message = Message(message=data['message'], response=data.get('response'))
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:message_id>', methods=['GET', 'PUT', 'DELETE'])
def message(message_id):
    message = Message.query.get_or_404(message_id)
    if request.method == 'GET':
        return jsonify(message.serialize())
    elif request.method == 'PUT':
        data = request.json
        message.message = data.get('message', message.message)
        message.response = data.get('response', message.response)
        db.session.commit()
        return jsonify(message.serialize())
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'}), 204

# Define routes for Agents
@app.route('/agents', methods=['GET', 'POST'])
def agents():
    if request.method == 'GET':
        agents = Agent.query.all()
        return jsonify([agent.serialize() for agent in agents])
    elif request.method == 'POST':
        data = request.json
        new_agent = Agent(username=data['username'], message=data['message'])
        db.session.add(new_agent)
        db.session.commit()
        return jsonify(new_agent.serialize()), 201

@app.route('/agents/<int:agent_id>', methods=['GET', 'PUT', 'DELETE'])
def agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    if request.method == 'GET':
        return jsonify(agent.serialize())
    elif request.method == 'PUT':
        data = request.json
        agent.username = data.get('username', agent.username)
        agent.message = data.get('message', agent.message)
        db.session.commit()
        return jsonify(agent.serialize())
    elif request.method == 'DELETE':
        db.session.delete(agent)
        db.session.commit()
        return jsonify({'message': 'Agent deleted'}), 204








if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

