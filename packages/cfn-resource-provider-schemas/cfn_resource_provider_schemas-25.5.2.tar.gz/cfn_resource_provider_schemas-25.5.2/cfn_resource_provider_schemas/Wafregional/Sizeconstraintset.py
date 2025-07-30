SCHEMA = {
  "typeName" : "AWS::WAFRegional::SizeConstraintSet",
  "description" : "Resource Type definition for AWS::WAFRegional::SizeConstraintSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SizeConstraints" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/SizeConstraint"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "SizeConstraint" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ComparisonOperator" : {
          "type" : "string"
        },
        "Size" : {
          "type" : "integer"
        },
        "TextTransformation" : {
          "type" : "string"
        },
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        }
      },
      "required" : [ "ComparisonOperator", "TextTransformation", "Size", "FieldToMatch" ]
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