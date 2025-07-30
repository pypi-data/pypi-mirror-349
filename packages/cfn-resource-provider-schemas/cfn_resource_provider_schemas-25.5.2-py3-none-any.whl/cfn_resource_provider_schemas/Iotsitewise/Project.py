SCHEMA = {
  "typeName" : "AWS::IoTSiteWise::Project",
  "description" : "Resource schema for AWS::IoTSiteWise::Project",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-IoTSiteWise.git",
  "definitions" : {
    "AssetId" : {
      "description" : "The ID of the asset",
      "type" : "string"
    },
    "Tag" : {
      "description" : "To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted",
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
      "required" : [ "Key", "Value" ]
    }
  },
  "properties" : {
    "PortalId" : {
      "description" : "The ID of the portal in which to create the project.",
      "type" : "string"
    },
    "ProjectId" : {
      "description" : "The ID of the project.",
      "type" : "string"
    },
    "ProjectName" : {
      "description" : "A friendly name for the project.",
      "type" : "string"
    },
    "ProjectDescription" : {
      "description" : "A description for the project.",
      "type" : "string"
    },
    "ProjectArn" : {
      "description" : "The ARN of the project.",
      "type" : "string"
    },
    "AssetIds" : {
      "description" : "The IDs of the assets to be associated to the project.",
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/AssetId"
      }
    },
    "Tags" : {
      "description" : "A list of key-value pairs that contain metadata for the project.",
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "iotsitewise:TagResource", "iotsitewise:UntagResource", "iotsitewise:ListTagsForResource" ]
  },
  "required" : [ "PortalId", "ProjectName" ],
  "readOnlyProperties" : [ "/properties/ProjectId", "/properties/ProjectArn" ],
  "createOnlyProperties" : [ "/properties/PortalId" ],
  "primaryIdentifier" : [ "/properties/ProjectId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotsitewise:CreateProject", "iotsitewise:DescribeProject", "iotsitewise:ListProjectAssets", "iotsitewise:ListTagsForResource", "iotsitewise:TagResource", "iotsitewise:BatchAssociateProjectAssets" ]
    },
    "read" : {
      "permissions" : [ "iotsitewise:DescribeProject", "iotsitewise:ListTagsForResource", "iotsitewise:ListProjectAssets" ]
    },
    "update" : {
      "permissions" : [ "iotsitewise:DescribeProject", "iotsitewise:UpdateProject", "iotsitewise:BatchAssociateProjectAssets", "iotsitewise:BatchDisAssociateProjectAssets", "iotsitewise:ListProjectAssets", "iotsitewise:TagResource", "iotsitewise:UntagResource", "iotsitewise:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "iotsitewise:DescribeProject", "iotsitewise:DeleteProject" ]
    },
    "list" : {
      "permissions" : [ "iotsitewise:ListPortals", "iotsitewise:ListProjects", "iotsitewise:ListTagsForResource" ]
    }
  }
}