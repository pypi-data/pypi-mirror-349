SCHEMA = {
  "typeName" : "AWS::VerifiedPermissions::Policy",
  "description" : "Definition of AWS::VerifiedPermissions::Policy Resource Type",
  "definitions" : {
    "EntityIdentifier" : {
      "type" : "object",
      "properties" : {
        "EntityType" : {
          "type" : "string",
          "maxLength" : 200,
          "minLength" : 1,
          "pattern" : "^.*$"
        },
        "EntityId" : {
          "type" : "string",
          "maxLength" : 200,
          "minLength" : 1,
          "pattern" : "^.*$"
        }
      },
      "required" : [ "EntityId", "EntityType" ],
      "additionalProperties" : False
    },
    "PolicyDefinition" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Static",
        "properties" : {
          "Static" : {
            "$ref" : "#/definitions/StaticPolicyDefinition"
          }
        },
        "required" : [ "Static" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "TemplateLinked",
        "properties" : {
          "TemplateLinked" : {
            "$ref" : "#/definitions/TemplateLinkedPolicyDefinition"
          }
        },
        "required" : [ "TemplateLinked" ],
        "additionalProperties" : False
      } ]
    },
    "PolicyType" : {
      "type" : "string",
      "enum" : [ "STATIC", "TEMPLATE_LINKED" ]
    },
    "StaticPolicyDefinition" : {
      "type" : "object",
      "properties" : {
        "Description" : {
          "type" : "string",
          "maxLength" : 150,
          "minLength" : 0
        },
        "Statement" : {
          "type" : "string",
          "maxLength" : 10000,
          "minLength" : 1
        }
      },
      "required" : [ "Statement" ],
      "additionalProperties" : False
    },
    "TemplateLinkedPolicyDefinition" : {
      "type" : "object",
      "properties" : {
        "PolicyTemplateId" : {
          "type" : "string",
          "maxLength" : 200,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9-]*$"
        },
        "Principal" : {
          "$ref" : "#/definitions/EntityIdentifier"
        },
        "Resource" : {
          "$ref" : "#/definitions/EntityIdentifier"
        }
      },
      "required" : [ "PolicyTemplateId" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Definition" : {
      "$ref" : "#/definitions/PolicyDefinition"
    },
    "PolicyId" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]*$"
    },
    "PolicyStoreId" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]*$"
    },
    "PolicyType" : {
      "$ref" : "#/definitions/PolicyType"
    }
  },
  "required" : [ "Definition", "PolicyStoreId" ],
  "readOnlyProperties" : [ "/properties/PolicyId", "/properties/PolicyType" ],
  "createOnlyProperties" : [ "/properties/PolicyStoreId" ],
  "primaryIdentifier" : [ "/properties/PolicyId", "/properties/PolicyStoreId" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-avp",
  "handlers" : {
    "create" : {
      "permissions" : [ "verifiedpermissions:CreatePolicy", "verifiedpermissions:GetPolicy" ]
    },
    "read" : {
      "permissions" : [ "verifiedpermissions:GetPolicy" ]
    },
    "update" : {
      "permissions" : [ "verifiedpermissions:UpdatePolicy", "verifiedpermissions:GetPolicy" ]
    },
    "delete" : {
      "permissions" : [ "verifiedpermissions:DeletePolicy", "verifiedpermissions:GetPolicy" ]
    },
    "list" : {
      "permissions" : [ "verifiedpermissions:ListPolicies", "verifiedpermissions:GetPolicy" ],
      "handlerSchema" : {
        "properties" : {
          "PolicyStoreId" : {
            "$ref" : "resource-schema.json#/properties/PolicyStoreId"
          }
        },
        "required" : [ "PolicyStoreId" ]
      }
    }
  },
  "additionalProperties" : False
}