import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_payload, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request


class ThermostatController(object):
    @staticmethod
    def handle_request(request):
        logger = logging.getLogger()
        logger.info("ThermostatController: Changing temperature or mode of '%s' ",
                    get_friendly_name_from_request(request))
        target_setpoint = get_payload(request).get("targetSetpoint")
        target_setpoint_delta = get_payload(request).get("targetSetpointDelta")
        thermostat_mode = get_payload(request).get("thermostatMode")
        if target_setpoint:
            key = "temp"
            value = int(target_setpoint["value"])
        elif target_setpoint_delta:
            key = "tempDelta"
            value = int(target_setpoint_delta["value"])
        elif thermostat_mode:
            key = "mode"
            value = thermostat_mode["value"]

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {key: value}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        current_setpoint = None
        current_mode = None
        status = resp_payload.get("status")
        if status:
            if thermostat_mode is not None:
                current_mode = status.get("mode")
            if target_setpoint is not None or target_setpoint_delta is not None:
                current_setpoint = status.get("temp")

        return ThermostatController.__response_success(request, current_setpoint, current_mode)

    @staticmethod
    def handle_report_state(request, status):
        logger = logging.getLogger()
        logger.info("PowerController: Reporting state of '%s'",
                    get_friendly_name_from_request(request))

        current_setpoint = None
        current_mode = None
        
        if status:
            current_mode = status.get("mode")
            current_setpoint = status.get("temp")

        logger.info("PowerController: '%s' has mode  %s ",
                    get_friendly_name_from_request(request), current_mode)
        return ThermostatController.__response_success_properties(current_setpoint, current_mode)

    @staticmethod
    def __response_success_properties(current_setpoint=None, current_mode=None):

        properties = []
        if current_setpoint is not None:
            properties.append({
                "namespace": "Alexa.ThermostatController",
                "name": "targetSetpoint",
                "value": {
                    "value": int(current_setpoint),
                    "scale": "CELSIUS"
                },
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 0
            })
        if current_mode is not None:
            properties.append({
                "namespace": "Alexa.ThermostatController",
                "name": "thermostatMode",
                "value": current_mode.upper(),
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 0
            })
        return properties

    @staticmethod
    def __response_success(request, current_setpoint=None, current_mode=None):
        payload = {
            "context": {
                "properties": ThermostatController.__response_success_properties(current_setpoint=current_setpoint, current_mode=current_mode)
            }
        }
        return success_response(request, payload)
