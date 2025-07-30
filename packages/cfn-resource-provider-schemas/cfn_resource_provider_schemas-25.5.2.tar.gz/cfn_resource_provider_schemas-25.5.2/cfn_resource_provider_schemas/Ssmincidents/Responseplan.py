SCHEMA = {
  "typeName" : "AWS::SSMIncidents::ResponsePlan",
  "description" : "Resource type definition for AWS::SSMIncidents::ResponsePlan",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ssm-incidents.git",
  "definitions" : {
    "SSMContact" : {
      "description" : "The ARN of the contact.",
      "type" : "string",
      "pattern" : "^arn:aws(-(cn|us-gov))?:ssm-contacts:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$",
      "maxLength" : 1000
    },
    "SnsArn" : {
      "description" : "The ARN of the Chatbot SNS topic.",
      "type" : "string",
      "pattern" : "^arn:aws(-(cn|us-gov))?:sns:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$",
      "maxLength" : 1000
    },
    "NotificationTargetItem" : {
      "description" : "A notification target.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SnsTopicArn" : {
          "$ref" : "#/definitions/SnsArn"
        }
      }
    },
    "Action" : {
      "description" : "The automation configuration to launch.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SsmAutomation" : {
          "$ref" : "#/definitions/SsmAutomation"
        }
      }
    },
    "SsmAutomation" : {
      "description" : "The configuration to use when starting the SSM automation document.",
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "RoleArn", "DocumentName" ],
      "properties" : {
        "RoleArn" : {
          "description" : "The role ARN to use when starting the SSM automation document.",
          "type" : "string",
          "pattern" : "^arn:aws(-(cn|us-gov))?:[a-z-]+:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$",
          "maxLength" : 1000
        },
        "DocumentName" : {
          "description" : "The document name to use when starting the SSM automation document.",
          "type" : "string",
          "maxLength" : 128
        },
        "DocumentVersion" : {
          "description" : "The version of the document to use when starting the SSM automation document.",
          "type" : "string",
          "maxLength" : 128
        },
        "TargetAccount" : {
          "description" : "The account type to use when starting the SSM automation document.",
          "type" : "string",
          "enum" : [ "IMPACTED_ACCOUNT", "RESPONSE_PLAN_OWNER_ACCOUNT" ]
        },
        "Parameters" : {
          "description" : "The parameters to set when starting the SSM automation document.",
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/SsmParameter"
          },
          "minItems" : 1,
          "maxItems" : 200,
          "default" : [ ]
        },
        "DynamicParameters" : {
          "description" : "The parameters with dynamic values to set when starting the SSM automation document.",
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/DynamicSsmParameter"
          },
          "maxItems" : 200,
          "default" : [ ]
        }
      }
    },
    "SsmParameter" : {
      "description" : "A parameter to set when starting the SSM automation document.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 50
        },
        "Values" : {
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : True,
          "maxItems" : 10,
          "items" : {
            "$ref" : "#/definitions/SsmParameterValue"
          }
        }
      },
      "required" : [ "Values", "Key" ],
      "additionalProperties" : False
    },
    "SsmParameterValue" : {
      "description" : "A value of the parameter to set when starting the SSM automation document.",
      "type" : "string",
      "maxLength" : 10000
    },
    "DynamicSsmParameter" : {
      "description" : "A parameter with a dynamic value to set when starting the SSM automation document.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 50
        },
        "Value" : {
          "$ref" : "#/definitions/DynamicSsmParameterValue"
        }
      },
      "required" : [ "Value", "Key" ],
      "additionalProperties" : False
    },
    "DynamicSsmParameterValue" : {
      "description" : "Value of the dynamic parameter to set when starting the SSM automation document.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Variable" : {
          "$ref" : "#/definitions/VariableType"
        }
      }
    },
    "VariableType" : {
      "description" : "The variable types used as dynamic parameter value when starting the SSM automation document.",
      "type" : "string",
      "enum" : [ "INCIDENT_RECORD_ARN", "INVOLVED_RESOURCES" ]
    },
    "Integration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PagerDutyConfiguration" : {
          "$ref" : "#/definitions/PagerDutyConfiguration"
        }
      },
      "oneOf" : [ {
        "required" : [ "PagerDutyConfiguration" ]
      } ]
    },
    "PagerDutyConfiguration" : {
      "description" : "The pagerDuty configuration to use when starting the incident.",
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "Name", "SecretId", "PagerDutyIncidentConfiguration" ],
      "properties" : {
        "Name" : {
          "description" : "The name of the pagerDuty configuration.",
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 200
        },
        "SecretId" : {
          "description" : "The AWS secrets manager secretId storing the pagerDuty token.",
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 512
        },
        "PagerDutyIncidentConfiguration" : {
          "$ref" : "#/definitions/PagerDutyIncidentConfiguration"
        }
      }
    },
    "PagerDutyIncidentConfiguration" : {
      "description" : "The pagerDuty incident configuration.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ServiceId" : {
          "description" : "The pagerDuty serviceId.",
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 200
        }
      },
      "required" : [ "ServiceId" ]
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
    },
    "IncidentTemplate" : {
      "description" : "The incident template configuration.",
      "additionalProperties" : False,
      "type" : "object",
      "required" : [ "Title", "Impact" ],
      "properties" : {
        "DedupeString" : {
          "description" : "The deduplication string.",
          "type" : "string",
          "maxLength" : 1000,
          "minLength" : 1
        },
        "Impact" : {
          "description" : "The impact value.",
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 5
        },
        "NotificationTargets" : {
          "description" : "The list of notification targets.",
          "type" : "array",
          "default" : [ ],
          "maxItems" : 10,
          "items" : {
            "$ref" : "#/definitions/NotificationTargetItem"
          },
          "insertionOrder" : False
        },
        "Summary" : {
          "description" : "The summary string.",
          "type" : "string",
          "maxLength" : 4000,
          "minLength" : 1
        },
        "Title" : {
          "description" : "The title string.",
          "type" : "string",
          "maxLength" : 200
        },
        "IncidentTags" : {
          "description" : "Tags that get applied to incidents created by the StartIncident API action.",
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : False,
          "default" : [ ],
          "maxItems" : 50,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        }
      }
    },
    "ChatbotSns" : {
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : True,
      "default" : [ ],
      "items" : {
        "$ref" : "#/definitions/SnsArn"
      }
    },
    "ChatChannel" : {
      "description" : "The chat channel configuration.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ChatbotSns" : {
          "$ref" : "#/definitions/ChatbotSns"
        }
      }
    }
  },
  "properties" : {
    "Arn" : {
      "description" : "The ARN of the response plan.",
      "type" : "string",
      "pattern" : "^arn:aws(-(cn|us-gov))?:[a-z-]+:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$",
      "maxLength" : 1000
    },
    "Name" : {
      "description" : "The name of the response plan.",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9_-]*$",
      "maxLength" : 200,
      "minLength" : 1
    },
    "DisplayName" : {
      "description" : "The display name of the response plan.",
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1
    },
    "ChatChannel" : {
      "$ref" : "#/definitions/ChatChannel"
    },
    "Engagements" : {
      "description" : "The list of engagements to use.",
      "type" : "array",
      "default" : [ ],
      "maxItems" : 5,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SSMContact"
      }
    },
    "Actions" : {
      "description" : "The list of actions.",
      "type" : "array",
      "default" : [ ],
      "uniqueItems" : True,
      "insertionOrder" : True,
      "maxItems" : 1,
      "items" : {
        "$ref" : "#/definitions/Action"
      }
    },
    "Integrations" : {
      "description" : "The list of integrations.",
      "type" : "array",
      "default" : [ ],
      "uniqueItems" : True,
      "insertionOrder" : True,
      "maxItems" : 1,
      "items" : {
        "$ref" : "#/definitions/Integration"
      }
    },
    "Tags" : {
      "description" : "The tags to apply to the response plan.",
      "type" : "array",
      "default" : [ ],
      "uniqueItems" : True,
      "insertionOrder" : False,
      "maxItems" : 50,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "IncidentTemplate" : {
      "$ref" : "#/definitions/IncidentTemplate"
    }
  },
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "required" : [ "Name", "IncidentTemplate" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ssm-incidents:TagResource", "ssm-incidents:UntagResource", "ssm-incidents:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ssm-incidents:CreateResponsePlan", "ssm-incidents:GetResponsePlan", "ssm-incidents:TagResource", "ssm-incidents:ListTagsForResource", "iam:PassRole", "secretsmanager:GetSecretValue", "kms:Decrypt", "kms:GenerateDataKey", "kms:GenerateDataKeyPair", "kms:GenerateDataKeyPairWithoutPlaintext", "kms:GenerateDataKeyWithoutPlaintext" ]
    },
    "read" : {
      "permissions" : [ "ssm-incidents:GetResponsePlan", "ssm-incidents:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "ssm-incidents:UpdateResponsePlan", "ssm-incidents:GetResponsePlan", "ssm-incidents:TagResource", "ssm-incidents:UntagResource", "ssm-incidents:ListTagsForResource", "iam:PassRole", "secretsmanager:GetSecretValue", "kms:Decrypt", "kms:GenerateDataKey", "kms:GenerateDataKeyPair", "kms:GenerateDataKeyPairWithoutPlaintext", "kms:GenerateDataKeyWithoutPlaintext" ]
    },
    "delete" : {
      "permissions" : [ "ssm-incidents:DeleteResponsePlan", "ssm-incidents:GetResponsePlan" ]
    },
    "list" : {
      "permissions" : [ "ssm-incidents:ListResponsePlans" ]
    }
  }
}