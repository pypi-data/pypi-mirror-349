SCHEMA = {
  "typeName" : "AWS::LakeFormation::TagAssociation",
  "description" : "A resource schema representing a Lake Formation Tag Association. While tag associations are not explicit Lake Formation resources, this CloudFormation resource can be used to associate tags with Lake Formation entities.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "CatalogIdString" : {
      "type" : "string",
      "minLength" : 12,
      "maxLength" : 12
    },
    "NameString" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "LFTagPair" : {
      "type" : "object",
      "properties" : {
        "CatalogId" : {
          "$ref" : "#/definitions/CatalogIdString"
        },
        "TagKey" : {
          "$ref" : "#/definitions/LFTagKey"
        },
        "TagValues" : {
          "$ref" : "#/definitions/TagValueList"
        }
      },
      "required" : [ "CatalogId", "TagKey", "TagValues" ],
      "additionalProperties" : False
    },
    "LFTagsList" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/LFTagPair"
      },
      "insertionOrder" : False
    },
    "DataLakePrincipalString" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 255
    },
    "DataLakePrincipal" : {
      "type" : "object",
      "properties" : {
        "DataLakePrincipalIdentifier" : {
          "$ref" : "#/definitions/DataLakePrincipalString"
        }
      },
      "additionalProperties" : False
    },
    "ResourceType" : {
      "type" : "string",
      "enum" : [ "DATABASE", "TABLE" ]
    },
    "CatalogResource" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "DatabaseResource" : {
      "type" : "object",
      "properties" : {
        "CatalogId" : {
          "$ref" : "#/definitions/CatalogIdString"
        },
        "Name" : {
          "$ref" : "#/definitions/NameString"
        }
      },
      "required" : [ "CatalogId", "Name" ],
      "additionalProperties" : False
    },
    "TableWildcard" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "TableResource" : {
      "type" : "object",
      "properties" : {
        "CatalogId" : {
          "$ref" : "#/definitions/CatalogIdString"
        },
        "DatabaseName" : {
          "$ref" : "#/definitions/NameString"
        },
        "Name" : {
          "$ref" : "#/definitions/NameString"
        },
        "TableWildcard" : {
          "$ref" : "#/definitions/TableWildcard"
        }
      },
      "required" : [ "CatalogId", "DatabaseName" ],
      "additionalProperties" : False
    },
    "ColumnNames" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/NameString"
      },
      "insertionOrder" : False
    },
    "TableWithColumnsResource" : {
      "type" : "object",
      "properties" : {
        "CatalogId" : {
          "$ref" : "#/definitions/CatalogIdString"
        },
        "DatabaseName" : {
          "$ref" : "#/definitions/NameString"
        },
        "Name" : {
          "$ref" : "#/definitions/NameString"
        },
        "ColumnNames" : {
          "$ref" : "#/definitions/ColumnNames"
        }
      },
      "required" : [ "CatalogId", "DatabaseName", "Name", "ColumnNames" ],
      "additionalProperties" : False
    },
    "Resource" : {
      "type" : "object",
      "properties" : {
        "Catalog" : {
          "$ref" : "#/definitions/CatalogResource"
        },
        "Database" : {
          "$ref" : "#/definitions/DatabaseResource"
        },
        "Table" : {
          "$ref" : "#/definitions/TableResource"
        },
        "TableWithColumns" : {
          "$ref" : "#/definitions/TableWithColumnsResource"
        }
      },
      "additionalProperties" : False
    },
    "LFTagKey" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128
    },
    "LFTagValue" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 256
    },
    "TagValueList" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/LFTagValue"
      },
      "insertionOrder" : False,
      "minItems" : 1,
      "maxItems" : 50
    }
  },
  "properties" : {
    "Resource" : {
      "description" : "Resource to tag with the Lake Formation Tags",
      "$ref" : "#/definitions/Resource"
    },
    "LFTags" : {
      "description" : "List of Lake Formation Tags to associate with the Lake Formation Resource",
      "$ref" : "#/definitions/LFTagsList"
    },
    "ResourceIdentifier" : {
      "description" : "Unique string identifying the resource. Used as primary identifier, which ideally should be a string",
      "type" : "string"
    },
    "TagsIdentifier" : {
      "description" : "Unique string identifying the resource's tags. Used as primary identifier, which ideally should be a string",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "Resource", "LFTags" ],
  "createOnlyProperties" : [ "/properties/Resource", "/properties/LFTags" ],
  "readOnlyProperties" : [ "/properties/ResourceIdentifier", "/properties/TagsIdentifier" ],
  "replacementStrategy" : "delete_then_create",
  "tagging" : {
    "taggable" : False
  },
  "primaryIdentifier" : [ "/properties/ResourceIdentifier", "/properties/TagsIdentifier" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "lakeformation:AddLFTagsToResource", "glue:GetDatabase", "glue:GetTable" ]
    },
    "read" : {
      "permissions" : [ "lakeformation:GetResourceLFTags", "glue:GetDatabase", "glue:GetTable" ]
    },
    "delete" : {
      "permissions" : [ "lakeformation:RemoveLFTagsFromResource", "glue:GetDatabase", "glue:GetTable" ]
    }
  }
}