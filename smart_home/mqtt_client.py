import json
import logging
import os
import ssl
from time import sleep
import time

import paho.mqtt as mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as mqtt_publish
from smart_home.utils_lambda import get_dict_from_bytes


MQTT_SERVER = os.getenv('MQTT_SERVER')  # provided by cloudmqtt
MQTT_PORT = int(os.getenv('MQTT_SERVER_PORT'))  # provided by cloudmqtt
MQTT_USERNAME = os.getenv('MQTT_USERNAME')  # as configured on cloudmqtt
MQTT_PASSWORD = os.getenv('MQTT_PASS')  # as configured on cloudmqtt
MQTT_CLIENT_NAME = os.getenv('MQTT_CLIENT_NAME')
MQTT_TIMEOUT_EXEC = int(os.getenv('MQTT_TIMEOUT_EXEC', "8"))


mqtt_auth = {'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
mqtt_tls = {'tls_version': ssl.PROTOCOL_TLSv1_2, 'ca_certs': 'certs/ca-certificates.crt',
            'certfile': None, 'keyfile': None, 'cert_reqs': ssl.CERT_REQUIRED}


class MQTTClient(object):

    @staticmethod
    def publish(topic, message, qos=1):
        logger = logging.getLogger()
        logger.info("MQTT: Publish [%s]: %s", topic, message)
        if isinstance(message, dict):
            message = json.dumps(message)
        mqtt_publish.single(topic, payload=message, qos=qos, retain=False, client_id=MQTT_CLIENT_NAME,
                            hostname=MQTT_SERVER, port=MQTT_PORT, auth=mqtt_auth, tls=mqtt_tls)

    @staticmethod
    def subscribe_get_message(receive_topic, qos=0, timeout=8):
        return MQTTClient.__publish_subscribe(receive_topic=receive_topic, qos=qos, timeout=timeout)

    @staticmethod
    def publish_wait_for_resp(send_topic, message, message_id, receive_topic, qos=1, timeout=MQTT_TIMEOUT_EXEC):
        return MQTTClient.__publish_subscribe(send_topic=send_topic, message=message, message_id=message_id, receive_topic=receive_topic, qos=qos, timeout=timeout)

    @staticmethod
    def __publish_subscribe(send_topic=None, message=None, message_id=None, receive_topic=None, qos=1, timeout=MQTT_TIMEOUT_EXEC):
        logger = logging.getLogger()
        userdata = []

        def _on_connect(client, userdata, flags, rc):
            """Internal callback"""
            if rc != 0:
                raise mqtt.MQTTException(paho.connack_string(rc))
            client.subscribe(receive_topic, qos)

        def _on_message_callback(client, userdata, msg):
            """Internal callback"""
            payload = get_dict_from_bytes(msg.payload)
            if message_id is None:
                # We are not looking for a specific message, so let's return
                # the latest (retain)
                userdata.append(payload)
                return

            msg_id = payload.get("messageId")
            if msg_id and msg_id == message_id:
                # We are looking for message with id messageId
                logger.debug("Message received with ID %s", message_id)
                userdata.append(payload)

        def _current_time():
            return int(round(time.time()))

        mqttc = paho.Client(clean_session=True,
                            transport="tcp", userdata=userdata)
        mqttc.on_message = _on_message_callback
        mqttc.on_connect = _on_connect
        mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        mqttc.tls_set(**mqtt_tls)

        mqttc.connect(MQTT_SERVER, MQTT_PORT)
        try:
            mqttc.loop_start()
            if send_topic is not None and message is not None:
                logger.info("MQTT: Publish [%s]: %s", send_topic, message)
                # Publish the message

                if isinstance(message, dict):
                    message = json.dumps(message)
                    mqtt_msg = mqttc.publish(send_topic, message, qos=qos)
                    mqtt_msg.wait_for_publish()
            if message_id is None:
                logger.info(
                    "MQTT: Waiting for the latest message from %s", receive_topic)
            else:
                logger.info("MQTT: Waiting for a message with ID %s in %s",
                            message_id, receive_topic)
            timeout_time = _current_time() + timeout
            while not userdata:
                sleep(.01)
                if _current_time() >= timeout_time:
                    logger.error(
                        "MQTT: Timeout during waiting for message with ID %s.", message_id)
                    break

            if len(userdata) >= 1:
                return userdata[0]

            return None  # indicates error
        finally:
            mqttc.loop_stop()
