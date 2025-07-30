SCHEMA = {
  "typeName" : "AWS::Glue::Connection",
  "description" : "Resource Type definition for AWS::Glue::Connection",
  "additionalProperties" : False,
  "properties" : {
    "ConnectionInput" : {
      "$ref" : "#/definitions/ConnectionInput"
    },
    "CatalogId" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "OAuth2PropertiesInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AuthorizationCodeProperties" : {
          "$ref" : "#/definitions/AuthorizationCodeProperties"
        },
        "OAuth2ClientApplication" : {
          "$ref" : "#/definitions/OAuth2ClientApplication"
        },
        "TokenUrl" : {
          "type" : "string"
        },
        "OAuth2Credentials" : {
          "$ref" : "#/definitions/OAuth2Credentials"
        },
        "OAuth2GrantType" : {
          "type" : "string"
        },
        "TokenUrlParametersMap" : {
          "type" : "object"
        }
      }
    },
    "ConnectionInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AuthenticationConfiguration" : {
          "$ref" : "#/definitions/AuthenticationConfigurationInput"
        },
        "PythonProperties" : {
          "type" : "object"
        },
        "Description" : {
          "type" : "string"
        },
        "ConnectionType" : {
          "type" : "string"
        },
        "MatchCriteria" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "ConnectionProperties" : {
          "type" : "object"
        },
        "AthenaProperties" : {
          "type" : "object"
        },
        "ValidateForComputeEnvironments" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Name" : {
          "type" : "string"
        },
        "SparkProperties" : {
          "type" : "object"
        },
        "PhysicalConnectionRequirements" : {
          "$ref" : "#/definitions/PhysicalConnectionRequirements"
        },
        "ValidateCredentials" : {
          "type" : "boolean"
        }
      },
      "required" : [ "ConnectionType" ]
    },
    "PhysicalConnectionRequirements" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AvailabilityZone" : {
          "type" : "string"
        },
        "SecurityGroupIdList" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetId" : {
          "type" : "string"
        }
      }
    },
    "BasicAuthenticationCredentials" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Username" : {
          "type" : "string"
        },
        "Password" : {
          "type" : "string"
        }
      }
    },
    "AuthorizationCodeProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AuthorizationCode" : {
          "type" : "string"
        },
        "RedirectUri" : {
          "type" : "string"
        }
      }
    },
    "OAuth2ClientApplication" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AWSManagedClientApplicationReference" : {
          "type" : "string"
        },
        "UserManagedClientApplicationClientId" : {
          "type" : "string"
        }
      }
    },
    "OAuth2Credentials" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "UserManagedClientApplicationClientSecret" : {
          "type" : "string"
        },
        "JwtToken" : {
          "type" : "string"
        },
        "RefreshToken" : {
          "type" : "string"
        },
        "AccessToken" : {
          "type" : "string"
        }
      }
    },
    "AuthenticationConfigurationInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretArn" : {
          "type" : "string"
        },
        "KmsKeyArn" : {
          "type" : "string"
        },
        "OAuth2Properties" : {
          "$ref" : "#/definitions/OAuth2PropertiesInput"
        },
        "CustomAuthenticationCredentials" : {
          "type" : "object"
        },
        "BasicAuthenticationCredentials" : {
          "$ref" : "#/definitions/BasicAuthenticationCredentials"
        },
        "AuthenticationType" : {
          "type" : "string"
        }
      },
      "required" : [ "AuthenticationType" ]
    }
  },
  "required" : [ "ConnectionInput", "CatalogId" ],
  "createOnlyProperties" : [ "/properties/CatalogId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}