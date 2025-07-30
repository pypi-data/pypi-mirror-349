SCHEMA = {
  "typeName" : "AWS::Pinpoint::ADMChannel",
  "description" : "Resource Type definition for AWS::Pinpoint::ADMChannel",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "ClientSecret" : {
      "type" : "string"
    },
    "Enabled" : {
      "type" : "boolean"
    },
    "ClientId" : {
      "type" : "string"
    },
    "ApplicationId" : {
      "type" : "string"
    }
  },
  "required" : [ "ApplicationId", "ClientId", "ClientSecret" ],
  "createOnlyProperties" : [ "/properties/ApplicationId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}