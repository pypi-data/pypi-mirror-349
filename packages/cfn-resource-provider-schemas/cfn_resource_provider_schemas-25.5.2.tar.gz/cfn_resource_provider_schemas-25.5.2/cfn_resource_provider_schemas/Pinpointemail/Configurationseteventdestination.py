SCHEMA = {
  "typeName" : "AWS::PinpointEmail::ConfigurationSetEventDestination",
  "description" : "Resource Type definition for AWS::PinpointEmail::ConfigurationSetEventDestination",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "EventDestinationName" : {
      "type" : "string"
    },
    "ConfigurationSetName" : {
      "type" : "string"
    },
    "EventDestination" : {
      "$ref" : "#/definitions/EventDestination"
    }
  },
  "definitions" : {
    "EventDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SnsDestination" : {
          "$ref" : "#/definitions/SnsDestination"
        },
        "CloudWatchDestination" : {
          "$ref" : "#/definitions/CloudWatchDestination"
        },
        "Enabled" : {
          "type" : "boolean"
        },
        "MatchingEventTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "PinpointDestination" : {
          "$ref" : "#/definitions/PinpointDestination"
        },
        "KinesisFirehoseDestination" : {
          "$ref" : "#/definitions/KinesisFirehoseDestination"
        }
      },
      "required" : [ "MatchingEventTypes" ]
    },
    "SnsDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TopicArn" : {
          "type" : "string"
        }
      },
      "required" : [ "TopicArn" ]
    },
    "PinpointDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ApplicationArn" : {
          "type" : "string"
        }
      }
    },
    "KinesisFirehoseDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeliveryStreamArn" : {
          "type" : "string"
        },
        "IamRoleArn" : {
          "type" : "string"
        }
      },
      "required" : [ "DeliveryStreamArn", "IamRoleArn" ]
    },
    "CloudWatchDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DimensionConfigurations" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/DimensionConfiguration"
          }
        }
      }
    },
    "DimensionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DimensionValueSource" : {
          "type" : "string"
        },
        "DefaultDimensionValue" : {
          "type" : "string"
        },
        "DimensionName" : {
          "type" : "string"
        }
      },
      "required" : [ "DimensionValueSource", "DefaultDimensionValue", "DimensionName" ]
    }
  },
  "required" : [ "ConfigurationSetName", "EventDestinationName" ],
  "createOnlyProperties" : [ "/properties/ConfigurationSetName", "/properties/EventDestinationName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}