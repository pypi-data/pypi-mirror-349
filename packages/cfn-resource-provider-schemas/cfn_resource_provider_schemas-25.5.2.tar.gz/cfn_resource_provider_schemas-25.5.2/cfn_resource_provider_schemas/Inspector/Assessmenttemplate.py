SCHEMA = {
  "typeName" : "AWS::Inspector::AssessmentTemplate",
  "description" : "Resource Type definition for AWS::Inspector::AssessmentTemplate",
  "additionalProperties" : False,
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "AssessmentTargetArn" : {
      "type" : "string"
    },
    "DurationInSeconds" : {
      "type" : "integer"
    },
    "AssessmentTemplateName" : {
      "type" : "string"
    },
    "RulesPackageArns" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "UserAttributesForFindings" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
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
  "required" : [ "AssessmentTargetArn", "DurationInSeconds", "RulesPackageArns" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/DurationInSeconds", "/properties/AssessmentTemplateName", "/properties/UserAttributesForFindings", "/properties/AssessmentTargetArn", "/properties/RulesPackageArns" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "taggable" : False,
  "handlers" : {
    "create" : {
      "permissions" : [ "inspector:CreateAssessmentTemplate", "inspector:ListAssessmentTemplates", "inspector:DescribeAssessmentTemplates" ]
    },
    "read" : {
      "permissions" : [ "inspector:DescribeAssessmentTemplates" ]
    },
    "delete" : {
      "permissions" : [ "inspector:DeleteAssessmentTemplate" ]
    },
    "list" : {
      "permissions" : [ "inspector:ListAssessmentTemplates" ]
    }
  }
}