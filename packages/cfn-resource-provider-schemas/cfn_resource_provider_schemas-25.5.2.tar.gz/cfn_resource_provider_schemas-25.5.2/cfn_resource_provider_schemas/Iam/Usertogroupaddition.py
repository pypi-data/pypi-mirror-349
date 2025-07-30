SCHEMA = {
  "typeName" : "AWS::IAM::UserToGroupAddition",
  "description" : "Resource Type definition for AWS::IAM::UserToGroupAddition",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "GroupName" : {
      "type" : "string"
    },
    "Users" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "required" : [ "GroupName", "Users" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}