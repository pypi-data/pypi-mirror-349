SCHEMA = {
  "typeName" : "AWS::WAFRegional::Rule",
  "description" : "Resource Type definition for AWS::WAFRegional::Rule",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "MetricName" : {
      "type" : "string"
    },
    "Predicates" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Predicate"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Predicate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "DataId" : {
          "type" : "string"
        },
        "Negated" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Type", "Negated", "DataId" ]
    }
  },
  "required" : [ "MetricName", "Name" ],
  "createOnlyProperties" : [ "/properties/MetricName", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}