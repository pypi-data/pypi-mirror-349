SCHEMA = {
  "typeName" : "AWS::WAF::IPSet",
  "description" : "Resource Type definition for AWS::WAF::IPSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "IPSetDescriptors" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/IPSetDescriptor"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "IPSetDescriptor" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Type" ]
    }
  },
  "required" : [ "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}