import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_payload, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request


class PercentageController(object):

    @staticmethod
    def handle_request(request):
        logger = logging.getLogger()
        logger.info("PercentageController: Changing the percentage of '%s' ",
                    get_friendly_name_from_request(request))
        percentage = get_payload(request).get("percentage")
        percentage_delta = get_payload(request).get("percentageDelta")

        if percentage:
            key = "percentage"
            value = int(percentage)
        elif percentage_delta:
            key = "percentageDelta"
            value = int(percentage_delta)

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {key: value}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        percentage = None
        status = resp_payload.get("status")
        if status:
            percentage = status.get("percentage")
            if percentage is not None:
                return PercentageController.__response_success(request, percentage)

        return error_response(request)

    @staticmethod
    def __response_success(request, percentage):
        payload = {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.PercentageController",
                        "name": "percentage",
                        "value": int(percentage),
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    }
                ]
            }
        }
        
        return success_response(request, payload)
