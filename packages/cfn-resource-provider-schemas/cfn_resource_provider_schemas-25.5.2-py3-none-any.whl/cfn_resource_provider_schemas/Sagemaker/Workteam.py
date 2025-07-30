SCHEMA = {
  "typeName" : "AWS::SageMaker::Workteam",
  "description" : "Resource Type definition for AWS::SageMaker::Workteam",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "NotificationConfiguration" : {
      "$ref" : "#/definitions/NotificationConfiguration"
    },
    "WorkteamName" : {
      "type" : "string"
    },
    "MemberDefinitions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/MemberDefinition"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "WorkforceName" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "OidcMemberDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OidcGroups" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "OidcGroups" ]
    },
    "NotificationConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NotificationTopicArn" : {
          "type" : "string"
        }
      },
      "required" : [ "NotificationTopicArn" ]
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "MemberDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CognitoMemberDefinition" : {
          "$ref" : "#/definitions/CognitoMemberDefinition"
        },
        "OidcMemberDefinition" : {
          "$ref" : "#/definitions/OidcMemberDefinition"
        }
      }
    },
    "CognitoMemberDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CognitoUserGroup" : {
          "type" : "string"
        },
        "CognitoUserPool" : {
          "type" : "string"
        },
        "CognitoClientId" : {
          "type" : "string"
        }
      },
      "required" : [ "CognitoUserPool", "CognitoClientId", "CognitoUserGroup" ]
    }
  },
  "createOnlyProperties" : [ "/properties/WorkteamName", "/properties/WorkforceName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}