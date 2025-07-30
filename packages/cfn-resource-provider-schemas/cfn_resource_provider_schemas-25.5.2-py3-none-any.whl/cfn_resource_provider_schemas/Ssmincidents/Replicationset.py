SCHEMA = {
  "typeName" : "AWS::SSMIncidents::ReplicationSet",
  "description" : "Resource type definition for AWS::SSMIncidents::ReplicationSet",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ssm-incidents.git",
  "definitions" : {
    "Arn" : {
      "description" : "The ARN of the ReplicationSet.",
      "type" : "string",
      "pattern" : "^arn:aws(-(cn|us-gov|iso(-b)?))?:[a-z-]+:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$",
      "maxLength" : 1000
    },
    "RegionName" : {
      "description" : "The AWS region name.",
      "type" : "string",
      "maxLength" : 20
    },
    "ReplicationRegion" : {
      "description" : "The ReplicationSet regional configuration.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RegionName" : {
          "$ref" : "#/definitions/RegionName"
        },
        "RegionConfiguration" : {
          "$ref" : "#/definitions/RegionConfiguration"
        }
      }
    },
    "RegionConfiguration" : {
      "description" : "The ReplicationSet regional configuration.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SseKmsKeyId" : {
          "type" : "string",
          "description" : "The AWS Key Management Service key ID or Key Alias to use to encrypt your replication set.",
          "maxLength" : 2048
        }
      },
      "required" : [ "SseKmsKeyId" ]
    },
    "DeletionProtected" : {
      "description" : "Configures the ReplicationSet deletion protection.",
      "type" : "boolean"
    },
    "RegionList" : {
      "type" : "array",
      "minItems" : 1,
      "maxItems" : 3,
      "items" : {
        "$ref" : "#/definitions/ReplicationRegion"
      },
      "insertionOrder" : False,
      "uniqueItems" : True
    },
    "Tag" : {
      "description" : "A key-value pair to tag a resource.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "pattern" : "^(?!aws:)[a-zA-Z+-=._:/]+$",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "properties" : {
    "Arn" : {
      "description" : "The ARN of the ReplicationSet.",
      "$ref" : "#/definitions/Arn",
      "additionalProperties" : False
    },
    "Regions" : {
      "description" : "The ReplicationSet configuration.",
      "$ref" : "#/definitions/RegionList"
    },
    "DeletionProtected" : {
      "$ref" : "#/definitions/DeletionProtected",
      "default" : False
    },
    "Tags" : {
      "description" : "The tags to apply to the replication set.",
      "type" : "array",
      "default" : [ ],
      "uniqueItems" : True,
      "insertionOrder" : False,
      "maxItems" : 50,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/Arn" ],
  "required" : [ "Regions" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ssm-incidents:TagResource", "ssm-incidents:UntagResource", "ssm-incidents:ListTagsForResource" ]
  },
  "readOnlyProperties" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ssm-incidents:CreateReplicationSet", "ssm-incidents:ListReplicationSets", "ssm-incidents:UpdateDeletionProtection", "ssm-incidents:GetReplicationSet", "ssm-incidents:TagResource", "ssm-incidents:ListTagsForResource", "iam:CreateServiceLinkedRole" ]
    },
    "read" : {
      "permissions" : [ "ssm-incidents:ListReplicationSets", "ssm-incidents:GetReplicationSet", "ssm-incidents:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "ssm-incidents:UpdateReplicationSet", "ssm-incidents:UpdateDeletionProtection", "ssm-incidents:GetReplicationSet", "ssm-incidents:TagResource", "ssm-incidents:UntagResource", "ssm-incidents:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "ssm-incidents:DeleteReplicationSet", "ssm-incidents:GetReplicationSet" ]
    },
    "list" : {
      "permissions" : [ "ssm-incidents:ListReplicationSets" ]
    }
  }
}