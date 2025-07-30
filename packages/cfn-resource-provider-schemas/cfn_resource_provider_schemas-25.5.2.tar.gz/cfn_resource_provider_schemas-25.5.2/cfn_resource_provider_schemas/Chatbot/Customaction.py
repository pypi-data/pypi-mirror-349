SCHEMA = {
  "typeName" : "AWS::Chatbot::CustomAction",
  "description" : "Definition of AWS::Chatbot::CustomAction Resource Type",
  "definitions" : {
    "CustomActionAttachment" : {
      "type" : "object",
      "properties" : {
        "NotificationType" : {
          "type" : "string",
          "maxLength" : 100,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9-]+$"
        },
        "ButtonText" : {
          "type" : "string",
          "maxLength" : 50,
          "minLength" : 1,
          "pattern" : "^[\\S\\s]+$"
        },
        "Criteria" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/CustomActionAttachmentCriteria"
          },
          "maxItems" : 5,
          "minItems" : 1
        },
        "Variables" : {
          "$ref" : "#/definitions/CustomActionAttachmentVariables"
        }
      },
      "additionalProperties" : False
    },
    "CustomActionAttachmentCriteria" : {
      "type" : "object",
      "properties" : {
        "Operator" : {
          "$ref" : "#/definitions/CustomActionAttachmentCriteriaOperator"
        },
        "VariableName" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 1024,
          "minLength" : 0
        }
      },
      "required" : [ "Operator", "VariableName" ],
      "additionalProperties" : False
    },
    "CustomActionAttachmentCriteriaOperator" : {
      "type" : "string",
      "enum" : [ "HAS_VALUE", "EQUALS" ]
    },
    "CustomActionAttachmentVariables" : {
      "type" : "object",
      "maxProperties" : 5,
      "minProperties" : 1,
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "CustomActionDefinition" : {
      "type" : "object",
      "properties" : {
        "CommandText" : {
          "type" : "string",
          "maxLength" : 5000,
          "minLength" : 1
        }
      },
      "required" : [ "CommandText" ],
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "ActionName" : {
      "type" : "string",
      "maxLength" : 64,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9_-]{1,64}$"
    },
    "AliasName" : {
      "type" : "string",
      "maxLength" : 30,
      "minLength" : 1,
      "pattern" : "^[A-Za-z0-9-_]+$"
    },
    "Attachments" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/CustomActionAttachment"
      }
    },
    "CustomActionArn" : {
      "type" : "string",
      "maxLength" : 1011,
      "minLength" : 1,
      "pattern" : "^arn:(aws[a-zA-Z-]*)?:chatbot:[A-Za-z0-9_/.-]{0,63}:[A-Za-z0-9_/.-]{0,63}:custom-action/[a-zA-Z0-9_-]{1,64}$"
    },
    "Definition" : {
      "$ref" : "#/definitions/CustomActionDefinition"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "maxItems" : 200,
      "minItems" : 0
    }
  },
  "required" : [ "ActionName", "Definition" ],
  "readOnlyProperties" : [ "/properties/CustomActionArn" ],
  "createOnlyProperties" : [ "/properties/ActionName" ],
  "primaryIdentifier" : [ "/properties/CustomActionArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "chatbot:CreateCustomAction", "chatbot:GetCustomAction", "chatbot:TagResource", "chatbot:ListTagsForResource" ]
    },
    "read" : {
      "permissions" : [ "chatbot:GetCustomAction", "chatbot:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "chatbot:UpdateCustomAction", "chatbot:GetCustomAction", "chatbot:TagResource", "chatbot:UntagResource", "chatbot:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "chatbot:DeleteCustomAction" ]
    },
    "list" : {
      "permissions" : [ "chatbot:ListCustomActions" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "chatbot:TagResource", "chatbot:ListTagsForResource", "chatbot:UntagResource" ]
  },
  "additionalProperties" : False
}