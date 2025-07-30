SCHEMA = {
  "typeName" : "AWS::WAFRegional::ByteMatchSet",
  "description" : "Resource Type definition for AWS::WAFRegional::ByteMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "ByteMatchTuples" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ByteMatchTuple"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ByteMatchTuple" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetString" : {
          "type" : "string"
        },
        "TargetStringBase64" : {
          "type" : "string"
        },
        "PositionalConstraint" : {
          "type" : "string"
        },
        "TextTransformation" : {
          "type" : "string"
        },
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        }
      },
      "required" : [ "PositionalConstraint", "TextTransformation", "FieldToMatch" ]
    },
    "FieldToMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Data" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    }
  },
  "required" : [ "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}