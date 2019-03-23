# -*- coding: utf-8 -*-
import json
import logging
import os

from smart_home.channel_controller import ChannelController
from smart_home.devices import DEVICES
from smart_home.percentage_controller import PercentageController
from smart_home.power_controller import PowerController
from smart_home.thermostat_controller import ThermostatController
from smart_home.utils_lambda import get_uuid, get_directive_version
from validation import validate_message
from smart_home.speaker_controller import SpeakerController
from smart_home.playback_controller import PlaybackController
from smart_home.color_controller import ColorController
from smart_home.lock_controller import LockController
from smart_home.utils_lambda import report_state_success
from smart_home.utils_mqtt import get_device_status

# Setup logger
logger = logging.getLogger()
logger.setLevel(eval(os.getenv('DEBUG_LEVEL')))


def lambda_handler(request, context):
    """Main Lambda handler"""
    try:
        logger.debug("Directive:")
        logger.debug(json.dumps(request, indent=4, sort_keys=True))

        version = get_directive_version(request)

        if version != "3":
            raise Exception(
                "Unsupported Directive version '%s'! We support only version 3" % version)

        if request["directive"]["header"]["name"] == "Discover":
            # handle discovery
            response = handle_discovery(request)
        else:
            # handle other requests
            response = handle_non_discovery(request)

        logger.debug("Response:")
        logger.debug(json.dumps(response, indent=4, sort_keys=True))

        # Validate v3 response
        # FIXME: Add PlaybackController in the JSON schema
        #validate_message(request, response)
        return response
    except ValueError as error:
        logger.error(error)
        raise


def handle_discovery(request):
    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": get_uuid()
            },
            "payload": {
                "endpoints": DEVICES
            }
        }
    }
    return response


def handle_non_discovery(request):
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]
    endpoint_id = request["directive"].get(
        "endpoint", {"endpointId": None})["endpointId"]

    logger.info("Endpoint ID '%s', namespace: '%s', name '%s' ",
                endpoint_id, request_namespace, request_name)

    if request_namespace == "Alexa.PowerController":
        return PowerController.handle_request(request)
    elif request_namespace == "Alexa.ThermostatController":
        return ThermostatController.handle_request(request)
    elif request_namespace == "Alexa.PercentageController":
        return PercentageController.handle_request(request)
    elif request_namespace == "Alexa.ChannelController":
        return ChannelController.handle_request(request)
    elif request_namespace == "Alexa.Speaker":
        return SpeakerController.handle_request(request)
    elif request_namespace == "Alexa.PlaybackController":
        return PlaybackController.handle_request(request)
    elif request_namespace == "Alexa.LockController":
        return LockController.handle_request(request)
    elif request_namespace == "Alexa.ColorController":
        return ColorController.handle_request(request)
    elif request_namespace == "Alexa" and request_name == "ReportState":
        return __handle_report_state(request)
    elif request_namespace == "Alexa.Authorization":
        if request_name == "AcceptGrant":
            response = {
                "event": {
                    "header": {
                        "namespace": "Alexa.Authorization",
                        "name": "AcceptGrant.Response",
                        "payloadVersion": "3",
                        "messageId": "5f8a426e-01e4-4cc9-8b79-65f8bd0fd8a4"
                    },
                    "payload": {}
                }
            }
            return response
    else:
        raise Exception("Unknown request namespace '%s' for request name '%s' and endpoint ID '%s'." % (
            request_namespace, request_name, endpoint_id))


def __handle_report_state(request):

    endpoint_id = request["directive"].get(
        "endpoint", {"endpointId": None})["endpointId"]

    interfaces = []
    for device in DEVICES:
        if device["endpointId"] == endpoint_id:
            for capability in device["capabilities"]:
                if capability["interface"] is not "Alexa" and capability["properties"]["retrievable"]:
                    interfaces.append(capability["interface"])
            break
    logger.info("Endpoint ID '%s', interfaces: '%s'", endpoint_id, interfaces)

    status = get_device_status(request)

    properties = []
    for interface in interfaces:
        if interface == "Alexa.PowerController":
            properties.append(
                PowerController.handle_report_state(request, status))
        elif interface == "Alexa.ThermostatController":
            properties.extend(
                ThermostatController.handle_report_state(request, status))
        elif interface == "Alexa.LockController":
            properties.append(
                LockController.handle_report_state(request, status))
        elif interface == "Alexa.ColorController":
            properties.append(
                ColorController.handle_report_state(request, status))

    return report_state_success(request, properties)
