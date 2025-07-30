SCHEMA = {
  "typeName" : "AWS::PinpointEmail::ConfigurationSet",
  "description" : "Resource Type definition for AWS::PinpointEmail::ConfigurationSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SendingOptions" : {
      "$ref" : "#/definitions/SendingOptions"
    },
    "TrackingOptions" : {
      "$ref" : "#/definitions/TrackingOptions"
    },
    "ReputationOptions" : {
      "$ref" : "#/definitions/ReputationOptions"
    },
    "DeliveryOptions" : {
      "$ref" : "#/definitions/DeliveryOptions"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tags"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "SendingOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SendingEnabled" : {
          "type" : "boolean"
        }
      }
    },
    "TrackingOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CustomRedirectDomain" : {
          "type" : "string"
        }
      }
    },
    "ReputationOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ReputationMetricsEnabled" : {
          "type" : "boolean"
        }
      }
    },
    "DeliveryOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SendingPoolName" : {
          "type" : "string"
        }
      }
    },
    "Tags" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}