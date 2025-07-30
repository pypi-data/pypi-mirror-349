SCHEMA = {
  "typeName" : "AWS::Cognito::LogDeliveryConfiguration",
  "description" : "Resource Type definition for AWS::Cognito::LogDeliveryConfiguration",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "CloudWatchLogsConfiguration" : {
      "type" : "object",
      "properties" : {
        "LogGroupArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "S3Configuration" : {
      "type" : "object",
      "properties" : {
        "BucketArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "FirehoseConfiguration" : {
      "type" : "object",
      "properties" : {
        "StreamArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "LogConfiguration" : {
      "type" : "object",
      "properties" : {
        "LogLevel" : {
          "type" : "string"
        },
        "EventSource" : {
          "type" : "string"
        },
        "CloudWatchLogsConfiguration" : {
          "$ref" : "#/definitions/CloudWatchLogsConfiguration"
        },
        "S3Configuration" : {
          "$ref" : "#/definitions/S3Configuration"
        },
        "FirehoseConfiguration" : {
          "$ref" : "#/definitions/FirehoseConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "LogConfigurations" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/LogConfiguration"
      }
    }
  },
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "UserPoolId" : {
      "type" : "string"
    },
    "LogConfigurations" : {
      "$ref" : "#/definitions/LogConfigurations"
    }
  },
  "additionalProperties" : False,
  "required" : [ "UserPoolId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/UserPoolId" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:GetLogDeliveryConfiguration", "cognito-idp:SetLogDeliveryConfiguration", "logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "s3:GetBucketPolicy", "s3:PutBucketPolicy", "s3:ListBucket", "s3:PutObject", "s3:GetBucketAcl", "firehose:TagDeliveryStream", "iam:CreateServiceLinkedRole" ],
      "timeoutInMinutes" : 2
    },
    "read" : {
      "permissions" : [ "cognito-idp:GetLogDeliveryConfiguration" ]
    },
    "update" : {
      "permissions" : [ "cognito-idp:GetLogDeliveryConfiguration", "cognito-idp:SetLogDeliveryConfiguration", "logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "s3:GetBucketPolicy", "s3:PutBucketPolicy", "s3:ListBucket", "s3:PutObject", "s3:GetBucketAcl", "firehose:TagDeliveryStream", "iam:CreateServiceLinkedRole" ],
      "timeoutInMinutes" : 2
    },
    "delete" : {
      "permissions" : [ "cognito-idp:GetLogDeliveryConfiguration", "cognito-idp:SetLogDeliveryConfiguration", "logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "s3:GetBucketPolicy", "s3:PutBucketPolicy", "s3:ListBucket", "s3:PutObject", "s3:GetBucketAcl", "firehose:TagDeliveryStream", "iam:CreateServiceLinkedRole" ],
      "timeoutInMinutes" : 2
    }
  }
}