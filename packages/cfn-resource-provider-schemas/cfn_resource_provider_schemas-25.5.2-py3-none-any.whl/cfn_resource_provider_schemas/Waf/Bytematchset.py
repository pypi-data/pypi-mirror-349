SCHEMA = {
  "typeName" : "AWS::WAF::ByteMatchSet",
  "description" : "Resource Type definition for AWS::WAF::ByteMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "ByteMatchTuples" : {
      "type" : "array",
      "uniqueItems" : True,
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
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        },
        "PositionalConstraint" : {
          "type" : "string"
        },
        "TargetString" : {
          "type" : "string"
        },
        "TargetStringBase64" : {
          "type" : "string"
        },
        "TextTransformation" : {
          "type" : "string"
        }
      },
      "required" : [ "PositionalConstraint", "TextTransformation", "FieldToMatch" ]
    },
    "FieldToMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Data" : {
          "type" : "string"
        },
        "Type" : {
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