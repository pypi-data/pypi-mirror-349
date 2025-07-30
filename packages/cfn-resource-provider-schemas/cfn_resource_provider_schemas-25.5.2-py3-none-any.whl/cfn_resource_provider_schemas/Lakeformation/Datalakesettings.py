SCHEMA = {
  "typeName" : "AWS::LakeFormation::DataLakeSettings",
  "description" : "Resource Type definition for AWS::LakeFormation::DataLakeSettings",
  "additionalProperties" : False,
  "properties" : {
    "AllowExternalDataFiltering" : {
      "type" : "boolean"
    },
    "ExternalDataFilteringAllowList" : {
      "$ref" : "#/definitions/ExternalDataFilteringAllowList"
    },
    "CreateTableDefaultPermissions" : {
      "$ref" : "#/definitions/CreateTableDefaultPermissions"
    },
    "MutationType" : {
      "type" : "string"
    },
    "Parameters" : {
      "type" : "object"
    },
    "AllowFullTableExternalDataAccess" : {
      "type" : "boolean"
    },
    "Admins" : {
      "$ref" : "#/definitions/Admins"
    },
    "CreateDatabaseDefaultPermissions" : {
      "$ref" : "#/definitions/CreateDatabaseDefaultPermissions"
    },
    "Id" : {
      "type" : "string"
    },
    "AuthorizedSessionTagValueList" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "TrustedResourceOwners" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "definitions" : {
    "ExternalDataFilteringAllowList" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "CreateTableDefaultPermissions" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "Admins" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "CreateDatabaseDefaultPermissions" : {
      "type" : "object",
      "additionalProperties" : False
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}