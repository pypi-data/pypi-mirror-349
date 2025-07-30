SCHEMA = {
  "typeName" : "AWS::DAX::ParameterGroup",
  "description" : "Resource Type definition for AWS::DAX::ParameterGroup",
  "additionalProperties" : False,
  "properties" : {
    "ParameterNameValues" : {
      "type" : "object"
    },
    "Description" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "ParameterGroupName" : {
      "type" : "string"
    }
  },
  "createOnlyProperties" : [ "/properties/ParameterGroupName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}