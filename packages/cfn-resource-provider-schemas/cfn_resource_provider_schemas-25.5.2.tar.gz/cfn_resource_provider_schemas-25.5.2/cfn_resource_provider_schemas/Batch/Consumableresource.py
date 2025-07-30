SCHEMA = {
  "typeName" : "AWS::Batch::ConsumableResource",
  "description" : "Resource Type definition for AWS::Batch::ConsumableResource",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-batch.git",
  "definitions" : {
    "ResourceArn" : {
      "description" : "ARN of the Consumable Resource.",
      "type" : "string"
    },
    "ResourceType" : {
      "description" : "Type of Consumable Resource.",
      "type" : "string",
      "enum" : [ "REPLENISHABLE", "NON_REPLENISHABLE" ]
    }
  },
  "properties" : {
    "ConsumableResourceName" : {
      "description" : "Name of ConsumableResource.",
      "type" : "string",
      "pattern" : ""
    },
    "ConsumableResourceArn" : {
      "$ref" : "#/definitions/ResourceArn"
    },
    "TotalQuantity" : {
      "description" : "Total Quantity of ConsumableResource.",
      "type" : "integer",
      "format" : "int64"
    },
    "InUseQuantity" : {
      "description" : "In-use Quantity of ConsumableResource.",
      "type" : "integer",
      "format" : "int64"
    },
    "AvailableQuantity" : {
      "description" : "Available Quantity of ConsumableResource.",
      "type" : "integer",
      "format" : "int64"
    },
    "ResourceType" : {
      "$ref" : "#/definitions/ResourceType"
    },
    "CreatedAt" : {
      "type" : "integer",
      "format" : "int64"
    },
    "Tags" : {
      "type" : "object",
      "description" : "A key-value pair to associate with a resource.",
      "patternProperties" : {
        ".*" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    }
  },
  "required" : [ "ResourceType", "TotalQuantity" ],
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "Batch:TagResource", "Batch:UntagResource" ]
  },
  "primaryIdentifier" : [ "/properties/ConsumableResourceArn" ],
  "createOnlyProperties" : [ "/properties/ConsumableResourceName", "/properties/ResourceType", "/properties/Tags" ],
  "readOnlyProperties" : [ "/properties/ConsumableResourceArn", "/properties/CreatedAt", "/properties/InUseQuantity", "/properties/AvailableQuantity" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "Batch:CreateConsumableResource", "Batch:TagResource" ]
    },
    "read" : {
      "permissions" : [ "Batch:DescribeConsumableResource" ]
    },
    "update" : {
      "permissions" : [ "Batch:UpdateConsumableResource", "Batch:TagResource", "Batch:UnTagResource" ]
    },
    "delete" : {
      "permissions" : [ "Batch:DescribeConsumableResource", "Batch:DeleteConsumableResource" ]
    },
    "list" : {
      "permissions" : [ "Batch:ListConsumableResources" ]
    }
  }
}