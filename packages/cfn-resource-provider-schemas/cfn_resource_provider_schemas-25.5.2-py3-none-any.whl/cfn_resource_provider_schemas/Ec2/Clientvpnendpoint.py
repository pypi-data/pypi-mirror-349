SCHEMA = {
  "typeName" : "AWS::EC2::ClientVpnEndpoint",
  "description" : "Resource Type definition for AWS::EC2::ClientVpnEndpoint",
  "additionalProperties" : False,
  "properties" : {
    "ClientCidrBlock" : {
      "type" : "string"
    },
    "ClientConnectOptions" : {
      "$ref" : "#/definitions/ClientConnectOptions"
    },
    "Description" : {
      "type" : "string"
    },
    "ClientRouteEnforcementOptions" : {
      "$ref" : "#/definitions/ClientRouteEnforcementOptions"
    },
    "TagSpecifications" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/TagSpecification"
      }
    },
    "AuthenticationOptions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ClientAuthenticationRequest"
      }
    },
    "ServerCertificateArn" : {
      "type" : "string"
    },
    "SessionTimeoutHours" : {
      "type" : "integer"
    },
    "DnsServers" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "DisconnectOnSessionTimeout" : {
      "type" : "boolean"
    },
    "ConnectionLogOptions" : {
      "$ref" : "#/definitions/ConnectionLogOptions"
    },
    "SplitTunnel" : {
      "type" : "boolean"
    },
    "ClientLoginBannerOptions" : {
      "$ref" : "#/definitions/ClientLoginBannerOptions"
    },
    "VpcId" : {
      "type" : "string"
    },
    "SelfServicePortal" : {
      "type" : "string"
    },
    "TransportProtocol" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "VpnPort" : {
      "type" : "integer"
    }
  },
  "definitions" : {
    "ConnectionLogOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "CloudwatchLogGroup" : {
          "type" : "string"
        },
        "CloudwatchLogStream" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    },
    "ClientConnectOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "LambdaFunctionArn" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    },
    "FederatedAuthenticationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SAMLProviderArn" : {
          "type" : "string"
        },
        "SelfServiceSAMLProviderArn" : {
          "type" : "string"
        }
      },
      "required" : [ "SAMLProviderArn" ]
    },
    "ClientRouteEnforcementOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enforced" : {
          "type" : "boolean"
        }
      }
    },
    "ClientLoginBannerOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "BannerText" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    },
    "DirectoryServiceAuthenticationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DirectoryId" : {
          "type" : "string"
        }
      },
      "required" : [ "DirectoryId" ]
    },
    "CertificateAuthenticationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientRootCertificateChainArn" : {
          "type" : "string"
        }
      },
      "required" : [ "ClientRootCertificateChainArn" ]
    },
    "ClientAuthenticationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MutualAuthentication" : {
          "$ref" : "#/definitions/CertificateAuthenticationRequest"
        },
        "Type" : {
          "type" : "string"
        },
        "ActiveDirectory" : {
          "$ref" : "#/definitions/DirectoryServiceAuthenticationRequest"
        },
        "FederatedAuthentication" : {
          "$ref" : "#/definitions/FederatedAuthenticationRequest"
        }
      },
      "required" : [ "Type" ]
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "TagSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceType" : {
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
      "required" : [ "ResourceType", "Tags" ]
    }
  },
  "required" : [ "ClientCidrBlock", "ConnectionLogOptions", "AuthenticationOptions", "ServerCertificateArn" ],
  "createOnlyProperties" : [ "/properties/TransportProtocol", "/properties/ClientCidrBlock", "/properties/TagSpecifications", "/properties/AuthenticationOptions" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}