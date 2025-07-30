SCHEMA = {
  "typeName" : "AWS::WAFRegional::SqlInjectionMatchSet",
  "description" : "Resource Type definition for AWS::WAFRegional::SqlInjectionMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SqlInjectionMatchTuples" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/SqlInjectionMatchTuple"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "SqlInjectionMatchTuple" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TextTransformation" : {
          "type" : "string"
        },
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        }
      },
      "required" : [ "TextTransformation", "FieldToMatch" ]
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