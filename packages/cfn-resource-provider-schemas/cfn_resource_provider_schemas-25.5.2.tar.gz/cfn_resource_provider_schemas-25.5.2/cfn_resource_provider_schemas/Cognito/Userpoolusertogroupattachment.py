SCHEMA = {
  "typeName" : "AWS::Cognito::UserPoolUserToGroupAttachment",
  "description" : "Resource Type definition for AWS::Cognito::UserPoolUserToGroupAttachment",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "properties" : {
    "UserPoolId" : {
      "type" : "string"
    },
    "Username" : {
      "type" : "string"
    },
    "GroupName" : {
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
  "required" : [ "UserPoolId", "Username", "GroupName" ],
  "createOnlyProperties" : [ "/properties/UserPoolId", "/properties/GroupName", "/properties/Username" ],
  "primaryIdentifier" : [ "/properties/UserPoolId", "/properties/GroupName", "/properties/Username" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:AdminAddUserToGroup", "cognito-idp:AdminListGroupsForUser" ],
      "timeoutInMinutes" : 2
    },
    "delete" : {
      "permissions" : [ "cognito-idp:AdminRemoveUserFromGroup", "cognito-idp:AdminListGroupsForUser" ],
      "timeoutInMinutes" : 2
    },
    "read" : {
      "permissions" : [ "cognito-idp:AdminListGroupsForUser" ]
    }
  }
}