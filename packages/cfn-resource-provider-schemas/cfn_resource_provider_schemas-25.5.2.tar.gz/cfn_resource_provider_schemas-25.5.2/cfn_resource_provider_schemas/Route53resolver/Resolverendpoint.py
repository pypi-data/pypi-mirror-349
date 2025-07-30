SCHEMA = {
  "typeName" : "AWS::Route53Resolver::ResolverEndpoint",
  "description" : "Resource Type definition for AWS::Route53Resolver::ResolverEndpoint",
  "additionalProperties" : False,
  "properties" : {
    "ResolverEndpointId" : {
      "type" : "string"
    },
    "Protocols" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "OutpostArn" : {
      "type" : "string"
    },
    "ResolverEndpointType" : {
      "type" : "string"
    },
    "Direction" : {
      "type" : "string"
    },
    "SecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Name" : {
      "type" : "string"
    },
    "IpAddresses" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/IpAddressRequest"
      }
    },
    "IpAddressCount" : {
      "type" : "string"
    },
    "PreferredInstanceType" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "HostVPCId" : {
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
    "IpAddressRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubnetId" : {
          "type" : "string"
        },
        "Ipv6" : {
          "type" : "string"
        },
        "Ip" : {
          "type" : "string"
        }
      },
      "required" : [ "SubnetId" ]
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
  "required" : [ "IpAddresses", "Direction", "SecurityGroupIds" ],
  "createOnlyProperties" : [ "/properties/OutpostArn", "/properties/Direction", "/properties/SecurityGroupIds", "/properties/PreferredInstanceType" ],
  "primaryIdentifier" : [ "/properties/ResolverEndpointId" ],
  "readOnlyProperties" : [ "/properties/ResolverEndpointId", "/properties/IpAddressCount", "/properties/Arn", "/properties/HostVPCId" ]
}