from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema
from app.udaconnect.services import PersonService
from flask import request, abort, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
import sys
import json

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Persons api.")  # noqa

# TODO: This needs better exception handling


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema, status_code=202, description="Accepted", api=api)
    def post(self) -> Person:
        try:
            payload = request.get_json()
            new_person: Person = PersonService.create_person(payload)
            return Response(json.dumps({
                "id": payload["id"],
                "first_name": payload["first_name"],
                "last_name": payload["last_name"],
                "company_name": payload["company_name"]
            }), 202)
        except Exception as err:
            print(sys.exc_info())
            abort(Response(err), 422)

    @responds(schema=PersonSchema, many=True, api=api)
    def get(self) -> List[Person]:
        try:
            persons: List[Person] = PersonService.retrieve_all()
            return persons
        except Exception as err:
            print(sys.exc_info())
            abort(Response(err), 501)


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema, api=api)
    def get(self, person_id) -> Person:
        try:
            person: Person = PersonService.retrieve(person_id)
            return person
        except Exception as err:
            print(sys.exc_info())
            abort(Response(err), 501)
