SCHEMA = {
  "typeName" : "AWS::FSx::FileSystem",
  "description" : "Resource Type definition for AWS::FSx::FileSystem",
  "additionalProperties" : False,
  "properties" : {
    "StorageType" : {
      "type" : "string"
    },
    "KmsKeyId" : {
      "type" : "string"
    },
    "StorageCapacity" : {
      "type" : "integer"
    },
    "RootVolumeId" : {
      "type" : "string"
    },
    "LustreConfiguration" : {
      "$ref" : "#/definitions/LustreConfiguration"
    },
    "BackupId" : {
      "type" : "string"
    },
    "OntapConfiguration" : {
      "$ref" : "#/definitions/OntapConfiguration"
    },
    "DNSName" : {
      "type" : "string"
    },
    "SubnetIds" : {
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
    "WindowsConfiguration" : {
      "$ref" : "#/definitions/WindowsConfiguration"
    },
    "FileSystemTypeVersion" : {
      "type" : "string"
    },
    "OpenZFSConfiguration" : {
      "$ref" : "#/definitions/OpenZFSConfiguration"
    },
    "ResourceARN" : {
      "type" : "string"
    },
    "FileSystemType" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "LustreMountName" : {
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
  "definitions" : {
    "SelfManagedActiveDirectoryConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FileSystemAdministratorsGroup" : {
          "type" : "string"
        },
        "UserName" : {
          "type" : "string"
        },
        "DomainName" : {
          "type" : "string"
        },
        "OrganizationalUnitDistinguishedName" : {
          "type" : "string"
        },
        "DnsIps" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Password" : {
          "type" : "string"
        }
      }
    },
    "AuditLogConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FileAccessAuditLogLevel" : {
          "type" : "string"
        },
        "FileShareAccessAuditLogLevel" : {
          "type" : "string"
        },
        "AuditLogDestination" : {
          "type" : "string"
        }
      },
      "required" : [ "FileAccessAuditLogLevel", "FileShareAccessAuditLogLevel" ]
    },
    "LustreConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DriveCacheType" : {
          "type" : "string"
        },
        "AutoImportPolicy" : {
          "type" : "string"
        },
        "EfaEnabled" : {
          "type" : "boolean"
        },
        "ImportedFileChunkSize" : {
          "type" : "integer"
        },
        "DeploymentType" : {
          "type" : "string"
        },
        "DataCompressionType" : {
          "type" : "string"
        },
        "ImportPath" : {
          "type" : "string"
        },
        "WeeklyMaintenanceStartTime" : {
          "type" : "string"
        },
        "MetadataConfiguration" : {
          "$ref" : "#/definitions/MetadataConfiguration"
        },
        "DailyAutomaticBackupStartTime" : {
          "type" : "string"
        },
        "CopyTagsToBackups" : {
          "type" : "boolean"
        },
        "ExportPath" : {
          "type" : "string"
        },
        "PerUnitStorageThroughput" : {
          "type" : "integer"
        },
        "AutomaticBackupRetentionDays" : {
          "type" : "integer"
        }
      }
    },
    "OntapConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HAPairs" : {
          "type" : "integer"
        },
        "FsxAdminPassword" : {
          "type" : "string"
        },
        "ThroughputCapacityPerHAPair" : {
          "type" : "integer"
        },
        "DeploymentType" : {
          "type" : "string"
        },
        "ThroughputCapacity" : {
          "type" : "integer"
        },
        "EndpointIpAddressRange" : {
          "type" : "string"
        },
        "RouteTableIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "WeeklyMaintenanceStartTime" : {
          "type" : "string"
        },
        "DiskIopsConfiguration" : {
          "$ref" : "#/definitions/DiskIopsConfiguration"
        },
        "DailyAutomaticBackupStartTime" : {
          "type" : "string"
        },
        "AutomaticBackupRetentionDays" : {
          "type" : "integer"
        },
        "PreferredSubnetId" : {
          "type" : "string"
        }
      },
      "required" : [ "DeploymentType" ]
    },
    "RootVolumeConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ReadOnly" : {
          "type" : "boolean"
        },
        "DataCompressionType" : {
          "type" : "string"
        },
        "NfsExports" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/NfsExports"
          }
        },
        "CopyTagsToSnapshots" : {
          "type" : "boolean"
        },
        "RecordSizeKiB" : {
          "type" : "integer"
        },
        "UserAndGroupQuotas" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/UserAndGroupQuotas"
          }
        }
      }
    },
    "WindowsConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SelfManagedActiveDirectoryConfiguration" : {
          "$ref" : "#/definitions/SelfManagedActiveDirectoryConfiguration"
        },
        "AuditLogConfiguration" : {
          "$ref" : "#/definitions/AuditLogConfiguration"
        },
        "ActiveDirectoryId" : {
          "type" : "string"
        },
        "DeploymentType" : {
          "type" : "string"
        },
        "Aliases" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "ThroughputCapacity" : {
          "type" : "integer"
        },
        "WeeklyMaintenanceStartTime" : {
          "type" : "string"
        },
        "DiskIopsConfiguration" : {
          "$ref" : "#/definitions/DiskIopsConfiguration"
        },
        "CopyTagsToBackups" : {
          "type" : "boolean"
        },
        "DailyAutomaticBackupStartTime" : {
          "type" : "string"
        },
        "AutomaticBackupRetentionDays" : {
          "type" : "integer"
        },
        "PreferredSubnetId" : {
          "type" : "string"
        }
      },
      "required" : [ "ThroughputCapacity" ]
    },
    "OpenZFSConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Options" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "CopyTagsToVolumes" : {
          "type" : "boolean"
        },
        "DeploymentType" : {
          "type" : "string"
        },
        "ThroughputCapacity" : {
          "type" : "integer"
        },
        "RootVolumeConfiguration" : {
          "$ref" : "#/definitions/RootVolumeConfiguration"
        },
        "EndpointIpAddressRange" : {
          "type" : "string"
        },
        "ReadCacheConfiguration" : {
          "$ref" : "#/definitions/ReadCacheConfiguration"
        },
        "RouteTableIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "WeeklyMaintenanceStartTime" : {
          "type" : "string"
        },
        "DiskIopsConfiguration" : {
          "$ref" : "#/definitions/DiskIopsConfiguration"
        },
        "DailyAutomaticBackupStartTime" : {
          "type" : "string"
        },
        "CopyTagsToBackups" : {
          "type" : "boolean"
        },
        "AutomaticBackupRetentionDays" : {
          "type" : "integer"
        },
        "PreferredSubnetId" : {
          "type" : "string"
        }
      },
      "required" : [ "DeploymentType" ]
    },
    "ReadCacheConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SizingMode" : {
          "type" : "string"
        },
        "SizeGiB" : {
          "type" : "integer"
        }
      }
    },
    "DiskIopsConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mode" : {
          "type" : "string"
        },
        "Iops" : {
          "type" : "integer"
        }
      }
    },
    "MetadataConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mode" : {
          "type" : "string"
        },
        "Iops" : {
          "type" : "integer"
        }
      }
    },
    "NfsExports" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientConfigurations" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ClientConfigurations"
          }
        }
      }
    },
    "ClientConfigurations" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Clients" : {
          "type" : "string"
        },
        "Options" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
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
    "UserAndGroupQuotas" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Id" : {
          "type" : "integer"
        },
        "StorageCapacityQuotaGiB" : {
          "type" : "integer"
        }
      }
    }
  },
  "required" : [ "FileSystemType", "SubnetIds" ],
  "createOnlyProperties" : [ "/properties/KmsKeyId", "/properties/SecurityGroupIds", "/properties/FileSystemType", "/properties/SubnetIds", "/properties/BackupId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/ResourceARN", "/properties/Id", "/properties/LustreMountName", "/properties/RootVolumeId", "/properties/DNSName" ]
}