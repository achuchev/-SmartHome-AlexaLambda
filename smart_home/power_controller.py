import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_request_message_id, get_mqtt_topics_from_request, get_request_name, get_friendly_name_from_request


class PowerController(object):
    @staticmethod
    def handle_request(request):
        power_on_desired_state = False
        if get_request_name(request) == "TurnOn":
            power_on_desired_state = True

        logger = logging.getLogger()
        logger.info("PowerController: Changing power state of '%s' to PowerOn %s ",
                    get_friendly_name_from_request(request), power_on_desired_state)

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {"powerOn": power_on_desired_state}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        current_power_on = False
        status = resp_payload.get("status")
        if status:
            current_power_on = status.get("powerOn")

        if current_power_on == power_on_desired_state:
            return PowerController.__response_success(request, current_power_on)

        return error_response(request)

    @staticmethod
    def handle_report_state(request, status):
        logger = logging.getLogger()
        logger.info("PowerController: Reporting state of '%s'",
                    get_friendly_name_from_request(request))

        if status:
            current_power_on = status.get("powerOn")

        logger.info("PowerController: '%s' has PowerOn  %s ",
                    get_friendly_name_from_request(request), current_power_on)
        return PowerController.__response_success_property(current_power_on)

    @staticmethod
    def __response_success_property(current_power_on):
        return {
            "namespace": "Alexa.PowerController",
            "name": "powerState",
            "value": "ON" if current_power_on else "OFF",
            "timeOfSample": get_utc_timestamp(),
            "uncertaintyInMilliseconds": 500
        }

    @staticmethod
    def __response_success(request, current_power_on):
        payload = {
            "context": {
                "properties": [
                    PowerController.__response_success_property(
                        current_power_on)
                ]
            }
        }
        return success_response(request, payload)
