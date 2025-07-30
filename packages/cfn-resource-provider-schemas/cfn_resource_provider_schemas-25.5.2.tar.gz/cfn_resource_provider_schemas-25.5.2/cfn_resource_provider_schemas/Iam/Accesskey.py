SCHEMA = {
  "typeName" : "AWS::IAM::AccessKey",
  "description" : "Resource Type definition for AWS::IAM::AccessKey",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SecretAccessKey" : {
      "type" : "string"
    },
    "Serial" : {
      "type" : "integer"
    },
    "Status" : {
      "type" : "string"
    },
    "UserName" : {
      "type" : "string"
    }
  },
  "required" : [ "UserName" ],
  "readOnlyProperties" : [ "/properties/SecretAccessKey", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/UserName", "/properties/Serial" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}