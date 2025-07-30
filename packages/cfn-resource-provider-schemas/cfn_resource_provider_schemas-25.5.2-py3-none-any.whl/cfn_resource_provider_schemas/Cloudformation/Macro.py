SCHEMA = {
  "typeName" : "AWS::CloudFormation::Macro",
  "description" : "Resource Type definition for AWS::CloudFormation::Macro",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "FunctionName" : {
      "type" : "string"
    },
    "LogGroupName" : {
      "type" : "string"
    },
    "LogRoleARN" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "required" : [ "FunctionName", "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}