import sys
from datetime import datetime
from app.udaconnect.schemas import ConnectionSchema
from app.udaconnect.services import ConnectionService
from flask import request, abort, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections api.")  # noqa


# TODO: This needs better exception handling


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        try:
            start_date: datetime = datetime.strptime(
                request.args["start_date"], DATE_FORMAT
            )
            end_date: datetime = datetime.strptime(
                request.args["end_date"], DATE_FORMAT)
            distance: Optional[int] = request.args.get("distance", 5)

            results = ConnectionService.find_contacts(
                person_id=person_id,
                start_date=start_date,
                end_date=end_date,
                meters=distance,
            )
            if len(results) == 0:
                abort(404)
            return results
        except Exception as err:
            print(sys.exc_info())
            abort(Response(err), 422)
        return results
