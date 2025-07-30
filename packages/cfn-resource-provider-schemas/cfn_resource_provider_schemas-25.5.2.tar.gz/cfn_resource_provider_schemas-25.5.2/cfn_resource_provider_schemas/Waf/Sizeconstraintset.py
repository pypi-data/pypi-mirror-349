SCHEMA = {
  "typeName" : "AWS::WAF::SizeConstraintSet",
  "description" : "Resource Type definition for AWS::WAF::SizeConstraintSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "SizeConstraints" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/SizeConstraint"
      }
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
        "FieldToMatch" : {
          "$ref" : "#/definitions/FieldToMatch"
        },
        "Size" : {
          "type" : "integer"
        },
        "TextTransformation" : {
          "type" : "string"
        }
      },
      "required" : [ "ComparisonOperator", "TextTransformation", "FieldToMatch", "Size" ]
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
  "required" : [ "SizeConstraints", "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}