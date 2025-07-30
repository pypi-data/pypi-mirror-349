SCHEMA = {
  "typeName" : "AWS::RDS::DBSecurityGroup",
  "description" : "Resource Type definition for AWS::RDS::DBSecurityGroup",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DBSecurityGroupIngress" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Ingress"
      }
    },
    "EC2VpcId" : {
      "type" : "string"
    },
    "GroupDescription" : {
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
    "Ingress" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CIDRIP" : {
          "type" : "string"
        },
        "EC2SecurityGroupId" : {
          "type" : "string"
        },
        "EC2SecurityGroupName" : {
          "type" : "string"
        },
        "EC2SecurityGroupOwnerId" : {
          "type" : "string"
        }
      }
    },
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
  "required" : [ "GroupDescription", "DBSecurityGroupIngress" ],
  "createOnlyProperties" : [ "/properties/GroupDescription", "/properties/EC2VpcId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}