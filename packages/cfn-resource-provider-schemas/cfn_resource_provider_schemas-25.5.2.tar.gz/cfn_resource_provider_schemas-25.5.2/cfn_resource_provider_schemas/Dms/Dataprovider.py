SCHEMA = {
  "typeName" : "AWS::DMS::DataProvider",
  "description" : "Resource schema for AWS::DMS::DataProvider",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-dms.git",
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "dms:AddTagsToResource", "dms:RemoveTagsFromResource", "dms:ListTagsForResource" ]
  },
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "DmsSslModeValue" : {
      "type" : "string",
      "enum" : [ "none", "require", "verify-ca", "verify-full" ]
    },
    "Db2SslModeValue" : {
      "type" : "string",
      "enum" : [ "none", "verify-ca" ]
    },
    "MongoDbSslModeValue" : {
      "type" : "string",
      "enum" : [ "none", "require", "verify-full" ]
    },
    "MongoDbAuthType" : {
      "type" : "string",
      "enum" : [ "no", "password" ]
    },
    "MongoDbAuthMechanism" : {
      "type" : "string",
      "enum" : [ "default", "mongodb_cr", "scram_sha_1" ]
    }
  },
  "properties" : {
    "DataProviderName" : {
      "description" : "The property describes a name to identify the data provider.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "DataProviderIdentifier" : {
      "description" : "The property describes an identifier for the data provider. It is used for describing/deleting/modifying can be name/arn",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "DataProviderArn" : {
      "description" : "The data provider ARN.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "DataProviderCreationTime" : {
      "description" : "The data provider creation time.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 40
    },
    "Description" : {
      "description" : "The optional description of the data provider.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Engine" : {
      "description" : "The property describes a data engine for the data provider.",
      "type" : "string",
      "enum" : [ "aurora", "aurora_postgresql", "mysql", "oracle", "postgres", "sqlserver", "redshift", "mariadb", "mongodb", "docdb", "db2", "db2_zos" ]
    },
    "ExactSettings" : {
      "description" : "The property describes the exact settings which can be modified",
      "type" : "boolean",
      "default" : False
    },
    "Settings" : {
      "description" : "The property identifies the exact type of settings for the data provider.",
      "type" : "object",
      "properties" : {
        "PostgreSqlSettings" : {
          "description" : "PostgreSqlSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/DmsSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode", "DatabaseName" ],
          "additionalProperties" : False
        },
        "MySqlSettings" : {
          "description" : "MySqlSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "SslMode" : {
              "$ref" : "#/definitions/DmsSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode" ],
          "additionalProperties" : False
        },
        "OracleSettings" : {
          "description" : "OracleSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/DmsSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            },
            "AsmServer" : {
              "type" : "string"
            },
            "SecretsManagerOracleAsmSecretId" : {
              "type" : "string"
            },
            "SecretsManagerOracleAsmAccessRoleArn" : {
              "type" : "string"
            },
            "SecretsManagerSecurityDbEncryptionSecretId" : {
              "type" : "string"
            },
            "SecretsManagerSecurityDbEncryptionAccessRoleArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode", "DatabaseName" ],
          "additionalProperties" : False
        },
        "MicrosoftSqlServerSettings" : {
          "description" : "MicrosoftSqlServerSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/DmsSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode", "DatabaseName" ],
          "additionalProperties" : False
        },
        "RedshiftSettings" : {
          "description" : "RedshiftSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "DatabaseName" ],
          "additionalProperties" : False
        },
        "MariaDbSettings" : {
          "description" : "MariaDbSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "SslMode" : {
              "$ref" : "#/definitions/DmsSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode" ],
          "additionalProperties" : False
        },
        "DocDbSettings" : {
          "description" : "DocDbSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/MongoDbSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "DatabaseName" ],
          "additionalProperties" : False
        },
        "MongoDbSettings" : {
          "description" : "MongoDbSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/MongoDbSslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            },
            "AuthType" : {
              "$ref" : "#/definitions/MongoDbAuthType"
            },
            "AuthSource" : {
              "type" : "string"
            },
            "AuthMechanism" : {
              "$ref" : "#/definitions/MongoDbAuthMechanism"
            }
          },
          "required" : [ "ServerName", "Port" ],
          "additionalProperties" : False
        },
        "IbmDb2LuwSettings" : {
          "description" : "IbmDb2LuwSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/Db2SslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode", "DatabaseName" ],
          "additionalProperties" : False
        },
        "IbmDb2zOsSettings" : {
          "description" : "IbmDb2zOsSettings property identifier.",
          "type" : "object",
          "properties" : {
            "ServerName" : {
              "type" : "string"
            },
            "Port" : {
              "type" : "integer"
            },
            "DatabaseName" : {
              "type" : "string"
            },
            "SslMode" : {
              "$ref" : "#/definitions/Db2SslModeValue"
            },
            "CertificateArn" : {
              "type" : "string"
            }
          },
          "required" : [ "ServerName", "Port", "SslMode", "DatabaseName" ],
          "additionalProperties" : False
        }
      },
      "anyOf" : [ {
        "required" : [ "PostgreSqlSettings" ]
      }, {
        "required" : [ "MySqlSettings" ]
      }, {
        "required" : [ "OracleSettings" ]
      }, {
        "required" : [ "MicrosoftSqlServerSettings" ]
      }, {
        "required" : [ "RedshiftSettings" ]
      }, {
        "required" : [ "DocDbSettings" ]
      }, {
        "required" : [ "MariaDbSettings" ]
      }, {
        "required" : [ "MongoDbSettings" ]
      }, {
        "required" : [ "IbmDb2LuwSettings" ]
      }, {
        "required" : [ "IbmDb2zOsSettings" ]
      } ],
      "additionalProperties" : False
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this resource.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "additionalProperties" : False,
  "required" : [ "Engine" ],
  "primaryIdentifier" : [ "/properties/DataProviderArn" ],
  "additionalIdentifiers" : [ [ "/properties/DataProviderName" ] ],
  "readOnlyProperties" : [ "/properties/DataProviderArn", "/properties/DataProviderCreationTime" ],
  "writeOnlyProperties" : [ "/properties/DataProviderIdentifier", "/properties/ExactSettings" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "dms:CreateDataProvider", "dms:ListDataProviders", "dms:DescribeDataProviders", "dms:AddTagsToResource", "dms:ListTagsForResource", "iam:GetRole", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "dms:ListDataProviders", "dms:DescribeDataProviders", "dms:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "dms:UpdateDataProvider", "dms:ModifyDataProvider", "dms:AddTagsToResource", "dms:RemoveTagsFromResource", "dms:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "dms:DeleteDataProvider" ]
    },
    "list" : {
      "permissions" : [ "dms:ListDataProviders", "dms:DescribeDataProviders", "dms:ListTagsForResource" ]
    }
  }
}