SCHEMA = {
  "typeName" : "AWS::GroundStation::Config",
  "description" : "AWS Ground Station config resource type for CloudFormation.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ground-station.git",
  "definitions" : {
    "JsonString" : {
      "type" : "string",
      "pattern" : "^[{}\\[\\]:.,\"0-9A-z\\-_\\s]{1,8192}$"
    },
    "ConfigData" : {
      "type" : "object",
      "minProperties" : 1,
      "maxProperties" : 1,
      "properties" : {
        "AntennaDownlinkConfig" : {
          "$ref" : "#/definitions/AntennaDownlinkConfig"
        },
        "TrackingConfig" : {
          "$ref" : "#/definitions/TrackingConfig"
        },
        "DataflowEndpointConfig" : {
          "$ref" : "#/definitions/DataflowEndpointConfig"
        },
        "AntennaDownlinkDemodDecodeConfig" : {
          "$ref" : "#/definitions/AntennaDownlinkDemodDecodeConfig"
        },
        "AntennaUplinkConfig" : {
          "$ref" : "#/definitions/AntennaUplinkConfig"
        },
        "UplinkEchoConfig" : {
          "$ref" : "#/definitions/UplinkEchoConfig"
        },
        "S3RecordingConfig" : {
          "$ref" : "#/definitions/S3RecordingConfig"
        }
      },
      "additionalProperties" : False
    },
    "EirpUnits" : {
      "type" : "string",
      "enum" : [ "dBW" ]
    },
    "Eirp" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "number"
        },
        "Units" : {
          "$ref" : "#/definitions/EirpUnits"
        }
      },
      "additionalProperties" : False
    },
    "FrequencyUnits" : {
      "type" : "string",
      "enum" : [ "GHz", "MHz", "kHz" ]
    },
    "BandwidthUnits" : {
      "type" : "string",
      "enum" : [ "GHz", "MHz", "kHz" ]
    },
    "FrequencyBandwidth" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "number"
        },
        "Units" : {
          "$ref" : "#/definitions/BandwidthUnits"
        }
      },
      "additionalProperties" : False
    },
    "Frequency" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "number"
        },
        "Units" : {
          "$ref" : "#/definitions/FrequencyUnits"
        }
      },
      "additionalProperties" : False
    },
    "Polarization" : {
      "type" : "string",
      "enum" : [ "LEFT_HAND", "RIGHT_HAND", "NONE" ]
    },
    "S3KeyPrefix" : {
      "type" : "string",
      "pattern" : "^([a-zA-Z0-9_\\-=/]|\\{satellite_id\\}|\\{config\\-name}|\\{s3\\-config-id}|\\{year\\}|\\{month\\}|\\{day\\}){1,900}$"
    },
    "BucketArn" : {
      "type" : "string",
      "pattern" : "^arn:aws[A-Za-z0-9-]{0,64}:s3:::[A-Za-z0-9-]{1,64}$"
    },
    "RoleArn" : {
      "type" : "string",
      "pattern" : "^arn:[^:\\n]+:iam::[^:\\n]+:role\\/.+$"
    },
    "UplinkSpectrumConfig" : {
      "type" : "object",
      "properties" : {
        "CenterFrequency" : {
          "$ref" : "#/definitions/Frequency"
        },
        "Polarization" : {
          "$ref" : "#/definitions/Polarization"
        }
      },
      "additionalProperties" : False
    },
    "SpectrumConfig" : {
      "type" : "object",
      "properties" : {
        "CenterFrequency" : {
          "$ref" : "#/definitions/Frequency"
        },
        "Bandwidth" : {
          "$ref" : "#/definitions/FrequencyBandwidth"
        },
        "Polarization" : {
          "$ref" : "#/definitions/Polarization"
        }
      },
      "additionalProperties" : False
    },
    "AntennaDownlinkConfig" : {
      "type" : "object",
      "properties" : {
        "SpectrumConfig" : {
          "$ref" : "#/definitions/SpectrumConfig"
        }
      },
      "additionalProperties" : False
    },
    "TrackingConfig" : {
      "type" : "object",
      "properties" : {
        "Autotrack" : {
          "type" : "string",
          "enum" : [ "REQUIRED", "PREFERRED", "REMOVED" ]
        }
      },
      "additionalProperties" : False
    },
    "DataflowEndpointConfig" : {
      "type" : "object",
      "properties" : {
        "DataflowEndpointName" : {
          "type" : "string"
        },
        "DataflowEndpointRegion" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "DemodulationConfig" : {
      "type" : "object",
      "properties" : {
        "UnvalidatedJSON" : {
          "$ref" : "#/definitions/JsonString"
        }
      },
      "additionalProperties" : False
    },
    "DecodeConfig" : {
      "type" : "object",
      "properties" : {
        "UnvalidatedJSON" : {
          "$ref" : "#/definitions/JsonString"
        }
      },
      "additionalProperties" : False
    },
    "AntennaDownlinkDemodDecodeConfig" : {
      "type" : "object",
      "properties" : {
        "SpectrumConfig" : {
          "$ref" : "#/definitions/SpectrumConfig"
        },
        "DemodulationConfig" : {
          "$ref" : "#/definitions/DemodulationConfig"
        },
        "DecodeConfig" : {
          "$ref" : "#/definitions/DecodeConfig"
        }
      },
      "additionalProperties" : False
    },
    "AntennaUplinkConfig" : {
      "type" : "object",
      "properties" : {
        "SpectrumConfig" : {
          "$ref" : "#/definitions/UplinkSpectrumConfig"
        },
        "TargetEirp" : {
          "$ref" : "#/definitions/Eirp"
        },
        "TransmitDisabled" : {
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "UplinkEchoConfig" : {
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "AntennaUplinkConfigArn" : {
          "type" : "string",
          "pattern" : "^(arn:(aws[a-zA-Z-]*)?:[a-z0-9-.]+:.*)|()$"
        }
      },
      "additionalProperties" : False
    },
    "S3RecordingConfig" : {
      "type" : "object",
      "properties" : {
        "BucketArn" : {
          "$ref" : "#/definitions/BucketArn"
        },
        "RoleArn" : {
          "$ref" : "#/definitions/RoleArn"
        },
        "Prefix" : {
          "$ref" : "#/definitions/S3KeyPrefix"
        }
      },
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "pattern" : "^[ a-zA-Z0-9\\+\\-=._:/@]{1,128}$"
        },
        "Value" : {
          "type" : "string",
          "pattern" : "^[ a-zA-Z0-9\\+\\-=._:/@]{1,256}$"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Name" : {
      "type" : "string",
      "pattern" : "^[ a-zA-Z0-9_:-]{1,256}$"
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Type" : {
      "type" : "string"
    },
    "ConfigData" : {
      "$ref" : "#/definitions/ConfigData"
    },
    "Arn" : {
      "type" : "string",
      "pattern" : "^(arn:(aws[a-zA-Z-]*)?:[a-z0-9-.]+:.*)|()$"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "required" : [ "Name", "ConfigData" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Id", "/properties/Type" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "groundstation:TagResource", "groundstation:UntagResource", "groundstation:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "groundstation:CreateConfig", "groundstation:TagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "groundstation:GetConfig", "groundstation:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "groundstation:UpdateConfig", "groundstation:ListTagsForResource", "groundstation:TagResource", "groundstation:UntagResource", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "groundstation:DeleteConfig" ]
    },
    "list" : {
      "permissions" : [ "groundstation:ListConfigs" ]
    }
  },
  "additionalProperties" : False
}