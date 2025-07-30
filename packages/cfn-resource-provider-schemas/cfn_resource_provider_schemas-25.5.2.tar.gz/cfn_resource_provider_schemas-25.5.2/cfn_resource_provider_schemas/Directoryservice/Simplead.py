SCHEMA = {
  "typeName" : "AWS::DirectoryService::SimpleAD",
  "description" : "Resource Type definition for AWS::DirectoryService::SimpleAD",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Alias" : {
      "type" : "string"
    },
    "DnsIpAddresses" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "CreateAlias" : {
      "type" : "boolean"
    },
    "Description" : {
      "type" : "string"
    },
    "EnableSso" : {
      "type" : "boolean"
    },
    "Name" : {
      "type" : "string"
    },
    "Password" : {
      "type" : "string"
    },
    "ShortName" : {
      "type" : "string"
    },
    "Size" : {
      "type" : "string"
    },
    "VpcSettings" : {
      "$ref" : "#/definitions/VpcSettings"
    }
  },
  "definitions" : {
    "VpcSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "VpcId" : {
          "type" : "string"
        }
      },
      "required" : [ "VpcId", "SubnetIds" ]
    }
  },
  "required" : [ "VpcSettings", "Size", "Name", "Password" ],
  "readOnlyProperties" : [ "/properties/Alias", "/properties/DnsIpAddresses", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/Size", "/properties/VpcSettings", "/properties/Name", "/properties/Password", "/properties/ShortName", "/properties/Description", "/properties/CreateAlias" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}