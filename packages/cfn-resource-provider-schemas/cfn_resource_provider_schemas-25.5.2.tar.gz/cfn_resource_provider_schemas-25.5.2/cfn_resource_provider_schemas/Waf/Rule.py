SCHEMA = {
  "typeName" : "AWS::WAF::Rule",
  "description" : "Resource Type definition for AWS::WAF::Rule",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "MetricName" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "Predicates" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Predicate"
      }
    }
  },
  "definitions" : {
    "Predicate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DataId" : {
          "type" : "string"
        },
        "Negated" : {
          "type" : "boolean"
        },
        "Type" : {
          "type" : "string"
        }
      },
      "required" : [ "Negated", "Type", "DataId" ]
    }
  },
  "required" : [ "MetricName", "Name" ],
  "createOnlyProperties" : [ "/properties/MetricName", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}