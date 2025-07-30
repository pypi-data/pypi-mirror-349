SCHEMA = {
  "typeName" : "AWS::Cloud9::EnvironmentEC2",
  "description" : "Resource Type definition for AWS::Cloud9::EnvironmentEC2",
  "additionalProperties" : False,
  "properties" : {
    "Repositories" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Repository"
      }
    },
    "OwnerArn" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "ConnectionType" : {
      "type" : "string"
    },
    "AutomaticStopTimeMinutes" : {
      "type" : "integer"
    },
    "ImageId" : {
      "type" : "string"
    },
    "SubnetId" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "InstanceType" : {
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
    "Repository" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RepositoryUrl" : {
          "type" : "string"
        },
        "PathComponent" : {
          "type" : "string"
        }
      },
      "required" : [ "PathComponent", "RepositoryUrl" ]
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
  "required" : [ "ImageId", "InstanceType" ],
  "createOnlyProperties" : [ "/properties/AutomaticStopTimeMinutes", "/properties/OwnerArn", "/properties/ConnectionType", "/properties/InstanceType", "/properties/ImageId", "/properties/SubnetId", "/properties/Repositories" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}