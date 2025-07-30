SCHEMA = {
  "typeName" : "AWS::OpsWorks::Stack",
  "description" : "Resource Type definition for AWS::OpsWorks::Stack",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "AgentVersion" : {
      "type" : "string"
    },
    "Attributes" : {
      "type" : "object",
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : "string"
        }
      }
    },
    "ChefConfiguration" : {
      "$ref" : "#/definitions/ChefConfiguration"
    },
    "CloneAppIds" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "ClonePermissions" : {
      "type" : "boolean"
    },
    "ConfigurationManager" : {
      "$ref" : "#/definitions/StackConfigurationManager"
    },
    "CustomCookbooksSource" : {
      "$ref" : "#/definitions/Source"
    },
    "CustomJson" : {
      "type" : "object"
    },
    "DefaultAvailabilityZone" : {
      "type" : "string"
    },
    "DefaultInstanceProfileArn" : {
      "type" : "string"
    },
    "DefaultOs" : {
      "type" : "string"
    },
    "DefaultRootDeviceType" : {
      "type" : "string"
    },
    "DefaultSshKeyName" : {
      "type" : "string"
    },
    "DefaultSubnetId" : {
      "type" : "string"
    },
    "EcsClusterArn" : {
      "type" : "string"
    },
    "ElasticIps" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/ElasticIp"
      }
    },
    "HostnameTheme" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "RdsDbInstances" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/RdsDbInstance"
      }
    },
    "ServiceRoleArn" : {
      "type" : "string"
    },
    "SourceStackId" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "UseCustomCookbooks" : {
      "type" : "boolean"
    },
    "UseOpsworksSecurityGroups" : {
      "type" : "boolean"
    },
    "VpcId" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Source" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Password" : {
          "type" : "string"
        },
        "Revision" : {
          "type" : "string"
        },
        "SshKey" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Url" : {
          "type" : "string"
        },
        "Username" : {
          "type" : "string"
        }
      }
    },
    "StackConfigurationManager" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Version" : {
          "type" : "string"
        }
      }
    },
    "RdsDbInstance" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DbPassword" : {
          "type" : "string"
        },
        "DbUser" : {
          "type" : "string"
        },
        "RdsDbInstanceArn" : {
          "type" : "string"
        }
      },
      "required" : [ "DbPassword", "DbUser", "RdsDbInstanceArn" ]
    },
    "ElasticIp" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Ip" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Ip" ]
    },
    "ChefConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BerkshelfVersion" : {
          "type" : "string"
        },
        "ManageBerkshelf" : {
          "type" : "boolean"
        }
      }
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "required" : [ "DefaultInstanceProfileArn", "ServiceRoleArn", "Name" ],
  "createOnlyProperties" : [ "/properties/ServiceRoleArn", "/properties/CloneAppIds", "/properties/ClonePermissions", "/properties/VpcId", "/properties/SourceStackId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}