SCHEMA = {
  "typeName" : "AWS::SSO::InstanceAccessControlAttributeConfiguration",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False
  },
  "description" : "Resource Type definition for SSO InstanceAccessControlAttributeConfiguration",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-sso/aws-sso-instanceaccesscontrolattributeconfiguration",
  "definitions" : {
    "AccessControlAttributeValueSource" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 256,
      "pattern" : "[\\p{L}\\p{Z}\\p{N}_.:\\/=+\\-@\\[\\]\\{\\}\\$\\\\\"]*"
    },
    "AccessControlAttributeValueSourceList" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/AccessControlAttributeValueSource"
      },
      "maxItems" : 1
    },
    "AccessControlAttributeValue" : {
      "type" : "object",
      "properties" : {
        "Source" : {
          "$ref" : "#/definitions/AccessControlAttributeValueSourceList"
        }
      },
      "required" : [ "Source" ],
      "additionalProperties" : False
    },
    "AccessControlAttribute" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "pattern" : "[\\p{L}\\p{Z}\\p{N}_.:\\/=+\\-@]+",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "$ref" : "#/definitions/AccessControlAttributeValue"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "AccessControlAttributeList" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/AccessControlAttribute"
      },
      "maxItems" : 50
    }
  },
  "properties" : {
    "InstanceArn" : {
      "description" : "The ARN of the AWS SSO instance under which the operation will be executed.",
      "type" : "string",
      "pattern" : "arn:(aws|aws-us-gov|aws-cn|aws-iso|aws-iso-b):sso:::instance/(sso)?ins-[a-zA-Z0-9-.]{16}",
      "minLength" : 10,
      "maxLength" : 1224
    },
    "InstanceAccessControlAttributeConfiguration" : {
      "description" : "The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes. We recomend that you use  AccessControlAttributes property instead.",
      "type" : "object",
      "properties" : {
        "AccessControlAttributes" : {
          "$ref" : "#/definitions/AccessControlAttributeList"
        }
      },
      "required" : [ "AccessControlAttributes" ],
      "additionalProperties" : False
    },
    "AccessControlAttributes" : {
      "$ref" : "#/definitions/AccessControlAttributeList"
    }
  },
  "additionalProperties" : False,
  "required" : [ "InstanceArn" ],
  "createOnlyProperties" : [ "/properties/InstanceArn" ],
  "primaryIdentifier" : [ "/properties/InstanceArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "sso:CreateInstanceAccessControlAttributeConfiguration", "sso:UpdateApplicationProfileForAWSAccountInstance", "sso:DescribeInstanceAccessControlAttributeConfiguration" ]
    },
    "read" : {
      "permissions" : [ "sso:DescribeInstanceAccessControlAttributeConfiguration" ]
    },
    "update" : {
      "permissions" : [ "sso:UpdateInstanceAccessControlAttributeConfiguration", "sso:DescribeInstanceAccessControlAttributeConfiguration" ]
    },
    "delete" : {
      "permissions" : [ "sso:DeleteInstanceAccessControlAttributeConfiguration", "sso:DescribeInstanceAccessControlAttributeConfiguration" ]
    },
    "list" : {
      "permissions" : [ "sso:DescribeInstanceAccessControlAttributeConfiguration" ]
    }
  },
  "deprecatedProperties" : [ "/properties/InstanceAccessControlAttributeConfiguration" ]
}