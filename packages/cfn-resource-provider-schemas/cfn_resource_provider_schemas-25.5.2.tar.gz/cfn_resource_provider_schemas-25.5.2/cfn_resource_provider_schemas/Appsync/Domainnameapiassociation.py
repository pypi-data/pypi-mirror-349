SCHEMA = {
  "typeName" : "AWS::AppSync::DomainNameApiAssociation",
  "description" : "Resource Type definition for AWS::AppSync::DomainNameApiAssociation",
  "additionalProperties" : False,
  "properties" : {
    "DomainName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 253,
      "pattern" : "^(\\*[a-z\\d-]*\\.)?([a-z\\d-]+\\.)+[a-z\\d-]+$"
    },
    "ApiId" : {
      "type" : "string"
    },
    "ApiAssociationIdentifier" : {
      "type" : "string"
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "required" : [ "DomainName", "ApiId" ],
  "primaryIdentifier" : [ "/properties/ApiAssociationIdentifier" ],
  "readOnlyProperties" : [ "/properties/ApiAssociationIdentifier" ],
  "createOnlyProperties" : [ "/properties/DomainName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "appsync:AssociateApi", "appsync:GetApiAssociation" ]
    },
    "delete" : {
      "permissions" : [ "appsync:DisassociateApi", "appsync:GetApiAssociation" ]
    },
    "update" : {
      "permissions" : [ "appsync:AssociateApi", "appsync:GetApiAssociation" ]
    },
    "read" : {
      "permissions" : [ "appsync:GetApiAssociation" ]
    }
  }
}