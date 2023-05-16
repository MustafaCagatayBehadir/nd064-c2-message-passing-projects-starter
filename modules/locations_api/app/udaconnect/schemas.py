from app.udaconnect.models import Location
from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")

    class Meta:
        model = Location
