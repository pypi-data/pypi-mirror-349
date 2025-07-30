SCHEMA = {
  "typeName" : "AWS::WAFRegional::GeoMatchSet",
  "description" : "Resource Type definition for AWS::WAFRegional::GeoMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "GeoMatchConstraints" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/GeoMatchConstraint"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "GeoMatchConstraint" : {
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