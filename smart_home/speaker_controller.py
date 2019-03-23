import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_payload, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request, get_header_name


class SpeakerController(object):

    @classmethod
    def handle_request(cls, request):
        logger = logging.getLogger()
        logger.info("SpeakerController: Changing volume of '%s' ",
                    get_friendly_name_from_request(request))
        header_name = get_header_name(request)

        value = None
        key = None
        if header_name == "SetVolume":
            key = "SetVolume"
            value = int(get_payload(request).get("volume"))
        if header_name == "AdjustVolume":
            key = "AdjustVolume"
            value = int(get_payload(request).get("volume"))
            
            # Increase the volume with 2, as 1 is too minor
            if value == 10:
                value = 20
        if header_name == "SetMute":
            key = "SetMute"
            value = get_payload(request).get("mute")

        if key is None or value is None:
            return error_response(request)

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {key: value}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        volume = None
        status = resp_payload.get("status")
        if status:
            volume = status.get("volume")
            if volume is not None and volume < 0:
                # -1 is valid value in case we don't know the exact volume
                volume = 0
            muted = status.get("mute")
            return SpeakerController.__response_success(request, volume, muted)

        return error_response(request)

    @staticmethod
    def __response_success(request, volume, muted):
        properties = []
        if volume is not None:
            properties.append({
                "namespace": "Alexa.Speaker",
                "name": "volume",
                "value": volume,
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 500
            })
        if muted is not None:
            properties.append({
                "namespace": "Alexa.Speaker",
                "name": "muted",
                "value": muted,
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 500
            })

        payload = {
            "context": {
                "properties": properties
            }
        }

        return success_response(request, payload)
