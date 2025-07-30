SCHEMA = {
  "typeName" : "AWS::LakeFormation::Permissions",
  "description" : "Resource Type definition for AWS::LakeFormation::Permissions",
  "additionalProperties" : False,
  "properties" : {
    "Resource" : {
      "$ref" : "#/definitions/Resource"
    },
    "Permissions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "DataLakePrincipal" : {
      "$ref" : "#/definitions/DataLakePrincipal"
    },
    "PermissionsWithGrantOption" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "definitions" : {
    "DataLakePrincipal" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DataLakePrincipalIdentifier" : {
          "type" : "string"
        }
      }
    },
    "TableResource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatabaseName" : {
          "type" : "string"
        },
        "CatalogId" : {
          "type" : "string"
        },
        "TableWildcard" : {
          "$ref" : "#/definitions/TableWildcard"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "Resource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatabaseResource" : {
          "$ref" : "#/definitions/DatabaseResource"
        },
        "DataLocationResource" : {
          "$ref" : "#/definitions/DataLocationResource"
        },
        "TableWithColumnsResource" : {
          "$ref" : "#/definitions/TableWithColumnsResource"
        },
        "TableResource" : {
          "$ref" : "#/definitions/TableResource"
        }
      }
    },
    "DatabaseResource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CatalogId" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "DataLocationResource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3Resource" : {
          "type" : "string"
        },
        "CatalogId" : {
          "type" : "string"
        }
      }
    },
    "TableWildcard" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "TableWithColumnsResource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatabaseName" : {
          "type" : "string"
        },
        "ColumnNames" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "CatalogId" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        },
        "ColumnWildcard" : {
          "$ref" : "#/definitions/ColumnWildcard"
        }
      }
    },
    "ColumnWildcard" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ExcludedColumnNames" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    }
  },
  "required" : [ "DataLakePrincipal", "Resource" ],
  "createOnlyProperties" : [ "/properties/DataLakePrincipal", "/properties/Resource" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}