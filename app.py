from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# jonisfy is a method from Flask to convert Python dict into JSON

### https://flask.palletsprojects.com/en/1.1.x/
### https://flask-restful.readthedocs.io/en/latest/quickstart.html
### https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699

# create app within Flask
# wrap app in api. initializes api
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# buses = [
#     {
#         "number_plate": "NAX 123",
#         "manufacturer": "Toyota",
#         "model": "Hiace",
#         "year": "2009",
#         "capacity": 18,
#     },
#     {
#         "number_plate": "LX Z19",
#         "manufacturer": "Ford",
#         "model": "FordX",
#         "year": "2010",
#         "capacity": 45,
#     },
# ]

# database model
class BusModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.number_plate} {self.manufacturer} {self.model} {self.year} {self.capacity}"

    @classmethod
    def bus_serializer(cls, bus):
        return {
            "id": bus.id,
            "number_plate": bus.number_plate,
            "manufacturer": bus.manufacturer,
            "model": bus.model,
            "year": bus.year,
            "capacity": bus.capacity,
        }


# db.create_all()

# Get buses
@app.route(
    "/buses"
)  # decorator involked when '/buses' route is requested and returns JSON
def get_buses():
    # return jsonify(buses)
    return jsonify([*map(BusModel.bus_serializer, BusModel.query.all())])


# Get one bus
@app.route("/buses/<int:index>")
def get_bus(index):
    bus = BusModel.query.filter_by(id=index)[0]
    return jsonify(BusModel.bus_serializer(bus))


# Create new bus
@app.route("/buses", methods=["POST"])
def add_bus():
    bus = request.get_json()
    new_bus = BusModel(**bus)
    print(new_bus)

    db.session.add(new_bus)
    db.session.commit()
    return (bus), 201  # code 201 means created


# Update bus
@app.route("/buses/<int:index>", methods=["PUT"])
def update_bus(index):
    updates = request.get_json()
    bus_to_update = BusModel.query.get(index)
    # bus = BusModel(id=index, **updates)
    # db.session.add(bus)
    # for key in updates:
    #     bus_to_update[key] = updates[key]
    bus_to_update.number_plate = updates["number_plate"]
    bus_to_update.manufacturer = updates["manufacturer"]
    bus_to_update.model = updates["model"]
    bus_to_update.year = updates["year"]
    bus_to_update.capacity = updates["capacity"]
    db.session.commit()
    return (BusModel.bus_serializer(bus_to_update)), 200


# Delete bus
@app.route("/buses/<int:index>", methods=["DELETE"])
def delete_bus(index):
    bus_to_delete = BusModel.query.get(index)
    db.session.delete(bus_to_delete)
    db.session.commit()
    return "", 204


app.run()