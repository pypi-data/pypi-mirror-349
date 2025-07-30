SCHEMA = {
  "typeName" : "AWS::AppIntegrations::Application",
  "description" : "Resource Type definition for AWS:AppIntegrations::Application",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "Tag" : {
      "description" : "A label for tagging Application resources",
      "type" : "object",
      "properties" : {
        "Key" : {
          "description" : "A key to identify the tag.",
          "type" : "string",
          "pattern" : "^(?!aws:)[a-zA-Z+-=._:/]+$",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "description" : "Corresponding tag value for the key.",
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "additionalProperties" : False,
      "required" : [ "Key", "Value" ]
    },
    "ExternalUrlConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "AccessUrl" ],
      "properties" : {
        "AccessUrl" : {
          "type" : "string",
          "pattern" : "^\\w+\\:\\/\\/.*$",
          "minLength" : 1,
          "maxLength" : 1000
        },
        "ApprovedOrigins" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ApprovedOrigins"
          },
          "minItems" : 0,
          "maxItems" : 50
        }
      }
    },
    "ApprovedOrigins" : {
      "type" : "string",
      "pattern" : "^\\w+\\:\\/\\/.*$",
      "minLength" : 1,
      "maxLength" : 1000
    },
    "Permissions" : {
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9\\/\\._\\-\\*]+$",
      "minLength" : 1,
      "maxLength" : 255
    }
  },
  "properties" : {
    "Name" : {
      "description" : "The name of the application.",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9\\/\\._ \\-]+$",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Id" : {
      "description" : "The id of the application.",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9/\\._\\-]+$",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Namespace" : {
      "description" : "The namespace of the application.",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9/\\._\\-]+$",
      "minLength" : 1,
      "maxLength" : 255
    },
    "Description" : {
      "description" : "The application description.",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1000
    },
    "ApplicationArn" : {
      "description" : "The Amazon Resource Name (ARN) of the application.",
      "pattern" : "^arn:aws[-a-z0-9]*:app-integrations:[-a-z0-9]*:[0-9]{12}:application/[-a-zA-Z0-9]*",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 2048
    },
    "ApplicationSourceConfig" : {
      "description" : "Application source config",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ExternalUrlConfig" : {
          "$ref" : "#/definitions/ExternalUrlConfig"
        }
      },
      "required" : [ "ExternalUrlConfig" ]
    },
    "Permissions" : {
      "description" : "The configuration of events or requests that the application has access to.",
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Permissions"
      },
      "minItems" : 0,
      "maxItems" : 150
    },
    "Tags" : {
      "description" : "The tags (keys and values) associated with the application.",
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "minItems" : 0,
      "maxItems" : 200
    }
  },
  "additionalProperties" : False,
  "required" : [ "Name", "Namespace", "Description", "ApplicationSourceConfig" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "app-integrations:TagResource", "app-integrations:UntagResource" ]
  },
  "readOnlyProperties" : [ "/properties/ApplicationArn", "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/ApplicationArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "app-integrations:CreateApplication", "app-integrations:TagResource" ]
    },
    "read" : {
      "permissions" : [ "app-integrations:GetApplication" ]
    },
    "list" : {
      "permissions" : [ "app-integrations:ListApplications", "app-integrations:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "app-integrations:GetApplication", "app-integrations:UpdateApplication", "app-integrations:TagResource", "app-integrations:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "app-integrations:DeleteApplication" ]
    }
  }
}