from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask_accepts import responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema, api=api)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
