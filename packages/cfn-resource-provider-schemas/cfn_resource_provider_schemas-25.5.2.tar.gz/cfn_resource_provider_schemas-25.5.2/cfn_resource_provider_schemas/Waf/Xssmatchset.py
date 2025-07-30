SCHEMA = {
  "typeName" : "AWS::WAF::XssMatchSet",
  "description" : "Resource Type definition for AWS::WAF::XssMatchSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "XssMatchTuples" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/XssMatchTuple"
      }
    }
  },
  "definitions" : {
    "XssMatchTuple" : {
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
  "required" : [ "Name", "XssMatchTuples" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}