SCHEMA = {
  "typeName" : "AWS::WorkSpacesWeb::TrustStore",
  "description" : "Definition of AWS::WorkSpacesWeb::TrustStore Resource Type",
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$"
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0,
          "pattern" : "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "AssociatedPortalArns" : {
      "type" : "array",
      "items" : {
        "type" : "string",
        "maxLength" : 2048,
        "minLength" : 20,
        "pattern" : "^arn:[\\w+=\\/,.@-]+:[a-zA-Z0-9\\-]+:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:[a-zA-Z]+(\\/[a-fA-F0-9\\-]{36})+$"
      },
      "insertionOrder" : False
    },
    "CertificateList" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      },
      "insertionOrder" : False
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "maxItems" : 200,
      "minItems" : 0,
      "insertionOrder" : False
    },
    "TrustStoreArn" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:[\\w+=\\/,.@-]+:[a-zA-Z0-9\\-]+:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:[a-zA-Z]+(\\/[a-fA-F0-9\\-]{36})+$"
    }
  },
  "required" : [ "CertificateList" ],
  "readOnlyProperties" : [ "/properties/AssociatedPortalArns", "/properties/TrustStoreArn" ],
  "primaryIdentifier" : [ "/properties/TrustStoreArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "workspaces-web:CreateTrustStore", "workspaces-web:GetTrustStore", "workspaces-web:GetTrustStoreCertificate", "workspaces-web:ListTrustStoreCertificates", "workspaces-web:ListTagsForResource", "workspaces-web:TagResource" ]
    },
    "read" : {
      "permissions" : [ "workspaces-web:GetTrustStore", "workspaces-web:GetTrustStoreCertificate", "workspaces-web:ListTagsForResource", "workspaces-web:ListTrustStoreCertificates" ]
    },
    "update" : {
      "permissions" : [ "workspaces-web:UpdateTrustStore", "workspaces-web:TagResource", "workspaces-web:UntagResource", "workspaces-web:GetTrustStore", "workspaces-web:GetTrustStoreCertificate", "workspaces-web:ListTagsForResource", "workspaces-web:ListTrustStoreCertificates" ]
    },
    "delete" : {
      "permissions" : [ "workspaces-web:GetTrustStore", "workspaces-web:GetTrustStoreCertificate", "workspaces-web:DeleteTrustStore" ]
    },
    "list" : {
      "permissions" : [ "workspaces-web:ListTrustStores", "workspaces-web:ListTrustStoreCertificates" ]
    }
  },
  "tagging" : {
    "cloudFormationSystemTags" : False,
    "tagOnCreate" : True,
    "tagProperty" : "/properties/Tags",
    "tagUpdatable" : True,
    "taggable" : True,
    "permissions" : [ "workspaces-web:UntagResource", "workspaces-web:ListTagsForResource", "workspaces-web:TagResource" ]
  },
  "additionalProperties" : False
}