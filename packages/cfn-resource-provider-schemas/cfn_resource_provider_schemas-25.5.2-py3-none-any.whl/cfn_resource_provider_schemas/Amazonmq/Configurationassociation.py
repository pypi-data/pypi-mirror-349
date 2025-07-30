SCHEMA = {
  "typeName" : "AWS::AmazonMQ::ConfigurationAssociation",
  "description" : "Resource Type definition for AWS::AmazonMQ::ConfigurationAssociation",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Broker" : {
      "type" : "string"
    },
    "Configuration" : {
      "$ref" : "#/definitions/ConfigurationId"
    }
  },
  "definitions" : {
    "ConfigurationId" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Revision" : {
          "type" : "integer"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "Revision", "Id" ]
    }
  },
  "required" : [ "Configuration", "Broker" ],
  "createOnlyProperties" : [ "/properties/Broker" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}