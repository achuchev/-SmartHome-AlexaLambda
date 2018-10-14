import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request, get_header_name


class LockController(object):
    @staticmethod
    def handle_request(request):
        logger = logging.getLogger()
        logger.info("LockController: Locking area with name '%s' ",
                    get_friendly_name_from_request(request))
        key = ""
        value = ""
        if get_header_name(request) == "Lock":
            key = "arm"
            value = get_friendly_name_from_request(request)
            # The friendly name is "Apartment Lock", but we just need
            # "Apartment"
            value = value.split(' ')[0]
        elif get_header_name(request) == "Unlock":
            # We don't want to support unlock
            return error_response(request)

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {key: value}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        status = resp_payload.get("status")

        if not status:
            return error_response(request)
        areasStatus = status.get("areasStatus")

        if areasStatus:
            logger.info(areasStatus)

            areaStatusName = None
            for area in areasStatus:
                if area.get("name") == value:
                    areaStatusName = area.get("statusName")
                    break
            if key == "arm" and areaStatusName == "armed":
                return LockController.__response_success(request, "LOCKED")

        return error_response(request)

    @staticmethod
    def handle_report_state(request, status):
        logger = logging.getLogger()
        logger.info("LockController: Reporting state of '%s'",
                    get_friendly_name_from_request(request))

        area_status_name = None
        if status:
            areas_status = status.get("areasStatus")

            if areas_status:
                logger.debug("LockController: Areas status: %s ", areas_status)

                area_name = get_friendly_name_from_request(request)
                # The friendly name is "Apartment Lock", but we just need
                # "Apartment"
                area_name = area_name.split(' ')[0]

                for area in areas_status:
                    if area.get("name") == area_name:
                        area_status_name = area.get("statusName")
                        break
                logger.debug("LockController: Area '%s' has status '%s'", area_name, area_status_name)
                
                if area_status_name == "armed":
                    area_status_name = "LOCKED"
                else:
                    area_status_name = "UNLOCKED"

        logger.info("LockController: '%s' has state  %s ",
                    get_friendly_name_from_request(request), area_status_name)

        return LockController.__response_success_property(area_status_name)

    @staticmethod
    def __response_success_property(lockState):
        return {
            "namespace": "Alexa.LockController",
            "name": "lockState",
                    "value": lockState,
                    "timeOfSample": get_utc_timestamp(),
                    "uncertaintyInMilliseconds": 500
        }

    @staticmethod
    def __response_success(request, lockState):
        payload = {
            "context": {
                "properties": [
                    LockController.__response_success_property(lockState)
                ]
            }
        }
        return success_response(request, payload)
