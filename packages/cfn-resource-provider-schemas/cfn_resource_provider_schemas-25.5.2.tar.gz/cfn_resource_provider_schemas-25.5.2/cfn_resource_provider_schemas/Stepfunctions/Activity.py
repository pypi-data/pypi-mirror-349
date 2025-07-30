SCHEMA = {
  "typeName" : "AWS::StepFunctions::Activity",
  "description" : "Resource schema for Activity",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-stepfunctions.git",
  "definitions" : {
    "TagsEntry" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "additionalProperties" : False,
      "required" : [ "Key", "Value" ]
    },
    "EncryptionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyId" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 2048
        },
        "KmsDataKeyReusePeriodSeconds" : {
          "type" : "integer",
          "minimum" : 60,
          "maximum" : 900
        },
        "Type" : {
          "type" : "string",
          "enum" : [ "CUSTOMER_MANAGED_KMS_KEY", "AWS_OWNED_KEY" ]
        }
      },
      "required" : [ "Type" ]
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 2048
    },
    "Name" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 80
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/TagsEntry"
      }
    },
    "EncryptionConfiguration" : {
      "$ref" : "#/definitions/EncryptionConfiguration"
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "states:UntagResource", "states:TagResource", "states:ListTagsForResource" ]
  },
  "required" : [ "Name" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/EncryptionConfiguration" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "states:CreateActivity", "states:DescribeActivity", "states:TagResource", "kms:DescribeKey" ]
    },
    "read" : {
      "permissions" : [ "states:DescribeActivity", "states:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "states:ListTagsForResource", "states:TagResource", "states:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "states:DescribeActivity", "states:DeleteActivity" ]
    },
    "list" : {
      "permissions" : [ "states:ListActivities" ]
    }
  }
}