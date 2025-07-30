SCHEMA = {
  "typeName" : "AWS::Greengrass::SubscriptionDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::SubscriptionDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SubscriptionDefinitionId" : {
      "type" : "string"
    },
    "Subscriptions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Subscription"
      }
    }
  },
  "definitions" : {
    "Subscription" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Target" : {
          "type" : "string"
        },
        "Id" : {
          "type" : "string"
        },
        "Source" : {
          "type" : "string"
        },
        "Subject" : {
          "type" : "string"
        }
      },
      "required" : [ "Target", "Id", "Source", "Subject" ]
    }
  },
  "required" : [ "SubscriptionDefinitionId", "Subscriptions" ],
  "createOnlyProperties" : [ "/properties/Subscriptions", "/properties/SubscriptionDefinitionId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}