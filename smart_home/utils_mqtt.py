"""
MQTT utils
"""
from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import error_response, get_mqtt_topics_from_request


def get_device_status(request):
    _, mqtt_topic_get = get_mqtt_topics_from_request(request)
    resp_payload = MQTTClient.subscribe_get_message(mqtt_topic_get)

    if resp_payload is None:
        return error_response(request)

    return resp_payload.get("status")
