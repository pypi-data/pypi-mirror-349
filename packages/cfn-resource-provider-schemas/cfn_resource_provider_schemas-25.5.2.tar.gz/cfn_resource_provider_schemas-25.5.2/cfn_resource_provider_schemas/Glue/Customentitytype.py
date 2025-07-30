SCHEMA = {
  "typeName" : "AWS::Glue::CustomEntityType",
  "description" : "Resource Type definition for AWS::Glue::CustomEntityType",
  "additionalProperties" : False,
  "properties" : {
    "RegexString" : {
      "type" : "string"
    },
    "ContextWords" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}