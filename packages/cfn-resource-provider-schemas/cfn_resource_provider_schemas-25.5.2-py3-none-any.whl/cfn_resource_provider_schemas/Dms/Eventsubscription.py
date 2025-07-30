SCHEMA = {
  "typeName" : "AWS::DMS::EventSubscription",
  "description" : "Resource Type definition for AWS::DMS::EventSubscription",
  "additionalProperties" : False,
  "properties" : {
    "SourceType" : {
      "type" : "string"
    },
    "EventCategories" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Enabled" : {
      "type" : "boolean"
    },
    "SubscriptionName" : {
      "type" : "string"
    },
    "SnsTopicArn" : {
      "type" : "string"
    },
    "SourceIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "required" : [ "SnsTopicArn" ],
  "createOnlyProperties" : [ "/properties/SubscriptionName", "/properties/SourceIds" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}