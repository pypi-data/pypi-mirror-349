SCHEMA = {
  "typeName" : "AWS::Glue::DataQualityRuleset",
  "description" : "Resource Type definition for AWS::Glue::DataQualityRuleset",
  "additionalProperties" : False,
  "properties" : {
    "Ruleset" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "TargetTable" : {
      "$ref" : "#/definitions/DataQualityTargetTable"
    },
    "Id" : {
      "type" : "string"
    },
    "ClientToken" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "DataQualityTargetTable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatabaseName" : {
          "type" : "string"
        },
        "TableName" : {
          "type" : "string"
        }
      }
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}