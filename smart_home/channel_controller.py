import logging

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_utc_timestamp, error_response, success_response, get_payload, get_request_message_id, get_mqtt_topics_from_request,\
    get_friendly_name_from_request, get_header_name


class ChannelController(object):
    channel_lists = {"fox life": 8,
                     "fox": 9,
                     "nova": 2,
                     "nova tv": 2,
                     "btv": 4,
                     "b. t. v. ": 4,
                     "btv comedy": 5,
                     "b. t. v. comedy": 5,
                     "b. t. v. comedies": 5,
                     "b. e. t. v. comedies": 5,
                     "btv cinema": 6,
                     "travel channel": 11,
                     "travel": 11,
                     "the discovery channel": 10,
                     "discovery channel": 10,
                     "discovery": 10}

    @classmethod
    def handle_request(cls, request):
        logger = logging.getLogger()
        logger.info("ChannelController: Changing the TV settings of '%s' ",
                    get_friendly_name_from_request(request))
        header_name = get_header_name(request)
        channel_number = None
        channel_metadata_name = None
        value = None
        key = None
        if header_name == "SkipChannels":
            key = "skipChannels"
            value = int(get_payload(request).get("channelCount"))
        if header_name == "ChangeChannel":
            channel_number = get_payload(request).get("channel").get("number")
            channel_metadata_name = get_payload(
                request).get("channelMetadata").get("name")

            key = "changeChannel"
            if channel_number is not None:
                value = int(channel_number)
            elif channel_metadata_name is not None:
                value_tmp = cls.channel_lists.get(
                    channel_metadata_name.lower())
                if value_tmp is not None:
                    value = value_tmp

        if key is None or value is None:
            return error_response(request)

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {key: value}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        channel_number = None
        status = resp_payload.get("status")
        if status:
            channel_number = status.get("channelNumber")
            if channel_number is not None:
                return ChannelController.__response_success(request, channel_number)

        return error_response(request)

    @staticmethod
    def __response_success(request, channel_number):
        payload = {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.ChannelController",
                        "name": "channel",
                        "value": {
                            "number": str(channel_number)
                        },
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    }
                ]
            }
        }

        return success_response(request, payload)
