SCHEMA = {
  "typeName" : "AWS::MediaLive::Input",
  "description" : "Resource Type definition for AWS::MediaLive::Input",
  "additionalProperties" : False,
  "properties" : {
    "SrtSettings" : {
      "$ref" : "#/definitions/SrtSettingsRequest"
    },
    "InputNetworkLocation" : {
      "type" : "string"
    },
    "Destinations" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/InputDestinationRequest"
      }
    },
    "Vpc" : {
      "$ref" : "#/definitions/InputVpcRequest"
    },
    "MediaConnectFlows" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/MediaConnectFlowRequest"
      }
    },
    "Sources" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/InputSourceRequest"
      }
    },
    "RoleArn" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "Type" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "InputSecurityGroups" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "MulticastSettings" : {
      "$ref" : "#/definitions/MulticastSettingsCreateRequest"
    },
    "InputDevices" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/InputDeviceSettings"
      }
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "SrtCallerSourceRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SrtListenerPort" : {
          "type" : "string"
        },
        "StreamId" : {
          "type" : "string"
        },
        "MinimumLatency" : {
          "type" : "integer"
        },
        "Decryption" : {
          "$ref" : "#/definitions/SrtCallerDecryptionRequest"
        },
        "SrtListenerAddress" : {
          "type" : "string"
        }
      }
    },
    "SrtCallerDecryptionRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Algorithm" : {
          "type" : "string"
        },
        "PassphraseSecretArn" : {
          "type" : "string"
        }
      }
    },
    "InputSourceRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PasswordParam" : {
          "type" : "string"
        },
        "Username" : {
          "type" : "string"
        },
        "Url" : {
          "type" : "string"
        }
      }
    },
    "MulticastSettingsCreateRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Sources" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/MulticastSourceCreateRequest"
          }
        }
      }
    },
    "InputDeviceSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Id" : {
          "type" : "string"
        }
      }
    },
    "InputDestinationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StreamName" : {
          "type" : "string"
        },
        "NetworkRoutes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/InputRequestDestinationRoute"
          }
        },
        "StaticIpAddress" : {
          "type" : "string"
        },
        "Network" : {
          "type" : "string"
        }
      }
    },
    "SrtSettingsRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SrtCallerSources" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/SrtCallerSourceRequest"
          }
        }
      }
    },
    "InputVpcRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "InputRequestDestinationRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Cidr" : {
          "type" : "string"
        },
        "Gateway" : {
          "type" : "string"
        }
      }
    },
    "MediaConnectFlowRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FlowArn" : {
          "type" : "string"
        }
      }
    },
    "MulticastSourceCreateRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Url" : {
          "type" : "string"
        },
        "SourceIp" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/Vpc", "/properties/Type", "/properties/InputNetworkLocation" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}