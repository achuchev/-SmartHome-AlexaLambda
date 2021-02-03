"""
Lambda utils
"""
import time
import uuid
import copy
import json
from smart_home.devices import DEVICES


def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))


def get_uuid():
    return str(uuid.uuid4())


def get_directive_version(request):
    try:
        return request["directive"]["header"]["payloadVersion"]
    except:
        try:
            return request["header"]["payloadVersion"]
        except:
            return "-1"


def get_endpoint_by_id(endpoint_id):
    for endpoint in DEVICES:
        if endpoint["endpointId"] == endpoint_id:
            return endpoint
    raise Exception("Endpoint with ID '%s' not found." % endpoint_id)


def get_endpoint_id(request):
    return request["directive"].get("endpoint", {"endpointId": None})["endpointId"]


def get_request_token(request):
    return request["directive"].get("endpoint", {"endpointId": None})["scope"]["token"]


def get_header(request):
    return request["directive"]["header"]


def get_header_name(request):
    return get_header(request)["name"]


def get_correlation_token(request):
    return get_header(request)["correlationToken"]


def get_request_name(request):
    return get_header(request)["name"]


def get_request_message_id(request):
    return get_header(request)["messageId"]


def get_payload(request):
    return request["directive"]["payload"]


def get_friendly_name_from_request(request):
    return get_endpoint_by_id(get_endpoint_id(request))["friendlyName"]


def get_mqtt_topics_from_request(request):
    endpoint = get_endpoint_by_id(get_endpoint_id(request))
    mqtt_topic_set = endpoint["metadata"]["mqttTopicSet"]
    mqtt_topic_get = endpoint["metadata"]["mqttTopicGet"]
    return (mqtt_topic_set, mqtt_topic_get)


def success_response(request, payload):
    resp = copy.copy(payload)

    resp["event"] = {
        "header": {
            "namespace": "Alexa",
            "name": "Response",
            "payloadVersion": "3",
            "messageId": get_uuid(),
            "correlationToken": get_correlation_token(request)
        },
        "endpoint": {
            "scope": {
                "type": "BearerToken",
                "token": get_request_token(request)
            },
            "endpointId": get_endpoint_id(request)
        },
        "payload": {}
    }
    return resp


def report_state_success(request, properties):

    endpoint_health = {
        "namespace": "Alexa.EndpointHealth",
        "name": "connectivity",
        "value": {
                "value": "OK"
        },
        "timeOfSample": get_utc_timestamp(),
        "uncertaintyInMilliseconds": 0
    }

    properties.append(endpoint_health)

    resp = {
        "context": {
            "properties": properties
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "StateReport",
                "payloadVersion": "3",
                "messageId": get_uuid(),
                "correlationToken": get_correlation_token(request)
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": get_request_token(request)
                },
                "endpointId": get_endpoint_id(request)
            },
            "payload": {}
        }
    }
    return resp


def error_response(request, error_type="ENDPOINT_UNREACHABLE", error_message=None):
    if error_type == "ENDPOINT_UNREACHABLE" and error_message is None:
        error_message = "Unable to reach endpoint {} because it appears to be offline".format(
            get_endpoint_id(request))

    return {
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "ErrorResponse",
                "messageId": get_uuid(),
                "correlationToken": get_correlation_token(request),
                "payloadVersion": "3"
            },
            "endpoint": {
                "endpointId": get_endpoint_id(request)
            },
            "payload": {
                "type": "ENDPOINT_UNREACHABLE",
                "message": error_message
            }
        }
    }


def get_dict_from_bytes(data):
    return json.loads(data.decode("ASCII"))
