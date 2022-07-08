import json
import requests

from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse, Failure
from elg.model.base import StandardMessages

endpoint = "http://localhost:8001/process"


class TnppProxy(FlaskService):

    def process_text(self, request: TextRequest):
        try:
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "type": "text",
                    "content": request.content,
                    "params": request.params}
            payload = json.dumps(payload)
            response = requests.post(
                    endpoint, headers=headers, data=payload)
        except Exception:
            error = StandardMessages.generate_elg_service_internalerror(
                    params=["Error calling remote API"])
            return Failure(errors=[error])
        if response.ok:
            try:
                data = response.json()
                if "response" in data:
                    return AnnotationsResponse(
                            annotations=data["response"]["annotations"])
                if "failure" in data:
                    return Failure(errors=data["failure"]["errors"])
            except Exception:
                error = StandardMessages.generate_elg_service_internalerror(
                        params=["Invalid response from remote API"])
                return Failure(errors=[error])
            error = StandardMessages.generate_elg_service_internalerror(
                    params=["No response or failure from remote API"])
            return Failure(errors=[error])
        else:
            error = StandardMessages.generate_elg_service_internalerror(
                    params=[str(response.status_code)])
            return Failure(errors=[error])


flask_service = TnppProxy("Tnpp-proxy")
app = flask_service.app
