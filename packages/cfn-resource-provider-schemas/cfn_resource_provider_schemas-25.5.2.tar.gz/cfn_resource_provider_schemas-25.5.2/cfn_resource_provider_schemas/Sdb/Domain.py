SCHEMA = {
  "typeName" : "AWS::SDB::Domain",
  "description" : "Resource Type definition for AWS::SDB::Domain",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}