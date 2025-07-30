SCHEMA = {
  "typeName" : "AWS::WAF::SqlInjectionMatchSet",
  "description" : "Resource Type definition for AWS::WAF::SqlInjectionMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "SqlInjectionMatchTuples" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/SqlInjectionMatchTuple"
      }
    }
  },
  "definitions" : {
    "SqlInjectionMatchTuple" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        },
        "TextTransformation" : {
          "type" : "string"
        }
      },
      "required" : [ "TextTransformation", "FieldToMatch" ]
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