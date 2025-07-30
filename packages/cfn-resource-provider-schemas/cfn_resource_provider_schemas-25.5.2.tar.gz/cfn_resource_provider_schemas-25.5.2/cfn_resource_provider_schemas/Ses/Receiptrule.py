SCHEMA = {
  "typeName" : "AWS::SES::ReceiptRule",
  "description" : "Resource Type definition for AWS::SES::ReceiptRule",
  "additionalProperties" : False,
  "properties" : {
    "After" : {
      "type" : "string"
    },
    "Rule" : {
      "$ref" : "#/definitions/Rule"
    },
    "Id" : {
      "type" : "string"
    },
    "RuleSetName" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ConnectAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InstanceARN" : {
          "type" : "string"
        },
        "IAMRoleARN" : {
          "type" : "string"
        }
      },
      "required" : [ "InstanceARN", "IAMRoleARN" ]
    },
    "Action" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectAction" : {
          "$ref" : "#/definitions/ConnectAction"
        },
        "BounceAction" : {
          "$ref" : "#/definitions/BounceAction"
        },
        "S3Action" : {
          "$ref" : "#/definitions/S3Action"
        },
        "StopAction" : {
          "$ref" : "#/definitions/StopAction"
        },
        "SNSAction" : {
          "$ref" : "#/definitions/SNSAction"
        },
        "WorkmailAction" : {
          "$ref" : "#/definitions/WorkmailAction"
        },
        "AddHeaderAction" : {
          "$ref" : "#/definitions/AddHeaderAction"
        },
        "LambdaAction" : {
          "$ref" : "#/definitions/LambdaAction"
        }
      }
    },
    "BounceAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Sender" : {
          "type" : "string"
        },
        "SmtpReplyCode" : {
          "type" : "string"
        },
        "Message" : {
          "type" : "string"
        },
        "TopicArn" : {
          "type" : "string"
        },
        "StatusCode" : {
          "type" : "string"
        }
      },
      "required" : [ "Sender", "SmtpReplyCode", "Message" ]
    },
    "S3Action" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ObjectKeyPrefix" : {
          "type" : "string"
        },
        "BucketName" : {
          "type" : "string"
        },
        "IamRoleArn" : {
          "type" : "string"
        },
        "KmsKeyArn" : {
          "type" : "string"
        },
        "TopicArn" : {
          "type" : "string"
        }
      },
      "required" : [ "BucketName" ]
    },
    "StopAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Scope" : {
          "type" : "string"
        },
        "TopicArn" : {
          "type" : "string"
        }
      },
      "required" : [ "Scope" ]
    },
    "Rule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ScanEnabled" : {
          "type" : "boolean"
        },
        "Recipients" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Actions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Action"
          }
        },
        "Enabled" : {
          "type" : "boolean"
        },
        "Name" : {
          "type" : "string"
        },
        "TlsPolicy" : {
          "type" : "string"
        }
      }
    },
    "SNSAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TopicArn" : {
          "type" : "string"
        },
        "Encoding" : {
          "type" : "string"
        }
      }
    },
    "WorkmailAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TopicArn" : {
          "type" : "string"
        },
        "OrganizationArn" : {
          "type" : "string"
        }
      },
      "required" : [ "OrganizationArn" ]
    },
    "AddHeaderAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HeaderName" : {
          "type" : "string"
        },
        "HeaderValue" : {
          "type" : "string"
        }
      },
      "required" : [ "HeaderValue", "HeaderName" ]
    },
    "LambdaAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InvocationType" : {
          "type" : "string"
        },
        "FunctionArn" : {
          "type" : "string"
        },
        "TopicArn" : {
          "type" : "string"
        }
      },
      "required" : [ "FunctionArn" ]
    }
  },
  "required" : [ "Rule", "RuleSetName" ],
  "createOnlyProperties" : [ "/properties/RuleSetName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}