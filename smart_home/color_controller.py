import logging
import colorsys
import math

from smart_home.mqtt_client import MQTTClient
from smart_home.utils_lambda import get_payload, get_utc_timestamp, error_response, success_response, get_request_message_id, get_mqtt_topics_from_request, get_friendly_name_from_request


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


class ColorController(object):
    @staticmethod
    def handle_request(request):
        color_hsb = get_payload(request).get("color")

        hue = float(color_hsb.get("hue", 0))
        saturation = color_hsb.get("saturation")
        brightness = color_hsb.get("brightness")

        logger = logging.getLogger()
        logger.info("ColorController: Changing color of '%s' to Hue: %s, Saturation: %s, Brightness: %s",
                    get_friendly_name_from_request(request), hue, saturation, brightness)

        red, green, blue = hsv2rgb(hue, saturation, brightness)

        logger.info("ColorController: Changing color of '%s' to Red: %s, Green: %s, Blue: %s",
                    get_friendly_name_from_request(request), red, green, blue)

        white_bool = False
        red_bool = True if red == 255 else False
        green_bool = True if green == 255 else False
        blue_bool = True if blue == 255 else False

        if red_bool and green_bool and blue_bool:
            white_bool = True
            red_bool = False
            green_bool = False
            blue_bool = False

        mqtt_topic_set, mqtt_topic_get = get_mqtt_topics_from_request(request)
        message_id = get_request_message_id(request)
        resp_payload = MQTTClient.publish_wait_for_resp(
            mqtt_topic_set, {"messageId": message_id, "status": {"powerOn": True, "white": white_bool, "red": red_bool, "green": green_bool, "blue": blue_bool}}, message_id, mqtt_topic_get)

        if resp_payload is None:
            return error_response(request)

        status = resp_payload.get("status")

        hue, saturation, brightness = ColorController.__get_hsb_from_status(
            status)

        if status.get("hue") and status.get("saturation") and status.get("brightness"):
            return ColorController.__response_success(request, hue, saturation, brightness)

        return error_response(request)

    @staticmethod
    def handle_report_state(request, status):
        logger = logging.getLogger()
        logger.info("ColorController: Reporting state of '%s'",
                    get_friendly_name_from_request(request))

        hue, saturation, brightness = ColorController.__get_hsb_from_status(
            status)

        logger.info("ColorController: '%s' has Hue: %s, Saturation: %s, Brightness: %s",
                    get_friendly_name_from_request(request), hue, saturation, brightness)
        return ColorController.__response_success_property(hue, saturation, brightness)

    @staticmethod
    def __get_hsb_from_status(status):
        white_bool = False
        red_bool = False
        green_bool = False
        blue_bool = False

        if status:
            white_bool = status.get("white", False)
            red_bool = status.get("red", False)
            green_bool = status.get("green", False)
            blue_bool = status.get("blue", False)

        r = 255 if red_bool else 0
        g = 255 if green_bool else 0
        b = 255 if blue_bool else 0

        return colorsys.rgb_to_hsv(r, g, b)

    @staticmethod
    def __response_success_property(hue, saturation, brightness):
        return {
            "namespace": "Alexa.ColorController",
            "name": "color",
            "value": {
                "hue": hue,
                "saturation": saturation,
                "brightness": brightness
            },
            "timeOfSample": get_utc_timestamp(),
            "uncertaintyInMilliseconds": 0
        }

    @staticmethod
    def __response_success(request, hue, saturation, brightness):
        payload = {
            "context": {
                "properties": [
                    ColorController.__response_success_property(
                        hue, saturation, brightness)
                ]
            }
        }
        return success_response(request, payload)
