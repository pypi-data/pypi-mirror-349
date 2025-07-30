SCHEMA = {
  "typeName" : "AWS::DataBrew::Job",
  "description" : "Resource schema for AWS::DataBrew::Job.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-databrew.git",
  "properties" : {
    "DatasetName" : {
      "description" : "Dataset name",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "EncryptionKeyArn" : {
      "description" : "Encryption Key Arn",
      "type" : "string",
      "minLength" : 20,
      "maxLength" : 2048
    },
    "EncryptionMode" : {
      "description" : "Encryption mode",
      "enum" : [ "SSE-KMS", "SSE-S3" ],
      "type" : "string"
    },
    "Name" : {
      "description" : "Job name",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Type" : {
      "description" : "Job type",
      "enum" : [ "PROFILE", "RECIPE" ],
      "type" : "string"
    },
    "LogSubscription" : {
      "description" : "Log subscription",
      "enum" : [ "ENABLE", "DISABLE" ],
      "type" : "string"
    },
    "MaxCapacity" : {
      "description" : "Max capacity",
      "type" : "integer"
    },
    "MaxRetries" : {
      "description" : "Max retries",
      "type" : "integer"
    },
    "Outputs" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/Output"
      }
    },
    "DataCatalogOutputs" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/DataCatalogOutput"
      }
    },
    "DatabaseOutputs" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/DatabaseOutput"
      }
    },
    "OutputLocation" : {
      "description" : "Output location",
      "$ref" : "#/definitions/OutputLocation"
    },
    "ProjectName" : {
      "description" : "Project name",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Recipe" : {
      "$ref" : "#/definitions/Recipe"
    },
    "RoleArn" : {
      "description" : "Role arn",
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Timeout" : {
      "description" : "Timeout",
      "type" : "integer"
    },
    "JobSample" : {
      "description" : "Job Sample",
      "$ref" : "#/definitions/JobSample"
    },
    "ProfileConfiguration" : {
      "description" : "Profile Job configuration",
      "$ref" : "#/definitions/ProfileConfiguration"
    },
    "ValidationConfigurations" : {
      "description" : "Data quality rules configuration",
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/ValidationConfiguration"
      }
    }
  },
  "definitions" : {
    "S3Location" : {
      "description" : "S3 Output location",
      "type" : "object",
      "properties" : {
        "Bucket" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        },
        "BucketOwner" : {
          "type" : "string",
          "minLength" : 12,
          "maxLength" : 12
        }
      },
      "additionalProperties" : False,
      "required" : [ "Bucket" ]
    },
    "CsvOutputOptions" : {
      "description" : "Output Csv options",
      "type" : "object",
      "properties" : {
        "Delimiter" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1
        }
      },
      "additionalProperties" : False
    },
    "OutputFormatOptions" : {
      "description" : "Format options for job Output",
      "type" : "object",
      "properties" : {
        "Csv" : {
          "$ref" : "#/definitions/CsvOutputOptions"
        }
      },
      "additionalProperties" : False
    },
    "OutputLocation" : {
      "description" : "Output location",
      "type" : "object",
      "properties" : {
        "Bucket" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        },
        "BucketOwner" : {
          "type" : "string",
          "minLength" : 12,
          "maxLength" : 12
        }
      },
      "additionalProperties" : False,
      "required" : [ "Bucket" ]
    },
    "Output" : {
      "type" : "object",
      "properties" : {
        "CompressionFormat" : {
          "enum" : [ "GZIP", "LZ4", "SNAPPY", "BZIP2", "DEFLATE", "LZO", "BROTLI", "ZSTD", "ZLIB" ],
          "type" : "string"
        },
        "Format" : {
          "enum" : [ "CSV", "JSON", "PARQUET", "GLUEPARQUET", "AVRO", "ORC", "XML", "TABLEAUHYPER" ],
          "type" : "string"
        },
        "FormatOptions" : {
          "$ref" : "#/definitions/OutputFormatOptions"
        },
        "PartitionColumns" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Location" : {
          "$ref" : "#/definitions/S3Location"
        },
        "Overwrite" : {
          "type" : "boolean"
        },
        "MaxOutputFiles" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 999
        }
      },
      "additionalProperties" : False,
      "required" : [ "Location" ]
    },
    "DataCatalogOutput" : {
      "type" : "object",
      "properties" : {
        "CatalogId" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        },
        "DatabaseName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        },
        "TableName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        },
        "S3Options" : {
          "$ref" : "#/definitions/S3TableOutputOptions"
        },
        "DatabaseOptions" : {
          "$ref" : "#/definitions/DatabaseTableOutputOptions"
        },
        "Overwrite" : {
          "type" : "boolean"
        }
      },
      "additionalProperties" : False,
      "required" : [ "DatabaseName", "TableName" ]
    },
    "S3TableOutputOptions" : {
      "type" : "object",
      "properties" : {
        "Location" : {
          "$ref" : "#/definitions/S3Location"
        }
      },
      "additionalProperties" : False,
      "required" : [ "Location" ]
    },
    "DatabaseTableOutputOptions" : {
      "type" : "object",
      "properties" : {
        "TempDirectory" : {
          "$ref" : "#/definitions/S3Location"
        },
        "TableName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        }
      },
      "additionalProperties" : False,
      "required" : [ "TableName" ]
    },
    "DatabaseOutput" : {
      "type" : "object",
      "properties" : {
        "GlueConnectionName" : {
          "description" : "Glue connection name",
          "type" : "string"
        },
        "DatabaseOutputMode" : {
          "description" : "Database table name",
          "enum" : [ "NEW_TABLE" ],
          "type" : "string"
        },
        "DatabaseOptions" : {
          "$ref" : "#/definitions/DatabaseTableOutputOptions"
        }
      },
      "additionalProperties" : False,
      "required" : [ "GlueConnectionName", "DatabaseOptions" ]
    },
    "Recipe" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "description" : "Recipe name",
          "type" : "string"
        },
        "Version" : {
          "description" : "Recipe version",
          "type" : "string"
        }
      },
      "additionalProperties" : False,
      "required" : [ "Name" ]
    },
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "additionalProperties" : False,
      "required" : [ "Value", "Key" ]
    },
    "SampleMode" : {
      "description" : "Sample configuration mode for profile jobs.",
      "enum" : [ "FULL_DATASET", "CUSTOM_ROWS" ],
      "type" : "string"
    },
    "JobSize" : {
      "description" : "Sample configuration size for profile jobs.",
      "format" : "int64",
      "type" : "integer"
    },
    "JobSample" : {
      "description" : "Job Sample",
      "type" : "object",
      "properties" : {
        "Mode" : {
          "$ref" : "#/definitions/SampleMode"
        },
        "Size" : {
          "$ref" : "#/definitions/JobSize"
        }
      },
      "additionalProperties" : False
    },
    "ProfileConfiguration" : {
      "type" : "object",
      "properties" : {
        "DatasetStatisticsConfiguration" : {
          "$ref" : "#/definitions/StatisticsConfiguration"
        },
        "ProfileColumns" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/ColumnSelector"
          },
          "minItems" : 1
        },
        "ColumnStatisticsConfigurations" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/ColumnStatisticsConfiguration"
          },
          "minItems" : 1
        },
        "EntityDetectorConfiguration" : {
          "$ref" : "#/definitions/EntityDetectorConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "EntityDetectorConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "EntityTypes" ],
      "properties" : {
        "EntityTypes" : {
          "type" : "array",
          "insertionOrder" : True,
          "minItems" : 1,
          "items" : {
            "type" : "string",
            "minLength" : 1,
            "maxLength" : 128,
            "pattern" : "^[A-Z_][A-Z\\\\d_]*$"
          }
        },
        "AllowedStatistics" : {
          "$ref" : "#/definitions/AllowedStatistics"
        }
      }
    },
    "AllowedStatistics" : {
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "Statistics" ],
      "properties" : {
        "Statistics" : {
          "type" : "array",
          "insertionOrder" : True,
          "minItems" : 1,
          "items" : {
            "$ref" : "#/definitions/Statistic"
          }
        }
      }
    },
    "ColumnStatisticsConfiguration" : {
      "type" : "object",
      "properties" : {
        "Selectors" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/ColumnSelector"
          },
          "minItems" : 1
        },
        "Statistics" : {
          "$ref" : "#/definitions/StatisticsConfiguration"
        }
      },
      "required" : [ "Statistics" ],
      "additionalProperties" : False
    },
    "StatisticsConfiguration" : {
      "type" : "object",
      "properties" : {
        "IncludedStatistics" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/Statistic"
          },
          "minItems" : 1
        },
        "Overrides" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/StatisticOverride"
          },
          "minItems" : 1
        }
      },
      "additionalProperties" : False
    },
    "ColumnSelector" : {
      "type" : "object",
      "properties" : {
        "Regex" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        },
        "Name" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255
        }
      },
      "additionalProperties" : False
    },
    "Statistic" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128,
      "pattern" : "^[A-Z\\_]+$"
    },
    "StatisticOverride" : {
      "type" : "object",
      "properties" : {
        "Statistic" : {
          "$ref" : "#/definitions/Statistic"
        },
        "Parameters" : {
          "$ref" : "#/definitions/ParameterMap"
        }
      },
      "required" : [ "Statistic", "Parameters" ],
      "additionalProperties" : False
    },
    "ParameterMap" : {
      "type" : "object",
      "additionalProperties" : False,
      "patternProperties" : {
        "^[A-Za-z0-9]{1,128}$" : {
          "type" : "string"
        }
      }
    },
    "ValidationMode" : {
      "type" : "string",
      "enum" : [ "CHECK_ALL" ]
    },
    "ValidationConfiguration" : {
      "description" : "Configuration to attach Rulesets to the job",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RulesetArn" : {
          "description" : "Arn of the Ruleset",
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        },
        "ValidationMode" : {
          "$ref" : "#/definitions/ValidationMode"
        }
      },
      "required" : [ "RulesetArn" ]
    }
  },
  "additionalProperties" : False,
  "required" : [ "Name", "RoleArn", "Type" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/Type" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "databrew:TagResource", "databrew:UntagResource", "databrew:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "databrew:CreateProfileJob", "databrew:CreateRecipeJob", "databrew:DescribeJob", "databrew:TagResource", "databrew:UntagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "databrew:DescribeJob", "iam:ListRoles" ]
    },
    "update" : {
      "permissions" : [ "databrew:UpdateProfileJob", "databrew:UpdateRecipeJob", "databrew:TagResource", "databrew:UntagResource", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "databrew:DeleteJob" ]
    },
    "list" : {
      "permissions" : [ "databrew:ListJobs", "databrew:ListTagsForResource", "iam:ListRoles" ]
    }
  }
}