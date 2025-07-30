SCHEMA = {
  "typeName" : "AWS::Neptune::DBInstance",
  "description" : "Resource Type definition for AWS::Neptune::DBInstance",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Endpoint" : {
      "type" : "string"
    },
    "Port" : {
      "type" : "string"
    },
    "DBParameterGroupName" : {
      "type" : "string"
    },
    "DBInstanceClass" : {
      "type" : "string"
    },
    "AllowMajorVersionUpgrade" : {
      "type" : "boolean"
    },
    "DBClusterIdentifier" : {
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
    "DBSubnetGroupName" : {
      "type" : "string"
    },
    "DBInstanceIdentifier" : {
      "type" : "string"
    },
    "DBSnapshotIdentifier" : {
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
  "required" : [ "DBInstanceClass" ],
  "readOnlyProperties" : [ "/properties/Endpoint", "/properties/Port", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/DBClusterIdentifier", "/properties/AvailabilityZone", "/properties/DBInstanceIdentifier", "/properties/DBSubnetGroupName", "/properties/DBSnapshotIdentifier" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}