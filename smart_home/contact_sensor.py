import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_request_message_id, get_mqtt_topics_from_request, get_friendly_name_from_request


class ContactSensor(object):
    @staticmethod
    def handle_request(request):
        logger = logging.getLogger()
        logger.info("ContactSensor: Reporting state of %s contact sensor.",
                    get_friendly_name_from_request(request))

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        status = resp_payload.get("status")
        if status:
            detection_state = status.get("door")

        if detection_state:
            return ContactSensor.__response_success(request, detection_state)

        return error_response(request)

    @staticmethod
    def handle_report_state(request, status):
        logger = logging.getLogger()

        if status:
            detection_state = status.get("door")


        logger.info("ContactSensor: '%s' has state  %s ",
                    get_friendly_name_from_request(request), detection_state)
        return ContactSensor.__response_success_property(detection_state)

    @staticmethod
    def __response_success_property(detection_state):
        return {
            "namespace": "Alexa.ContactSensor",
            "name": "detectionState",
            "value": "NOT_DETECTED" if (detection_state == "closed") else "DETECTED",
            "timeOfSample": get_utc_timestamp(),
            "uncertaintyInMilliseconds": 0
        }

    @staticmethod
    def __response_success(request, detection_state):
        payload = {
            "context": {
                "properties": [
                    ContactSensor.__response_success_property(
                        detection_state)
                ]
            }
        }
        return success_response(request, payload)
