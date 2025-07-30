SCHEMA = {
  "typeName" : "AWS::AppSync::GraphQLSchema",
  "description" : "Resource Type definition for AWS::AppSync::GraphQLSchema",
  "additionalProperties" : False,
  "properties" : {
    "Definition" : {
      "type" : "string"
    },
    "DefinitionS3Location" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "ApiId" : {
      "type" : "string"
    }
  },
  "required" : [ "ApiId" ],
  "createOnlyProperties" : [ "/properties/ApiId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}