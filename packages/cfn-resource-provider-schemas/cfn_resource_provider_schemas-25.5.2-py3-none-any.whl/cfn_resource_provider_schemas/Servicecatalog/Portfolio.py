SCHEMA = {
  "typeName" : "AWS::ServiceCatalog::Portfolio",
  "description" : "Resource Type definition for AWS::ServiceCatalog::Portfolio",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "PortfolioName" : {
      "type" : "string"
    },
    "ProviderName" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "DisplayName" : {
      "type" : "string"
    },
    "AcceptLanguage" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "required" : [ "DisplayName", "ProviderName" ],
  "readOnlyProperties" : [ "/properties/PortfolioName", "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}