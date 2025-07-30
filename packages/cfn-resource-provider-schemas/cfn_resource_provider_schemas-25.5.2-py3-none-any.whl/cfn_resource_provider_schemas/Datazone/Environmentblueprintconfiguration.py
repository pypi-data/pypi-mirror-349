SCHEMA = {
  "tagging" : {
    "taggable" : False
  },
  "typeName" : "AWS::DataZone::EnvironmentBlueprintConfiguration",
  "readOnlyProperties" : [ "/properties/CreatedAt", "/properties/DomainId", "/properties/EnvironmentBlueprintId", "/properties/UpdatedAt" ],
  "description" : "Definition of AWS::DataZone::EnvironmentBlueprintConfiguration Resource Type",
  "createOnlyProperties" : [ "/properties/DomainIdentifier", "/properties/EnvironmentBlueprintIdentifier" ],
  "primaryIdentifier" : [ "/properties/DomainId", "/properties/EnvironmentBlueprintId" ],
  "required" : [ "DomainIdentifier", "EnvironmentBlueprintIdentifier", "EnabledRegions" ],
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-datazone",
  "handlers" : {
    "read" : {
      "permissions" : [ "datazone:GetEnvironmentBlueprintConfiguration" ]
    },
    "create" : {
      "permissions" : [ "datazone:ListEnvironmentBlueprints", "iam:PassRole", "datazone:GetEnvironmentBlueprintConfiguration", "datazone:PutEnvironmentBlueprintConfiguration" ]
    },
    "update" : {
      "permissions" : [ "datazone:DeleteEnvironmentBlueprintConfiguration", "iam:PassRole", "datazone:GetEnvironmentBlueprintConfiguration", "datazone:PutEnvironmentBlueprintConfiguration" ]
    },
    "list" : {
      "permissions" : [ "datazone:ListEnvironmentBlueprintConfigurations" ],
      "handlerSchema" : {
        "properties" : {
          "DomainIdentifier" : {
            "$ref" : "resource-schema.json#/properties/DomainIdentifier"
          }
        },
        "required" : [ "DomainIdentifier" ]
      }
    },
    "delete" : {
      "permissions" : [ "datazone:GetEnvironmentBlueprintConfiguration", "datazone:DeleteEnvironmentBlueprintConfiguration" ]
    }
  },
  "additionalIdentifiers" : [ [ "/properties/DomainIdentifier", "/properties/EnvironmentBlueprintIdentifier" ] ],
  "writeOnlyProperties" : [ "/properties/DomainIdentifier", "/properties/EnvironmentBlueprintIdentifier", "/properties/EnvironmentRolePermissionBoundary", "/properties/ProvisioningConfigurations" ],
  "additionalProperties" : False,
  "definitions" : {
    "ProvisioningConfiguration" : {
      "oneOf" : [ {
        "additionalProperties" : False,
        "type" : "object",
        "title" : "LakeFormationConfiguration",
        "properties" : {
          "LakeFormationConfiguration" : {
            "$ref" : "#/definitions/LakeFormationConfiguration"
          }
        },
        "required" : [ "LakeFormationConfiguration" ]
      } ]
    },
    "LakeFormationConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LocationRegistrationExcludeS3Locations" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "^s3://.+$",
            "type" : "string",
            "maxLength" : 1024
          }
        },
        "LocationRegistrationRole" : {
          "pattern" : "^arn:aws[^:]*:iam::\\d{12}:(role|role/service-role)/[\\w+=,.@-]*$",
          "type" : "string"
        }
      }
    },
    "RegionalParameter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Parameters" : {
          "$ref" : "#/definitions/Parameter"
        },
        "Region" : {
          "pattern" : "^[a-z]{2}-?(iso|gov)?-{1}[a-z]*-{1}[0-9]$",
          "type" : "string"
        }
      }
    },
    "Parameter" : {
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False,
      "type" : "object"
    }
  },
  "properties" : {
    "CreatedAt" : {
      "format" : "date-time",
      "type" : "string"
    },
    "EnabledRegions" : {
      "minItems" : 0,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "minLength" : 4,
        "pattern" : "^[a-z]{2}-?(iso|gov)?-{1}[a-z]*-{1}[0-9]$",
        "type" : "string",
        "maxLength" : 16
      }
    },
    "EnvironmentBlueprintIdentifier" : {
      "pattern" : "^[a-zA-Z0-9_-]{1,36}$",
      "type" : "string"
    },
    "EnvironmentBlueprintId" : {
      "pattern" : "^[a-zA-Z0-9_-]{1,36}$",
      "type" : "string"
    },
    "UpdatedAt" : {
      "format" : "date-time",
      "type" : "string"
    },
    "RegionalParameters" : {
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/RegionalParameter"
      }
    },
    "ProvisioningRoleArn" : {
      "pattern" : "^arn:aws[^:]*:iam::\\d{12}:(role|role/service-role)/[\\w+=,.@-]*$",
      "type" : "string"
    },
    "DomainId" : {
      "pattern" : "^dzd[-_][a-zA-Z0-9_-]{1,36}$",
      "type" : "string"
    },
    "ProvisioningConfigurations" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ProvisioningConfiguration"
      }
    },
    "DomainIdentifier" : {
      "pattern" : "^dzd[-_][a-zA-Z0-9_-]{1,36}$",
      "type" : "string"
    },
    "EnvironmentRolePermissionBoundary" : {
      "pattern" : "^arn:aws[^:]*:iam::(aws|\\d{12}):policy/[\\w+=,.@-]*$",
      "type" : "string"
    },
    "ManageAccessRoleArn" : {
      "pattern" : "^arn:aws[^:]*:iam::\\d{12}:(role|role/service-role)/[\\w+=,.@-]*$",
      "type" : "string"
    }
  }
}