SCHEMA = {
  "typeName" : "AWS::ElastiCache::ParameterGroup",
  "description" : "Resource Type definition for AWS::ElastiCache::ParameterGroup",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string",
      "description" : "The description for this cache parameter group."
    },
    "Properties" : {
      "type" : "object",
      "additionalProperties" : False,
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : "string"
        }
      },
      "description" : "A comma-delimited list of parameter name/value pairs. For more information see ModifyCacheParameterGroup in the Amazon ElastiCache API Reference Guide."
    },
    "Tags" : {
      "type" : "array",
      "description" : "Tags are composed of a Key/Value pair. You can use tags to categorize and track each parameter group. The tag value None is permitted.",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "insertionOrder" : False,
      "uniqueItems" : False
    },
    "CacheParameterGroupName" : {
      "type" : "string",
      "description" : "The name of the Cache Parameter Group."
    },
    "CacheParameterGroupFamily" : {
      "type" : "string",
      "description" : "The name of the cache parameter group family that this cache parameter group is compatible with."
    }
  },
  "definitions" : {
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
  "required" : [ "Description", "CacheParameterGroupFamily" ],
  "readOnlyProperties" : [ "/properties/CacheParameterGroupName" ],
  "createOnlyProperties" : [ "/properties/CacheParameterGroupFamily" ],
  "primaryIdentifier" : [ "/properties/CacheParameterGroupName" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ElastiCache:CreateCacheParameterGroup", "ElastiCache:DescribeCacheParameterGroups", "ElastiCache:AddTagsToResource", "ElastiCache:ModifyCacheParameterGroup", "iam:CreateServiceLinkedRole", "iam:PutRolePolicy" ]
    },
    "read" : {
      "permissions" : [ "ElastiCache:DescribeCacheParameterGroups", "ElastiCache:DescribeCacheParameters", "ElastiCache:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "ElastiCache:ModifyCacheParameterGroup", "ElastiCache:DescribeCacheParameterGroups", "ElastiCache:DescribeCacheParameters", "ElastiCache:DescribeEngineDefaultParameters", "ElastiCache:AddTagsToResource", "ElastiCache:RemoveTagsFromResource" ]
    },
    "delete" : {
      "permissions" : [ "ElastiCache:DescribeCacheParameterGroups", "ElastiCache:DeleteCacheParameterGroup" ]
    },
    "list" : {
      "permissions" : [ "ElastiCache:DescribeCacheParameterGroups" ]
    }
  }
}