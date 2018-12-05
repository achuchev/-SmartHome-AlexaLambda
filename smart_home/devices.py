DEVICES = [
    {
        "endpointId": "LivingRoomAC",
        "friendlyName": "Air Conditioner Living Room",
        "manufacturerName": "Daikin AC",
        "description": "Air conditioner in living room",
        "displayCategories": [
            "THERMOSTAT"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/livingRoom/ac",
            "mqttTopicSet": "set/apartment/livingRoom/ac"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.ThermostatController",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "targetSetpoint"
                        }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                },
                "configuration": {
                    "supportsScheduling": False,
                    "supportedModes": [
                        "HEAT",
                        "COOL",
                        "AUTO"
                    ]
                }
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.TemperatureSensor",
                "version": "3",
                "properties": {
                    "supported": [
                        {
                            "name": "temperature"
                        }
                    ],
                    "proactivelyReported": False,
                    "retrievable": False
                }
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    #     {
    #         "endpointId": "LargeBedroomHeater2",
    #         "friendlyName": "Heater Two Large Bedroom",
    #         "description": "The second heater in the large bedroom",
    #         "manufacturerName": "Adax",
    #         "displayCategories": [
    #             "THERMOSTAT"
    #         ],
    #         "metadata": {
    #             "mqttTopicGet": "get/apartment/largeBedroom/heater/2",
    #             "mqttTopicSet": "set/apartment/largeBedroom/heater/2"
    #         },
    #         "capabilities": [
    #             {
    #                 "interface": "Alexa.PowerController",
    #                 "properties": {
    #                     "proactivelyReported": False,
    #                     "retrievable": False,
    #                     "supported": [
    #                         {
    #                             "name": "powerState"
    #                         }
    #                     ]
    #                 },
    #                 "type": "AlexaInterface",
    #                 "version": "3"
    #             },
    #             {
    #                 "type": "AlexaInterface",
    #                 "interface": "Alexa.ThermostatController",
    #                 "version": "3",
    #                 "properties": {
    #                     "supported": [
    #                         {
    #                             "name": "targetSetpoint"
    #                         }
    #                     ],
    #                     "proactivelyReported": False,
    #                     "retrievable": False
    #                 }
    #             },
    #             {
    #                 "interface": "Alexa",
    #                 "type": "AlexaInterface",
    #                 "version": "3"
    #             }
    #         ]
    #     },
    {
        "endpointId": "SmallBedroomWindow",
        "friendlyName": "Window Small Bedroom",
        "description": "Sunblind for the window in the small bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/smallBedroom/sunblind/1",
            "mqttTopicSet": "set/apartment/smallBedroom/sunblind/1"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LargeBedroomWindowSunblind1",
        "friendlyName": "Door 1 Large Bedroom",
        "description": "Sunblind for the door in the large bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/largeBedroom/sunblind/1",
            "mqttTopicSet": "set/apartment/largeBedroom/sunblind/1"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LargeBedroomWindow2",
        "friendlyName": "Window 2 Large Bedroom",
        "description": "Sunblind for the second window in the large bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/largeBedroom/sunblind/2",
            "mqttTopicSet": "set/apartment/largeBedroom/sunblind/2"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LargeBedroomWindow3",
        "friendlyName": "Window 3 Large Bedroom",
        "description": "Sunblind for the third window in the large bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/largeBedroom/sunblind/3",
            "mqttTopicSet": "set/apartment/largeBedroom/sunblind/3"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LargeBedroomWindow4",
        "friendlyName": "Window 4 Large Bedroom",
        "description": "Sunblind for the fourth window in the large bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/largeBedroom/sunblind/4",
            "mqttTopicSet": "set/apartment/largeBedroom/sunblind/4"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LargeBedroomWindowAll",
        "friendlyName": "All Windows Large Bedroom",
        "description": "Sunblinds for all windows in the large bedroom",
        "manufacturerName": "Somfy",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/largeBedroom/sunblind/all",
            "mqttTopicSet": "set/apartment/largeBedroom/sunblind/all"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LivingRoomTV",
        "friendlyName": "TV Living Room",
        "description": "TV in the living room",
        "manufacturerName": "Samsung",
        "displayCategories": ["TV"],
        "metadata": {
            "mqttTopicGet": "get/apartment/livingRoom/tv",
            "mqttTopicSet": "set/apartment/livingRoom/tv"
        },
        "capabilities": [
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": False,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa.ChannelController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": False,
                    "supported": [
                        {
                            "name": "channel"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa.Speaker",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": False,
                    "supported": [
                        {
                            "name": "volume"
                        },
                        {
                            "name": "muted"
                        }
                    ]

                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa.PlaybackController",
                "supportedOperations": ["Play", "Pause", "Stop"],
                "type": "AlexaInterface",
                "version": "3",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": False, }
            }

        ]
    },
    {
        "endpointId": "ApartmentLock",
        "friendlyName": "Apartment Lock",
        "description": "Alarm system of Apartment zone",
        "manufacturerName": "Paradox",
        "displayCategories": [
            "SMARTLOCK"
        ],
        "metadata": {
            "mqttTopicGet": "get/home/lock",
            "mqttTopicSet": "set/home/lock"
        },
        "capabilities": [
            {
                "interface": "Alexa.LockController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "lockState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "GarageLock",
        "friendlyName": "Garage Lock",
        "description": "Alarm system of Garage zone",
        "manufacturerName": "Paradox",
        "displayCategories": [
            "SMARTLOCK"
        ],
        "metadata": {
            "mqttTopicGet": "get/home/lock",
            "mqttTopicSet": "set/home/lock"
        },
        "capabilities": [
            {
                "interface": "Alexa.LockController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "lockState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "BathroomVentilation",
        "friendlyName": "Bathroom Ventilation",
        "description": "Ventilation system of Bathroom",
        "manufacturerName": "MM motors",
        "displayCategories": [
            "SWITCH"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/bathroom/fan",
            "mqttTopicSet": "set/apartment/bathroom/fan"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "BathroomLamp",
        "friendlyName": "Lamp Bathroom",
        "description": "Lamp in the bathroom",
        "manufacturerName": "LED",
        "displayCategories": [
            "LIGHT"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/bathroom/lamp",
            "mqttTopicSet": "set/apartment/bathroom/lamp"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LivingRoomLampBig",
        "friendlyName": "Lamp Big Living Room",
        "description": "Lamp Big in the living room",
        "manufacturerName": "Regular lamp",
        "displayCategories": [
            "LIGHT"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/livingRoom/lamp/1",
            "mqttTopicSet": "set/apartment/livingRoom/lamp/1"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LivingRoomLampSmall",
        "friendlyName": "Lamp Small Living Room",
        "description": "Lamp Small in the living room",
        "manufacturerName": "Regular lamp",
        "displayCategories": [
            "LIGHT"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/livingRoom/lamp/2",
            "mqttTopicSet": "set/apartment/livingRoom/lamp/2"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    },
    {
        "endpointId": "LivingRoomLampLed",
        "friendlyName": "LED Lamp Living Room",
        "description": "LED Lamp in the living room",
        "manufacturerName": "LED",
        "displayCategories": [
            "LIGHT"
        ],
        "metadata": {
            "mqttTopicGet": "get/apartment/livingRoom/lamp/3",
            "mqttTopicSet": "set/apartment/livingRoom/lamp/3"
        },
        "capabilities": [
            {
                "interface": "Alexa.PowerController",
                "properties": {
                    "proactivelyReported": False,
                    "retrievable": True,
                    "supported": [
                        {
                            "name": "powerState"
                        }
                    ]
                },
                "type": "AlexaInterface",
                "version": "3"
            },
            {
                "interface": "Alexa",
                "type": "AlexaInterface",
                "version": "3"
            }
        ]
    }
]
