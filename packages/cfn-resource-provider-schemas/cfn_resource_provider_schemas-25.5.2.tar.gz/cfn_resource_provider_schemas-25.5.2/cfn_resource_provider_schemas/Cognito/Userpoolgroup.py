SCHEMA = {
  "typeName" : "AWS::Cognito::UserPoolGroup",
  "description" : "Resource Type definition for AWS::Cognito::UserPoolGroup",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "properties" : {
    "Description" : {
      "type" : "string",
      "maxLength" : 2048
    },
    "GroupName" : {
      "type" : "string"
    },
    "Precedence" : {
      "type" : "integer",
      "minimum" : 0
    },
    "RoleArn" : {
      "type" : "string"
    },
    "UserPoolId" : {
      "type" : "string"
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "additionalProperties" : False,
  "required" : [ "UserPoolId" ],
  "createOnlyProperties" : [ "/properties/UserPoolId", "/properties/GroupName" ],
  "primaryIdentifier" : [ "/properties/UserPoolId", "/properties/GroupName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:CreateGroup", "iam:PassRole", "iam:PutRolePolicy", "cognito-idp:GetGroup" ],
      "timeoutInMinutes" : 5
    },
    "read" : {
      "permissions" : [ "cognito-idp:GetGroup" ]
    },
    "update" : {
      "permissions" : [ "cognito-idp:UpdateGroup", "iam:PassRole", "iam:PutRolePolicy" ],
      "timeoutInMinutes" : 5
    },
    "delete" : {
      "permissions" : [ "cognito-idp:DeleteGroup", "cognito-idp:GetGroup", "iam:PutRolePolicy" ],
      "timeoutInMinutes" : 5
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "UserPoolId" : {
            "$ref" : "resource-schema.json#/properties/UserPoolId"
          }
        },
        "required" : [ "UserPoolId" ]
      },
      "permissions" : [ "cognito-idp:ListGroups" ]
    }
  }
}