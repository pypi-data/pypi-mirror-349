SCHEMA = {
  "typeName" : "AWS::Glue::Classifier",
  "description" : "Resource Type definition for AWS::Glue::Classifier",
  "additionalProperties" : False,
  "properties" : {
    "XMLClassifier" : {
      "$ref" : "#/definitions/XMLClassifier"
    },
    "CsvClassifier" : {
      "$ref" : "#/definitions/CsvClassifier"
    },
    "Id" : {
      "type" : "string"
    },
    "GrokClassifier" : {
      "$ref" : "#/definitions/GrokClassifier"
    },
    "JsonClassifier" : {
      "$ref" : "#/definitions/JsonClassifier"
    }
  },
  "definitions" : {
    "XMLClassifier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RowTag" : {
          "type" : "string"
        },
        "Classification" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "RowTag", "Classification" ]
    },
    "JsonClassifier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "JsonPath" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "JsonPath" ]
    },
    "CsvClassifier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContainsCustomDatatype" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "QuoteSymbol" : {
          "type" : "string"
        },
        "ContainsHeader" : {
          "type" : "string"
        },
        "Delimiter" : {
          "type" : "string"
        },
        "Header" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "AllowSingleColumn" : {
          "type" : "boolean"
        },
        "CustomDatatypeConfigured" : {
          "type" : "boolean"
        },
        "DisableValueTrimming" : {
          "type" : "boolean"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "GrokClassifier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CustomPatterns" : {
          "type" : "string"
        },
        "GrokPattern" : {
          "type" : "string"
        },
        "Classification" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "GrokPattern", "Classification" ]
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}