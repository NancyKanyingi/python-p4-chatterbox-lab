from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200 

@app.post("/messages")
def create_message():
    data = request.get_json()

    if not data.get("body") or not  data.get("username"):
        return jsonify({"error": "body and username are required",}), 400

    new_msg = Message(
        body=data["body"],
        username=data["username"]
    ) 
    db.session.add(new_msg)
    db.session.commit()

    return jsonify(new_msg.to_dict()), 201

@app.patch('/messages/<int:id>')
def messages_by_id(id):
    msg = Message.query.get_or_404(id)
    data = request.get_json()

    if "body" in data:
        msg.body = data["body"]

    db.session.commit()
    return jsonify(msg.to_dict()), 200

    @app.delete("/messages/<int:id>")
    def delete_message(id):
        msg = Message.query.get_or_404(id)
        db.session.delete(msg)
        db.session.commit()
        db.session.expire_all()

        return jsonify({"message": "Message deleted"}), 200

    



if __name__ == '__main__':
    app.run(port=5555)
