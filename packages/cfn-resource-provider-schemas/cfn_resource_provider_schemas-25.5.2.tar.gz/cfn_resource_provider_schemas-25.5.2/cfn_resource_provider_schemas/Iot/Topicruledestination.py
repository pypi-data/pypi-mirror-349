SCHEMA = {
  "typeName" : "AWS::IoT::TopicRuleDestination",
  "description" : "Resource Type definition for AWS::IoT::TopicRuleDestination",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "TopicRuleDestinationStatus" : {
      "type" : "string",
      "enum" : [ "ENABLED", "IN_PROGRESS", "DISABLED" ]
    },
    "HttpUrlDestinationSummary" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConfirmationUrl" : {
          "type" : "string"
        }
      }
    },
    "VpcDestinationProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "SecurityGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "VpcId" : {
          "type" : "string"
        },
        "RoleArn" : {
          "type" : "string"
        }
      }
    }
  },
  "properties" : {
    "Arn" : {
      "description" : "Amazon Resource Name (ARN).",
      "type" : "string"
    },
    "Status" : {
      "description" : "The status of the TopicRuleDestination.",
      "$ref" : "#/definitions/TopicRuleDestinationStatus"
    },
    "HttpUrlProperties" : {
      "description" : "HTTP URL destination properties.",
      "$ref" : "#/definitions/HttpUrlDestinationSummary"
    },
    "StatusReason" : {
      "description" : "The reasoning for the current status of the TopicRuleDestination.",
      "type" : "string"
    },
    "VpcProperties" : {
      "description" : "VPC destination properties.",
      "$ref" : "#/definitions/VpcDestinationProperties"
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : True
  },
  "additionalProperties" : False,
  "readOnlyProperties" : [ "/properties/Arn", "/properties/StatusReason" ],
  "createOnlyProperties" : [ "/properties/HttpUrlProperties", "/properties/VpcProperties" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:PassRole", "iot:CreateTopicRuleDestination", "iot:GetTopicRuleDestination", "iot:UpdateTopicRuleDestination" ]
    },
    "read" : {
      "permissions" : [ "iot:GetTopicRuleDestination" ]
    },
    "update" : {
      "permissions" : [ "iam:PassRole", "iot:GetTopicRuleDestination", "iot:UpdateTopicRuleDestination" ]
    },
    "delete" : {
      "permissions" : [ "iot:GetTopicRuleDestination", "iot:DeleteTopicRuleDestination" ]
    },
    "list" : {
      "permissions" : [ "iot:ListTopicRuleDestinations" ]
    }
  }
}