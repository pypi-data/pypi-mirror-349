SCHEMA = {
  "typeName" : "AWS::IoT::ProvisioningTemplate",
  "description" : "Creates a fleet provisioning template.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "ProvisioningHook" : {
      "type" : "object",
      "properties" : {
        "TargetArn" : {
          "type" : "string"
        },
        "PayloadVersion" : {
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
      "additionalProperties" : False,
      "required" : [ "Key", "Value" ]
    }
  },
  "properties" : {
    "TemplateArn" : {
      "type" : "string"
    },
    "TemplateName" : {
      "type" : "string",
      "pattern" : "^[0-9A-Za-z_-]+$",
      "minLength" : 1,
      "maxLength" : 36
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 500
    },
    "Enabled" : {
      "type" : "boolean"
    },
    "ProvisioningRoleArn" : {
      "type" : "string"
    },
    "TemplateBody" : {
      "type" : "string"
    },
    "TemplateType" : {
      "type" : "string",
      "enum" : [ "FLEET_PROVISIONING", "JITP" ]
    },
    "PreProvisioningHook" : {
      "$ref" : "#/definitions/ProvisioningHook"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
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
    "permissions" : [ "iot:ListTagsForResource", "iot:TagResource", "iot:UntagResource" ]
  },
  "additionalProperties" : False,
  "required" : [ "ProvisioningRoleArn", "TemplateBody" ],
  "createOnlyProperties" : [ "/properties/TemplateName", "/properties/TemplateType" ],
  "readOnlyProperties" : [ "/properties/TemplateArn" ],
  "primaryIdentifier" : [ "/properties/TemplateName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:GetRole", "iam:PassRole", "iot:CreateProvisioningTemplate", "iot:DescribeProvisioningTemplate", "iot:TagResource", "iot:ListTagsForResource" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeProvisioningTemplate", "iot:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iam:GetRole", "iam:PassRole", "iot:UpdateProvisioningTemplate", "iot:CreateProvisioningTemplateVersion", "iot:ListProvisioningTemplateVersions", "iot:DeleteProvisioningTemplateVersion", "iot:DescribeProvisioningTemplate", "iot:TagResource", "iot:UntagResource", "iot:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "iot:DeleteProvisioningTemplate", "iot:DescribeProvisioningTemplate" ]
    },
    "list" : {
      "permissions" : [ "iot:ListProvisioningTemplates" ]
    }
  }
}