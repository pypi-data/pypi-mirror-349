SCHEMA = {
  "typeName" : "AWS::Glue::TableOptimizer",
  "description" : "Resource Type definition for AWS::Glue::TableOptimizer",
  "additionalProperties" : False,
  "properties" : {
    "DatabaseName" : {
      "type" : "string"
    },
    "TableName" : {
      "type" : "string"
    },
    "Type" : {
      "type" : "string"
    },
    "TableOptimizerConfiguration" : {
      "$ref" : "#/definitions/TableOptimizerConfiguration"
    },
    "Id" : {
      "type" : "string"
    },
    "CatalogId" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "RetentionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IcebergConfiguration" : {
          "$ref" : "#/definitions/IcebergConfiguration"
        }
      }
    },
    "OrphanFileDeletionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IcebergConfiguration" : {
          "$ref" : "#/definitions/IcebergConfiguration"
        }
      }
    },
    "TableOptimizerConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "RetentionConfiguration" : {
          "$ref" : "#/definitions/RetentionConfiguration"
        },
        "VpcConfiguration" : {
          "$ref" : "#/definitions/VpcConfiguration"
        },
        "RoleArn" : {
          "type" : "string"
        },
        "OrphanFileDeletionConfiguration" : {
          "$ref" : "#/definitions/OrphanFileDeletionConfiguration"
        }
      },
      "required" : [ "Enabled", "RoleArn" ]
    },
    "VpcConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GlueConnectionName" : {
          "type" : "string"
        }
      }
    },
    "IcebergConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OrphanFileRetentionPeriodInDays" : {
          "type" : "integer"
        },
        "Location" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "TableName", "Type", "DatabaseName", "TableOptimizerConfiguration", "CatalogId" ],
  "createOnlyProperties" : [ "/properties/TableName", "/properties/DatabaseName", "/properties/Type", "/properties/CatalogId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}