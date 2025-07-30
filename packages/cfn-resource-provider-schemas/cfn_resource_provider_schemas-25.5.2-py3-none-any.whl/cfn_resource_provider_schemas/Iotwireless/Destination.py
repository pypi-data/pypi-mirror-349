SCHEMA = {
  "typeName" : "AWS::IoTWireless::Destination",
  "description" : "Destination's resource schema demonstrating some basic constructs and validation rules.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 127
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Name" : {
      "description" : "Unique name of destination",
      "type" : "string",
      "pattern" : "[a-zA-Z0-9:_-]+",
      "maxLength" : 128
    },
    "Expression" : {
      "description" : "Destination expression",
      "type" : "string"
    },
    "ExpressionType" : {
      "description" : "Must be RuleName",
      "type" : "string",
      "enum" : [ "RuleName", "MqttTopic", "SnsTopic" ]
    },
    "Description" : {
      "description" : "Destination description",
      "type" : "string",
      "maxLength" : 2048
    },
    "Tags" : {
      "description" : "A list of key-value pairs that contain metadata for the destination.",
      "type" : "array",
      "uniqueItems" : True,
      "maxItems" : 200,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "RoleArn" : {
      "description" : "AWS role ARN that grants access",
      "type" : "string",
      "minLength" : 20,
      "maxLength" : 2048
    },
    "Arn" : {
      "description" : "Destination arn. Returned after successful create.",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "Name", "Expression", "ExpressionType" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "iotwireless:TagResource", "iotwireless:UntagResource", "iotwireless:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:PassRole", "iotwireless:CreateDestination", "iotwireless:TagResource" ]
    },
    "read" : {
      "permissions" : [ "iotwireless:GetDestination", "iotwireless:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iam:PassRole", "iotwireless:GetDestination", "iotwireless:UpdateDestination", "iotwireless:UntagResource", "iotwireless:TagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotwireless:DeleteDestination" ]
    },
    "list" : {
      "permissions" : [ "iotwireless:ListDestinations", "iotwireless:ListTagsForResource" ]
    }
  }
}