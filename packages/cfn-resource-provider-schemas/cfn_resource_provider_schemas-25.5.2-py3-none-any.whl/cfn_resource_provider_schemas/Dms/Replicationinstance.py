SCHEMA = {
  "typeName" : "AWS::DMS::ReplicationInstance",
  "description" : "Resource Type definition for AWS::DMS::ReplicationInstance",
  "additionalProperties" : False,
  "properties" : {
    "DnsNameServers" : {
      "type" : "string"
    },
    "ReplicationInstanceIdentifier" : {
      "type" : "string"
    },
    "EngineVersion" : {
      "type" : "string"
    },
    "KmsKeyId" : {
      "type" : "string"
    },
    "AvailabilityZone" : {
      "type" : "string"
    },
    "PreferredMaintenanceWindow" : {
      "type" : "string"
    },
    "AutoMinorVersionUpgrade" : {
      "type" : "boolean"
    },
    "ReplicationSubnetGroupIdentifier" : {
      "type" : "string"
    },
    "ReplicationInstancePrivateIpAddresses" : {
      "type" : "string"
    },
    "AllocatedStorage" : {
      "type" : "integer"
    },
    "ResourceIdentifier" : {
      "type" : "string"
    },
    "VpcSecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "NetworkType" : {
      "type" : "string"
    },
    "AllowMajorVersionUpgrade" : {
      "type" : "boolean"
    },
    "ReplicationInstanceClass" : {
      "type" : "string"
    },
    "PubliclyAccessible" : {
      "type" : "boolean"
    },
    "Id" : {
      "type" : "string"
    },
    "MultiAZ" : {
      "type" : "boolean"
    },
    "ReplicationInstancePublicIpAddresses" : {
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
  "required" : [ "ReplicationInstanceClass" ],
  "createOnlyProperties" : [ "/properties/KmsKeyId", "/properties/ResourceIdentifier", "/properties/DnsNameServers", "/properties/ReplicationSubnetGroupIdentifier", "/properties/PubliclyAccessible" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/ReplicationInstancePublicIpAddresses", "/properties/Id", "/properties/ReplicationInstancePrivateIpAddresses" ]
}