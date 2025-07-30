SCHEMA = {
  "typeName" : "AWS::FSx::StorageVirtualMachine",
  "description" : "Resource Type definition for AWS::FSx::StorageVirtualMachine",
  "additionalProperties" : False,
  "properties" : {
    "ResourceARN" : {
      "type" : "string"
    },
    "SvmAdminPassword" : {
      "type" : "string"
    },
    "StorageVirtualMachineId" : {
      "type" : "string"
    },
    "ActiveDirectoryConfiguration" : {
      "$ref" : "#/definitions/ActiveDirectoryConfiguration"
    },
    "RootVolumeSecurityStyle" : {
      "type" : "string"
    },
    "FileSystemId" : {
      "type" : "string"
    },
    "UUID" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Name" : {
      "type" : "string"
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
    "ActiveDirectoryConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SelfManagedActiveDirectoryConfiguration" : {
          "$ref" : "#/definitions/SelfManagedActiveDirectoryConfiguration"
        },
        "NetBiosName" : {
          "type" : "string"
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
    }
  },
  "required" : [ "FileSystemId", "Name" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/RootVolumeSecurityStyle", "/properties/FileSystemId" ],
  "primaryIdentifier" : [ "/properties/StorageVirtualMachineId" ],
  "readOnlyProperties" : [ "/properties/ResourceARN", "/properties/UUID", "/properties/StorageVirtualMachineId" ]
}