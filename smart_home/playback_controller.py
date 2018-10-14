import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import error_response, success_response, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request, get_header_name


class PlaybackController(object):

    @classmethod
    def handle_request(cls, request):
        logger = logging.getLogger()
        header_name = get_header_name(request)
        logger.info("PlaybackController: Action '%s' on '%s' ", header_name,
                    get_friendly_name_from_request(request))

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {"playbackAction": header_name}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        status = resp_payload.get("status")
        if status:
            return PlaybackController.__response_success(request)

        return error_response(request)

    @staticmethod
    def __response_success(request):
        return success_response(request, {})
