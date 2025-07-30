SCHEMA = {
  "typeName" : "AWS::LicenseManager::License",
  "description" : "Resource Type definition for AWS::LicenseManager::License",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-licensemanager.git",
  "definitions" : {
    "ValidityDateFormat" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Begin" : {
          "description" : "Validity begin date for the license.",
          "type" : "string",
          "format" : "date-time"
        },
        "End" : {
          "description" : "Validity begin date for the license.",
          "type" : "string",
          "format" : "date-time"
        }
      },
      "required" : [ "Begin", "End" ]
    },
    "IssuerData" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "SignKey" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "Entitlement" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        },
        "MaxCount" : {
          "type" : "integer"
        },
        "Overage" : {
          "type" : "boolean"
        },
        "Unit" : {
          "type" : "string"
        },
        "AllowCheckIn" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Name", "Unit" ],
      "additionalProperties" : False
    },
    "ConsumptionConfiguration" : {
      "type" : "object",
      "properties" : {
        "RenewType" : {
          "type" : "string"
        },
        "ProvisionalConfiguration" : {
          "$ref" : "#/definitions/ProvisionalConfiguration"
        },
        "BorrowConfiguration" : {
          "$ref" : "#/definitions/BorrowConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "ProvisionalConfiguration" : {
      "type" : "object",
      "properties" : {
        "MaxTimeToLiveInMinutes" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxTimeToLiveInMinutes" ],
      "additionalProperties" : False
    },
    "BorrowConfiguration" : {
      "type" : "object",
      "properties" : {
        "MaxTimeToLiveInMinutes" : {
          "type" : "integer"
        },
        "AllowEarlyCheckIn" : {
          "type" : "boolean"
        }
      },
      "required" : [ "MaxTimeToLiveInMinutes", "AllowEarlyCheckIn" ],
      "additionalProperties" : False
    },
    "Metadata" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Name", "Value" ],
      "additionalProperties" : False
    },
    "LicenseStatus" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string",
      "maxLength" : 2048
    }
  },
  "properties" : {
    "ProductSKU" : {
      "description" : "ProductSKU of the license.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1024
    },
    "Issuer" : {
      "$ref" : "#/definitions/IssuerData"
    },
    "LicenseName" : {
      "description" : "Name for the created license.",
      "type" : "string"
    },
    "ProductName" : {
      "description" : "Product name for the created license.",
      "type" : "string"
    },
    "HomeRegion" : {
      "description" : "Home region for the created license.",
      "type" : "string"
    },
    "Validity" : {
      "$ref" : "#/definitions/ValidityDateFormat"
    },
    "Entitlements" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Entitlement"
      }
    },
    "Beneficiary" : {
      "description" : "Beneficiary of the license.",
      "type" : "string"
    },
    "ConsumptionConfiguration" : {
      "$ref" : "#/definitions/ConsumptionConfiguration"
    },
    "LicenseMetadata" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Metadata"
      }
    },
    "LicenseArn" : {
      "description" : "Amazon Resource Name is a unique name for each resource.",
      "$ref" : "#/definitions/Arn"
    },
    "Status" : {
      "$ref" : "#/definitions/LicenseStatus"
    },
    "Version" : {
      "description" : "The version of the license.",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "LicenseName", "ProductName", "Issuer", "HomeRegion", "Validity", "ConsumptionConfiguration", "Entitlements" ],
  "writeOnlyProperties" : [ "/properties/Status" ],
  "readOnlyProperties" : [ "/properties/LicenseArn", "/properties/Version" ],
  "primaryIdentifier" : [ "/properties/LicenseArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "license-manager:CreateLicense" ]
    },
    "read" : {
      "permissions" : [ "license-manager:GetLicense" ]
    },
    "update" : {
      "permissions" : [ "license-manager:CreateLicenseVersion" ]
    },
    "delete" : {
      "permissions" : [ "license-manager:DeleteLicense" ]
    },
    "list" : {
      "permissions" : [ "license-manager:ListLicenses" ]
    }
  }
}