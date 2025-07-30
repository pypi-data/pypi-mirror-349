SCHEMA = {
  "typeName" : "AWS::EC2::TrafficMirrorFilter",
  "description" : "Resource Type definition for AWS::EC2::TrafficMirrorFilter",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "NetworkServices" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "createOnlyProperties" : [ "/properties/Description" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}