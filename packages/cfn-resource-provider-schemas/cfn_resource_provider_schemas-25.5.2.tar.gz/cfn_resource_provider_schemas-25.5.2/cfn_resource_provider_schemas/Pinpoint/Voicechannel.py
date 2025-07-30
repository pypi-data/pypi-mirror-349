SCHEMA = {
  "typeName" : "AWS::Pinpoint::VoiceChannel",
  "description" : "Resource Type definition for AWS::Pinpoint::VoiceChannel",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Enabled" : {
      "type" : "boolean"
    },
    "ApplicationId" : {
      "type" : "string"
    }
  },
  "required" : [ "ApplicationId" ],
  "createOnlyProperties" : [ "/properties/ApplicationId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}