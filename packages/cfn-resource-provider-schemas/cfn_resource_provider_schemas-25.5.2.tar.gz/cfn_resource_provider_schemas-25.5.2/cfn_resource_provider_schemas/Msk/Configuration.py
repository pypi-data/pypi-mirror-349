SCHEMA = {
  "typeName" : "AWS::MSK::Configuration",
  "description" : "Resource Type definition for AWS::MSK::Configuration",
  "definitions" : {
    "KafkaVersionsList" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "LatestRevision" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CreationTime" : {
          "type" : "string"
        },
        "Description" : {
          "type" : "string"
        },
        "Revision" : {
          "type" : "integer"
        }
      }
    }
  },
  "properties" : {
    "Name" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "ServerProperties" : {
      "type" : "string"
    },
    "KafkaVersionsList" : {
      "$ref" : "#/definitions/KafkaVersionsList"
    },
    "Arn" : {
      "type" : "string"
    },
    "LatestRevision" : {
      "$ref" : "#/definitions/LatestRevision"
    }
  },
  "additionalProperties" : False,
  "required" : [ "ServerProperties", "Name" ],
  "createOnlyProperties" : [ "/properties/KafkaVersionsList", "/properties/Name" ],
  "writeOnlyProperties" : [ "/properties/ServerProperties" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/LatestRevision/CreationTime", "/properties/LatestRevision/Revision", "/properties/LatestRevision/Description" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "kafka:CreateConfiguration", "Kafka:DescribeConfiguration" ]
    },
    "delete" : {
      "permissions" : [ "kafka:DeleteConfiguration", "kafka:DescribeConfiguration" ]
    },
    "list" : {
      "permissions" : [ "kafka:ListConfigurations" ]
    },
    "read" : {
      "permissions" : [ "kafka:DescribeConfiguration" ]
    },
    "update" : {
      "permissions" : [ "kafka:UpdateConfiguration", "kafka:DescribeConfiguration" ]
    }
  }
}