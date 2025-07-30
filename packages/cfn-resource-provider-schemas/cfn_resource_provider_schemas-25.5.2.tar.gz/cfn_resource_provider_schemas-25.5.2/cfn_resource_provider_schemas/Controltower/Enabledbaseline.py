SCHEMA = {
  "typeName" : "AWS::ControlTower::EnabledBaseline",
  "description" : "Definition of AWS::ControlTower::EnabledBaseline Resource Type",
  "definitions" : {
    "Parameter" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 1
        },
        "Value" : {
          "$ref" : "#/definitions/AnyType"
        }
      },
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 1
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "additionalProperties" : False
    },
    "AnyType" : {
      "anyOf" : [ {
        "type" : "string"
      }, {
        "type" : "object"
      }, {
        "type" : "number"
      }, {
        "type" : "array",
        "items" : {
          "anyOf" : [ {
            "type" : "boolean"
          }, {
            "type" : "number"
          }, {
            "type" : "object"
          }, {
            "type" : "string"
          } ]
        },
        "insertionOrder" : False
      }, {
        "type" : "boolean"
      } ]
    }
  },
  "properties" : {
    "BaselineIdentifier" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:aws[0-9a-zA-Z_\\-:\\/]+$"
    },
    "BaselineVersion" : {
      "type" : "string",
      "pattern" : "^\\d+(?:\\.\\d+){0,2}$"
    },
    "EnabledBaselineIdentifier" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:aws[0-9a-zA-Z_\\-:\\/]+$"
    },
    "TargetIdentifier" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:aws[0-9a-zA-Z_\\-:\\/]+$"
    },
    "Parameters" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Parameter"
      },
      "insertionOrder" : False
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "insertionOrder" : False
    }
  },
  "required" : [ "BaselineIdentifier", "TargetIdentifier", "BaselineVersion" ],
  "readOnlyProperties" : [ "/properties/EnabledBaselineIdentifier" ],
  "createOnlyProperties" : [ "/properties/TargetIdentifier", "/properties/BaselineIdentifier" ],
  "primaryIdentifier" : [ "/properties/EnabledBaselineIdentifier" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "controltower:TagResource", "controltower:UntagResource", "controltower:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "controltower:EnableBaseline", "controltower:TagResource", "controltower:UntagResource", "controltower:GetBaselineOperation", "controltower:GetEnabledBaseline", "controltower:ListTagsForResource", "organizations:CreateOrganizationalUnit", "organizations:CreateOrganization", "organizations:UpdatePolicy", "organizations:CreatePolicy", "organizations:AttachPolicy", "organizations:DetachPolicy", "organizations:DeletePolicy", "organizations:EnablePolicyType", "organizations:EnableAWSServiceAccess", "organizations:ListRoots", "servicecatalog:AssociatePrincipalWithPortfolio", "servicecatalog:AssociateProductWithPortfolio", "servicecatalog:CreatePortfolio", "servicecatalog:CreateProduct", "servicecatalog:CreateProvisioningArtifact", "servicecatalog:ListPortfolios", "servicecatalog:ListProvisioningArtifacts", "servicecatalog:SearchProductsAsAdmin", "servicecatalog:UpdatePortfolio", "servicecatalog:UpdateProvisioningArtifact", "servicecatalog:ListPrincipalsForPortfolio", "servicecatalog:DeleteProvisioningArtifact" ]
    },
    "read" : {
      "permissions" : [ "controltower:GetEnabledBaseline", "controltower:ListEnabledBaselines", "controltower:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "controltower:UpdateEnabledBaseline", "controltower:GetBaselineOperation", "organizations:CreateOrganizationalUnit", "organizations:CreateOrganization", "organizations:UpdatePolicy", "organizations:CreatePolicy", "organizations:AttachPolicy", "organizations:DetachPolicy", "organizations:DeletePolicy", "organizations:EnablePolicyType", "organizations:EnableAWSServiceAccess", "organizations:ListRoots", "servicecatalog:AssociatePrincipalWithPortfolio", "servicecatalog:AssociateProductWithPortfolio", "servicecatalog:CreatePortfolio", "servicecatalog:CreateProduct", "servicecatalog:CreateProvisioningArtifact", "servicecatalog:ListPortfolios", "servicecatalog:ListProvisioningArtifacts", "servicecatalog:SearchProductsAsAdmin", "servicecatalog:UpdatePortfolio", "servicecatalog:UpdateProvisioningArtifact", "servicecatalog:ListPrincipalsForPortfolio", "servicecatalog:DeleteProvisioningArtifact", "controltower:TagResource", "controltower:UntagResource", "controltower:GetEnabledBaseline" ]
    },
    "delete" : {
      "permissions" : [ "controltower:DisableBaseline", "controltower:GetBaselineOperation", "organizations:CreateOrganizationalUnit", "organizations:CreateOrganization", "organizations:UpdatePolicy", "organizations:CreatePolicy", "organizations:AttachPolicy", "organizations:DetachPolicy", "organizations:DeletePolicy", "organizations:EnablePolicyType", "organizations:EnableAWSServiceAccess", "organizations:ListRoots", "servicecatalog:AssociatePrincipalWithPortfolio", "servicecatalog:AssociateProductWithPortfolio", "servicecatalog:CreatePortfolio", "servicecatalog:CreateProduct", "servicecatalog:CreateProvisioningArtifact", "servicecatalog:ListPortfolios", "servicecatalog:ListProvisioningArtifacts", "servicecatalog:SearchProductsAsAdmin", "servicecatalog:UpdatePortfolio", "servicecatalog:UpdateProvisioningArtifact", "servicecatalog:ListPrincipalsForPortfolio", "servicecatalog:DeleteProvisioningArtifact" ]
    },
    "list" : {
      "permissions" : [ "controltower:ListEnabledBaselines" ]
    }
  },
  "additionalProperties" : False
}