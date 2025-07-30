SCHEMA = {
  "typeName" : "AWS::NetworkFirewall::TLSInspectionConfiguration",
  "description" : "Resource type definition for AWS::NetworkFirewall::TLSInspectionConfiguration",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-networkfirewall.git",
  "additionalProperties" : False,
  "definitions" : {
    "ResourceArn" : {
      "description" : "A resource ARN.",
      "type" : "string",
      "pattern" : "^(arn:aws.*)$",
      "minLength" : 1,
      "maxLength" : 256
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^.*$"
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 255,
          "pattern" : "^.*$"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "TLSInspectionConfiguration" : {
      "type" : "object",
      "properties" : {
        "ServerCertificateConfigurations" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ServerCertificateConfiguration"
          }
        }
      },
      "additionalProperties" : False
    },
    "ServerCertificateConfiguration" : {
      "type" : "object",
      "properties" : {
        "ServerCertificates" : {
          "type" : "array",
          "insertionOrder" : False,
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/ServerCertificate"
          }
        },
        "Scopes" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ServerCertificateScope"
          }
        },
        "CertificateAuthorityArn" : {
          "$ref" : "#/definitions/ResourceArn"
        },
        "CheckCertificateRevocationStatus" : {
          "type" : "object",
          "properties" : {
            "RevokedStatusAction" : {
              "$ref" : "#/definitions/RevokedStatusAction"
            },
            "UnknownStatusAction" : {
              "$ref" : "#/definitions/UnknownStatusAction"
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "RevokedStatusAction" : {
      "type" : "string",
      "enum" : [ "PASS", "DROP", "REJECT" ]
    },
    "UnknownStatusAction" : {
      "type" : "string",
      "enum" : [ "PASS", "DROP", "REJECT" ]
    },
    "ServerCertificate" : {
      "type" : "object",
      "properties" : {
        "ResourceArn" : {
          "$ref" : "#/definitions/ResourceArn"
        }
      },
      "additionalProperties" : False
    },
    "ServerCertificateScope" : {
      "type" : "object",
      "properties" : {
        "Sources" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Address"
          }
        },
        "Destinations" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Address"
          }
        },
        "SourcePorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "DestinationPorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "Protocols" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ProtocolNumber"
          }
        }
      },
      "additionalProperties" : False
    },
    "Address" : {
      "type" : "object",
      "properties" : {
        "AddressDefinition" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255,
          "pattern" : "^([a-fA-F\\d:\\.]+/\\d{1,3})$"
        }
      },
      "required" : [ "AddressDefinition" ],
      "additionalProperties" : False
    },
    "PortRange" : {
      "type" : "object",
      "properties" : {
        "FromPort" : {
          "$ref" : "#/definitions/PortRangeBound"
        },
        "ToPort" : {
          "$ref" : "#/definitions/PortRangeBound"
        }
      },
      "required" : [ "FromPort", "ToPort" ],
      "additionalProperties" : False
    },
    "PortRangeBound" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 65535
    },
    "ProtocolNumber" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 255
    }
  },
  "properties" : {
    "TLSInspectionConfigurationName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128,
      "pattern" : "^[a-zA-Z0-9-]+$"
    },
    "TLSInspectionConfigurationArn" : {
      "$ref" : "#/definitions/ResourceArn"
    },
    "TLSInspectionConfiguration" : {
      "$ref" : "#/definitions/TLSInspectionConfiguration"
    },
    "TLSInspectionConfigurationId" : {
      "type" : "string",
      "minLength" : 36,
      "maxLength" : 36,
      "pattern" : "^([0-9a-f]{8})-([0-9a-f]{4}-){3}([0-9a-f]{12})$"
    },
    "Description" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 512,
      "pattern" : "^.*$"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "network-firewall:TagResource", "network-firewall:UntagResource", "network-firewall:ListTagsForResource" ]
  },
  "required" : [ "TLSInspectionConfigurationName", "TLSInspectionConfiguration" ],
  "readOnlyProperties" : [ "/properties/TLSInspectionConfigurationArn", "/properties/TLSInspectionConfigurationId" ],
  "primaryIdentifier" : [ "/properties/TLSInspectionConfigurationArn" ],
  "createOnlyProperties" : [ "/properties/TLSInspectionConfigurationName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:CreateServiceLinkedRole", "network-firewall:CreateTLSInspectionConfiguration", "network-firewall:DescribeTLSInspectionConfiguration", "network-firewall:TagResource" ]
    },
    "read" : {
      "permissions" : [ "network-firewall:DescribeTLSInspectionConfiguration", "network-firewall:ListTagsForResources" ]
    },
    "update" : {
      "permissions" : [ "network-firewall:UpdateTLSInspectionConfiguration", "network-firewall:DescribeTLSInspectionConfiguration", "network-firewall:TagResource", "network-firewall:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "network-firewall:DeleteTLSInspectionConfiguration", "network-firewall:DescribeTLSInspectionConfiguration", "network-firewall:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "network-firewall:ListTLSInspectionConfigurations" ]
    }
  }
}