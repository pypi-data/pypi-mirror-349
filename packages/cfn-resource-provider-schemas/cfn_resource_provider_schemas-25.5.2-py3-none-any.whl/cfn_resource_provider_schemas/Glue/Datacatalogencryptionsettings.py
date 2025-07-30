SCHEMA = {
  "typeName" : "AWS::Glue::DataCatalogEncryptionSettings",
  "description" : "Resource Type definition for AWS::Glue::DataCatalogEncryptionSettings",
  "additionalProperties" : False,
  "properties" : {
    "CatalogId" : {
      "type" : "string"
    },
    "DataCatalogEncryptionSettings" : {
      "$ref" : "#/definitions/DataCatalogEncryptionSettings"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ConnectionPasswordEncryption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyId" : {
          "type" : "string"
        },
        "ReturnConnectionPasswordEncrypted" : {
          "type" : "boolean"
        }
      }
    },
    "EncryptionAtRest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CatalogEncryptionMode" : {
          "type" : "string"
        },
        "CatalogEncryptionServiceRole" : {
          "type" : "string"
        },
        "SseAwsKmsKeyId" : {
          "type" : "string"
        }
      }
    },
    "DataCatalogEncryptionSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectionPasswordEncryption" : {
          "$ref" : "#/definitions/ConnectionPasswordEncryption"
        },
        "EncryptionAtRest" : {
          "$ref" : "#/definitions/EncryptionAtRest"
        }
      }
    }
  },
  "required" : [ "DataCatalogEncryptionSettings", "CatalogId" ],
  "createOnlyProperties" : [ "/properties/CatalogId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}