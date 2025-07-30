SCHEMA = {
  "typeName" : "AWS::EC2::DHCPOptions",
  "description" : "Resource Type definition for AWS::EC2::DHCPOptions",
  "additionalProperties" : False,
  "properties" : {
    "DhcpOptionsId" : {
      "type" : "string"
    },
    "DomainName" : {
      "type" : "string",
      "description" : "This value is used to complete unqualified DNS hostnames."
    },
    "DomainNameServers" : {
      "type" : "array",
      "description" : "The IPv4 addresses of up to four domain name servers, or AmazonProvidedDNS.",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "NetbiosNameServers" : {
      "type" : "array",
      "description" : "The IPv4 addresses of up to four NetBIOS name servers.",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "NetbiosNodeType" : {
      "type" : "integer",
      "description" : "The NetBIOS node type (1, 2, 4, or 8)."
    },
    "NtpServers" : {
      "type" : "array",
      "description" : "The IPv4 addresses of up to four Network Time Protocol (NTP) servers.",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Ipv6AddressPreferredLeaseTime" : {
      "type" : "integer",
      "description" : "The preferred Lease Time for ipV6 address in seconds."
    },
    "Tags" : {
      "type" : "array",
      "description" : "Any tags assigned to the DHCP options set.",
      "uniqueItems" : False,
      "insertionOrder" : False,
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
      "required" : [ "Value", "Key" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ]
  },
  "createOnlyProperties" : [ "/properties/NetbiosNameServers", "/properties/NetbiosNodeType", "/properties/NtpServers", "/properties/DomainName", "/properties/DomainNameServers", "/properties/Ipv6AddressPreferredLeaseTime" ],
  "readOnlyProperties" : [ "/properties/DhcpOptionsId" ],
  "primaryIdentifier" : [ "/properties/DhcpOptionsId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:CreateDhcpOptions", "ec2:DescribeDhcpOptions", "ec2:CreateTags" ]
    },
    "read" : {
      "permissions" : [ "ec2:DescribeDhcpOptions", "ec2:DescribeTags" ]
    },
    "update" : {
      "permissions" : [ "ec2:CreateTags", "ec2:DescribeDhcpOptions", "ec2:DeleteTags" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DeleteDhcpOptions", "ec2:DeleteTags", "ec2:DescribeDhcpOptions" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeDhcpOptions" ]
    }
  }
}