SCHEMA = {
  "typeName" : "AWS::DAX::SubnetGroup",
  "description" : "Resource Type definition for AWS::DAX::SubnetGroup",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "SubnetIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SubnetGroupName" : {
      "type" : "string"
    }
  },
  "required" : [ "SubnetIds" ],
  "createOnlyProperties" : [ "/properties/SubnetGroupName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}