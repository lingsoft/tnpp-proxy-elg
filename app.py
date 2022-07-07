import json
import requests

from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse, Failure
from elg.model.base import StandardMessages

endpoint = "http://localhost:8001/process"


class TnppProxy(FlaskService):

    def process_text(self, request: TextRequest):
        headers = {'Content-Type': 'application/json'}
        payload = {
                "type": "text",
                "content": request.content,
                "params": request.params}
        payload = json.dumps(payload)
        try:
            response = requests.post(
                    endpoint, headers=headers, data=payload)
        except Exception:
            error = StandardMessages.generate_elg_service_internalerror(
                    params=["Error calling remote API"])
            return Failure(errors=[error])
        if response.ok:
            data = response.json()
            if "response" in data:
                return AnnotationsResponse(
                        annotations=data["response"]["annotations"])
            if "failure" in data:
                return Failure(errors=data["failure"]["errors"])
            return "xxx"
        else:
            error = StandardMessages.generate_elg_service_internalerror(
                    params=[str(response.status_code)])
            return Failure(errors=[error])


flask_service = TnppProxy("Tnpp-proxy")
app = flask_service.app
