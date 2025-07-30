SCHEMA = {
  "typeName" : "AWS::SES::MailManagerRuleSet",
  "description" : "Definition of AWS::SES::MailManagerRuleSet Resource Type",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ses-mailmanager",
  "definitions" : {
    "ActionFailurePolicy" : {
      "type" : "string",
      "enum" : [ "CONTINUE", "DROP" ]
    },
    "AddHeaderAction" : {
      "type" : "object",
      "properties" : {
        "HeaderName" : {
          "type" : "string",
          "maxLength" : 64,
          "minLength" : 1,
          "pattern" : "^[xX]\\-[a-zA-Z0-9\\-]+$"
        },
        "HeaderValue" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1
        }
      },
      "required" : [ "HeaderName", "HeaderValue" ],
      "additionalProperties" : False
    },
    "Analysis" : {
      "type" : "object",
      "properties" : {
        "Analyzer" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        },
        "ResultField" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 1,
          "pattern" : "^(addon\\.)?[\\sa-zA-Z0-9_]+$"
        }
      },
      "required" : [ "Analyzer", "ResultField" ],
      "additionalProperties" : False
    },
    "RuleIsInAddressList" : {
      "type" : "object",
      "properties" : {
        "Attribute" : {
          "$ref" : "#/definitions/RuleAddressListEmailAttribute"
        },
        "AddressLists" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          },
          "maxItems" : 1,
          "minItems" : 1,
          "uniqueItems" : True
        }
      },
      "required" : [ "Attribute", "AddressLists" ],
      "additionalProperties" : False
    },
    "ArchiveAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "TargetArchive" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        }
      },
      "required" : [ "TargetArchive" ],
      "additionalProperties" : False
    },
    "DeliverToMailboxAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "MailboxArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        },
        "RoleArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        }
      },
      "required" : [ "MailboxArn", "RoleArn" ],
      "additionalProperties" : False
    },
    "SnsAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "TopicArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^arn:(aws|aws-cn|aws-us-gov):sns:[a-z]{2}-[a-z]+-\\d{1}:\\d{12}:[\\w\\-]{1,256}$"
        },
        "RoleArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        },
        "Encoding" : {
          "$ref" : "#/definitions/SnsNotificationEncoding"
        },
        "PayloadType" : {
          "$ref" : "#/definitions/SnsNotificationPayloadType"
        }
      },
      "required" : [ "TopicArn", "RoleArn" ],
      "additionalProperties" : False
    },
    "SnsNotificationEncoding" : {
      "type" : "string",
      "enum" : [ "UTF-8", "BASE64" ]
    },
    "SnsNotificationPayloadType" : {
      "type" : "string",
      "enum" : [ "CONTENT", "HEADERS" ]
    },
    "DeliverToQBusinessAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "ApplicationId" : {
          "type" : "string",
          "maxLength" : 36,
          "minLength" : 36,
          "pattern" : "^[a-z0-9-]+$"
        },
        "IndexId" : {
          "type" : "string",
          "maxLength" : 36,
          "minLength" : 36,
          "pattern" : "^[a-z0-9-]+$"
        },
        "RoleArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        }
      },
      "required" : [ "ApplicationId", "IndexId", "RoleArn" ],
      "additionalProperties" : False
    },
    "DropAction" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "MailFrom" : {
      "type" : "string",
      "enum" : [ "REPLACE", "PRESERVE" ]
    },
    "RelayAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "Relay" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        },
        "MailFrom" : {
          "$ref" : "#/definitions/MailFrom"
        }
      },
      "required" : [ "Relay" ],
      "additionalProperties" : False
    },
    "ReplaceRecipientAction" : {
      "type" : "object",
      "properties" : {
        "ReplaceWith" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 254,
            "minLength" : 0,
            "pattern" : "^[0-9A-Za-z@+.-]+$"
          },
          "maxItems" : 100,
          "minItems" : 1,
          "uniqueItems" : True
        }
      },
      "additionalProperties" : False
    },
    "Rule" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string",
          "maxLength" : 32,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9_.-]+$"
        },
        "Conditions" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RuleCondition"
          },
          "maxItems" : 10,
          "minItems" : 0
        },
        "Unless" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RuleCondition"
          },
          "maxItems" : 10,
          "minItems" : 0
        },
        "Actions" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RuleAction"
          },
          "maxItems" : 10,
          "minItems" : 1
        }
      },
      "required" : [ "Actions" ],
      "additionalProperties" : False
    },
    "RuleAction" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Drop",
        "properties" : {
          "Drop" : {
            "$ref" : "#/definitions/DropAction"
          }
        },
        "required" : [ "Drop" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Relay",
        "properties" : {
          "Relay" : {
            "$ref" : "#/definitions/RelayAction"
          }
        },
        "required" : [ "Relay" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Archive",
        "properties" : {
          "Archive" : {
            "$ref" : "#/definitions/ArchiveAction"
          }
        },
        "required" : [ "Archive" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "WriteToS3",
        "properties" : {
          "WriteToS3" : {
            "$ref" : "#/definitions/S3Action"
          }
        },
        "required" : [ "WriteToS3" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Send",
        "properties" : {
          "Send" : {
            "$ref" : "#/definitions/SendAction"
          }
        },
        "required" : [ "Send" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "AddHeader",
        "properties" : {
          "AddHeader" : {
            "$ref" : "#/definitions/AddHeaderAction"
          }
        },
        "required" : [ "AddHeader" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "ReplaceRecipient",
        "properties" : {
          "ReplaceRecipient" : {
            "$ref" : "#/definitions/ReplaceRecipientAction"
          }
        },
        "required" : [ "ReplaceRecipient" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "DeliverToMailbox",
        "properties" : {
          "DeliverToMailbox" : {
            "$ref" : "#/definitions/DeliverToMailboxAction"
          }
        },
        "required" : [ "DeliverToMailbox" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "DeliverToQBusiness",
        "properties" : {
          "DeliverToQBusiness" : {
            "$ref" : "#/definitions/DeliverToQBusinessAction"
          }
        },
        "required" : [ "DeliverToQBusiness" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "PublishToSns",
        "properties" : {
          "PublishToSns" : {
            "$ref" : "#/definitions/SnsAction"
          }
        },
        "required" : [ "PublishToSns" ],
        "additionalProperties" : False
      } ]
    },
    "RuleBooleanEmailAttribute" : {
      "type" : "string",
      "enum" : [ "READ_RECEIPT_REQUESTED", "TLS", "TLS_WRAPPED" ]
    },
    "RuleBooleanExpression" : {
      "type" : "object",
      "properties" : {
        "Evaluate" : {
          "$ref" : "#/definitions/RuleBooleanToEvaluate"
        },
        "Operator" : {
          "$ref" : "#/definitions/RuleBooleanOperator"
        }
      },
      "required" : [ "Evaluate", "Operator" ],
      "additionalProperties" : False
    },
    "RuleBooleanOperator" : {
      "type" : "string",
      "enum" : [ "IS_TRUE", "IS_FALSE" ]
    },
    "RuleBooleanToEvaluate" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/RuleBooleanEmailAttribute"
          }
        },
        "required" : [ "Attribute" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Analysis",
        "properties" : {
          "Analysis" : {
            "$ref" : "#/definitions/Analysis"
          }
        },
        "required" : [ "Analysis" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "IsInAddressList",
        "properties" : {
          "IsInAddressList" : {
            "$ref" : "#/definitions/RuleIsInAddressList"
          }
        },
        "required" : [ "IsInAddressList" ],
        "additionalProperties" : False
      } ]
    },
    "RuleCondition" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "BooleanExpression",
        "properties" : {
          "BooleanExpression" : {
            "$ref" : "#/definitions/RuleBooleanExpression"
          }
        },
        "required" : [ "BooleanExpression" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "StringExpression",
        "properties" : {
          "StringExpression" : {
            "$ref" : "#/definitions/RuleStringExpression"
          }
        },
        "required" : [ "StringExpression" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "NumberExpression",
        "properties" : {
          "NumberExpression" : {
            "$ref" : "#/definitions/RuleNumberExpression"
          }
        },
        "required" : [ "NumberExpression" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "IpExpression",
        "properties" : {
          "IpExpression" : {
            "$ref" : "#/definitions/RuleIpExpression"
          }
        },
        "required" : [ "IpExpression" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "VerdictExpression",
        "properties" : {
          "VerdictExpression" : {
            "$ref" : "#/definitions/RuleVerdictExpression"
          }
        },
        "required" : [ "VerdictExpression" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "DmarcExpression",
        "properties" : {
          "DmarcExpression" : {
            "$ref" : "#/definitions/RuleDmarcExpression"
          }
        },
        "required" : [ "DmarcExpression" ],
        "additionalProperties" : False
      } ]
    },
    "RuleDmarcExpression" : {
      "type" : "object",
      "properties" : {
        "Operator" : {
          "$ref" : "#/definitions/RuleDmarcOperator"
        },
        "Values" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RuleDmarcPolicy"
          },
          "maxItems" : 10,
          "minItems" : 1
        }
      },
      "required" : [ "Operator", "Values" ],
      "additionalProperties" : False
    },
    "RuleDmarcOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "NOT_EQUALS" ]
    },
    "RuleDmarcPolicy" : {
      "type" : "string",
      "enum" : [ "NONE", "QUARANTINE", "REJECT" ]
    },
    "RuleIpEmailAttribute" : {
      "type" : "string",
      "enum" : [ "SOURCE_IP" ]
    },
    "RuleIpExpression" : {
      "type" : "object",
      "properties" : {
        "Evaluate" : {
          "$ref" : "#/definitions/RuleIpToEvaluate"
        },
        "Operator" : {
          "$ref" : "#/definitions/RuleIpOperator"
        },
        "Values" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 43,
            "minLength" : 1,
            "pattern" : "^(([0-9]|.|:|/)*)$"
          },
          "maxItems" : 10,
          "minItems" : 1
        }
      },
      "required" : [ "Evaluate", "Operator", "Values" ],
      "additionalProperties" : False
    },
    "RuleIpOperator" : {
      "type" : "string",
      "enum" : [ "CIDR_MATCHES", "NOT_CIDR_MATCHES" ]
    },
    "RuleIpToEvaluate" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/RuleIpEmailAttribute"
          }
        },
        "required" : [ "Attribute" ],
        "additionalProperties" : False
      } ]
    },
    "RuleNumberEmailAttribute" : {
      "type" : "string",
      "enum" : [ "MESSAGE_SIZE" ]
    },
    "RuleNumberExpression" : {
      "type" : "object",
      "properties" : {
        "Evaluate" : {
          "$ref" : "#/definitions/RuleNumberToEvaluate"
        },
        "Operator" : {
          "$ref" : "#/definitions/RuleNumberOperator"
        },
        "Value" : {
          "type" : "number"
        }
      },
      "required" : [ "Evaluate", "Operator", "Value" ],
      "additionalProperties" : False
    },
    "RuleNumberOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "NOT_EQUALS", "LESS_THAN", "GREATER_THAN", "LESS_THAN_OR_EQUAL", "GREATER_THAN_OR_EQUAL" ]
    },
    "RuleAddressListEmailAttribute" : {
      "type" : "string",
      "enum" : [ "RECIPIENT", "MAIL_FROM", "SENDER", "FROM", "TO", "CC" ]
    },
    "RuleNumberToEvaluate" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/RuleNumberEmailAttribute"
          }
        },
        "required" : [ "Attribute" ],
        "additionalProperties" : False
      } ]
    },
    "RuleStringEmailAttribute" : {
      "type" : "string",
      "enum" : [ "MAIL_FROM", "HELO", "RECIPIENT", "SENDER", "FROM", "SUBJECT", "TO", "CC" ]
    },
    "RuleStringExpression" : {
      "type" : "object",
      "properties" : {
        "Evaluate" : {
          "$ref" : "#/definitions/RuleStringToEvaluate"
        },
        "Operator" : {
          "$ref" : "#/definitions/RuleStringOperator"
        },
        "Values" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 4096,
            "minLength" : 1
          },
          "maxItems" : 10,
          "minItems" : 1
        }
      },
      "required" : [ "Evaluate", "Operator", "Values" ],
      "additionalProperties" : False
    },
    "RuleStringOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "NOT_EQUALS", "STARTS_WITH", "ENDS_WITH", "CONTAINS" ]
    },
    "RuleStringToEvaluate" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/RuleStringEmailAttribute"
          }
        },
        "required" : [ "Attribute" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "MimeHeaderAttribute",
        "properties" : {
          "MimeHeaderAttribute" : {
            "type" : "string",
            "pattern" : "^X-[a-zA-Z0-9-]{1,256}$"
          }
        },
        "required" : [ "MimeHeaderAttribute" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Analysis",
        "properties" : {
          "Analysis" : {
            "$ref" : "#/definitions/Analysis"
          }
        },
        "required" : [ "Analysis" ],
        "additionalProperties" : False
      } ]
    },
    "RuleVerdict" : {
      "type" : "string",
      "enum" : [ "PASS", "FAIL", "GRAY", "PROCESSING_FAILED" ]
    },
    "RuleVerdictAttribute" : {
      "type" : "string",
      "enum" : [ "SPF", "DKIM" ]
    },
    "RuleVerdictExpression" : {
      "type" : "object",
      "properties" : {
        "Evaluate" : {
          "$ref" : "#/definitions/RuleVerdictToEvaluate"
        },
        "Operator" : {
          "$ref" : "#/definitions/RuleVerdictOperator"
        },
        "Values" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RuleVerdict"
          },
          "maxItems" : 10,
          "minItems" : 1
        }
      },
      "required" : [ "Evaluate", "Operator", "Values" ],
      "additionalProperties" : False
    },
    "RuleVerdictOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "NOT_EQUALS" ]
    },
    "RuleVerdictToEvaluate" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/RuleVerdictAttribute"
          }
        },
        "required" : [ "Attribute" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Analysis",
        "properties" : {
          "Analysis" : {
            "$ref" : "#/definitions/Analysis"
          }
        },
        "required" : [ "Analysis" ],
        "additionalProperties" : False
      } ]
    },
    "S3Action" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "RoleArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        },
        "S3Bucket" : {
          "type" : "string",
          "maxLength" : 62,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9.-]+$"
        },
        "S3Prefix" : {
          "type" : "string",
          "maxLength" : 62,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9!_.*'()/-]+$"
        },
        "S3SseKmsKeyId" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9-:/]+$"
        }
      },
      "required" : [ "RoleArn", "S3Bucket" ],
      "additionalProperties" : False
    },
    "SendAction" : {
      "type" : "object",
      "properties" : {
        "ActionFailurePolicy" : {
          "$ref" : "#/definitions/ActionFailurePolicy"
        },
        "RoleArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 20,
          "pattern" : "^[a-zA-Z0-9:_/+=,@.#-]+$"
        }
      },
      "required" : [ "RoleArn" ],
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9/_\\+=\\.:@\\-]+$"
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0,
          "pattern" : "^[a-zA-Z0-9/_\\+=\\.:@\\-]*$"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ses:TagResource", "ses:UntagResource" ]
  },
  "properties" : {
    "RuleSetArn" : {
      "type" : "string"
    },
    "RuleSetId" : {
      "type" : "string",
      "maxLength" : 100,
      "minLength" : 1
    },
    "RuleSetName" : {
      "type" : "string",
      "maxLength" : 100,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9_.-]+$"
    },
    "Rules" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Rule"
      },
      "maxItems" : 40,
      "minItems" : 0
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "maxItems" : 200,
      "minItems" : 0
    }
  },
  "required" : [ "Rules" ],
  "readOnlyProperties" : [ "/properties/RuleSetArn", "/properties/RuleSetId" ],
  "primaryIdentifier" : [ "/properties/RuleSetId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ses:TagResource", "ses:ListTagsForResource", "ses:GetRuleSet", "ses:CreateRuleSet" ]
    },
    "read" : {
      "permissions" : [ "ses:ListTagsForResource", "ses:GetRuleSet" ]
    },
    "update" : {
      "permissions" : [ "ses:TagResource", "ses:UntagResource", "ses:ListTagsForResource", "ses:GetRuleSet", "ses:UpdateRuleSet" ]
    },
    "delete" : {
      "permissions" : [ "ses:GetRuleSet", "ses:DeleteRuleSet" ]
    },
    "list" : {
      "permissions" : [ "ses:ListRuleSets" ]
    }
  },
  "additionalProperties" : False
}