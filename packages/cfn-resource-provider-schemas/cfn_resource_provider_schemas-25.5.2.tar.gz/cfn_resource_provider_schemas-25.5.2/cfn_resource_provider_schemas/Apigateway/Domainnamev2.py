SCHEMA = {
  "typeName" : "AWS::ApiGateway::DomainNameV2",
  "description" : "Resource Type definition for AWS::ApiGateway::DomainNameV2.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "EndpointConfiguration" : {
      "type" : "object",
      "properties" : {
        "Types" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "IpAddressType" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "CertificateArn" : {
      "type" : "string"
    },
    "DomainName" : {
      "type" : "string"
    },
    "EndpointConfiguration" : {
      "$ref" : "#/definitions/EndpointConfiguration"
    },
    "SecurityPolicy" : {
      "type" : "string"
    },
    "Policy" : {
      "type" : [ "object", "string" ]
    },
    "DomainNameId" : {
      "type" : "string"
    },
    "DomainNameArn" : {
      "type" : "string",
      "description" : "The amazon resource name (ARN) of the domain name resource."
    },
    "RoutingMode" : {
      "type" : "string",
      "description" : "The valid routing modes are [BASE_PATH_MAPPING_ONLY], [ROUTING_RULE_THEN_BASE_PATH_MAPPING] and [ROUTING_RULE_ONLY]. All other inputs are invalid.",
      "default" : "BASE_PATH_MAPPING_ONLY",
      "enum" : [ "BASE_PATH_MAPPING_ONLY", "ROUTING_RULE_THEN_BASE_PATH_MAPPING", "ROUTING_RULE_ONLY" ]
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "apigateway:PUT", "apigateway:PATCH", "apigateway:DELETE", "apigateway:GET", "apigateway:POST" ]
  },
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/DomainNameArn" ],
  "createOnlyProperties" : [ "/properties/DomainName", "/properties/SecurityPolicy", "/properties/EndpointConfiguration" ],
  "readOnlyProperties" : [ "/properties/DomainNameId", "/properties/DomainNameArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "apigateway:POST", "apigateway:GET", "apigateway:UpdateDomainNamePolicy" ]
    },
    "read" : {
      "permissions" : [ "apigateway:GET" ]
    },
    "update" : {
      "permissions" : [ "apigateway:GET", "apigateway:PUT", "apigateway:PATCH", "apigateway:UpdateDomainNamePolicy" ]
    },
    "delete" : {
      "permissions" : [ "apigateway:DELETE", "apigateway:GET", "apigateway:UpdateDomainNamePolicy" ]
    },
    "list" : {
      "permissions" : [ "apigateway:GET" ]
    }
  }
}