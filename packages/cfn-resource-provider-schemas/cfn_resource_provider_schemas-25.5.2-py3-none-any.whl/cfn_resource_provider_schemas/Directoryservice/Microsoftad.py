SCHEMA = {
  "typeName" : "AWS::DirectoryService::MicrosoftAD",
  "description" : "Resource Type definition for AWS::DirectoryService::MicrosoftAD",
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
    "Edition" : {
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
  "required" : [ "VpcSettings", "Name", "Password" ],
  "readOnlyProperties" : [ "/properties/Alias", "/properties/DnsIpAddresses", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/VpcSettings", "/properties/Edition", "/properties/Name", "/properties/Password", "/properties/ShortName", "/properties/CreateAlias" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}