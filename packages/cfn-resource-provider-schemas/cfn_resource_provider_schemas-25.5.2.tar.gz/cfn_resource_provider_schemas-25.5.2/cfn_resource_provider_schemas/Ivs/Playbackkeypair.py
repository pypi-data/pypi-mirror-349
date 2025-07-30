SCHEMA = {
  "typeName" : "AWS::IVS::PlaybackKeyPair",
  "description" : "Resource Type definition for AWS::IVS::PlaybackKeyPair",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "properties" : {
    "Name" : {
      "description" : "An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource. The value does not need to be unique.",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9-_]*$",
      "minLength" : 0,
      "maxLength" : 128
    },
    "PublicKeyMaterial" : {
      "description" : "The public portion of a customer-generated key pair. This field is required to create the AWS::IVS::PlaybackKeyPair resource.",
      "type" : "string"
    },
    "Fingerprint" : {
      "description" : "Key-pair identifier.",
      "type" : "string"
    },
    "Arn" : {
      "description" : "Key-pair identifier.",
      "type" : "string",
      "pattern" : "^arn:aws:ivs:[a-z0-9-]+:[0-9]+:playback-key/[a-zA-Z0-9-]+$",
      "minLength" : 1,
      "maxLength" : 128
    },
    "Tags" : {
      "description" : "A list of key-value pairs that contain metadata for the asset model.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "maxItems" : 50,
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
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ivs:TagResource", "ivs:UntagResource", "ivs:ListTagsForResource" ]
  },
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Fingerprint" ],
  "writeOnlyProperties" : [ "/properties/PublicKeyMaterial" ],
  "createOnlyProperties" : [ "/properties/PublicKeyMaterial", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ivs:ImportPlaybackKeyPair", "ivs:TagResource" ]
    },
    "read" : {
      "permissions" : [ "ivs:GetPlaybackKeyPair" ]
    },
    "update" : {
      "permissions" : [ "ivs:GetPlaybackKeyPair", "ivs:ListTagsForResource", "ivs:UntagResource", "ivs:TagResource" ]
    },
    "delete" : {
      "permissions" : [ "ivs:DeletePlaybackKeyPair", "ivs:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "ivs:ListPlaybackKeyPairs", "ivs:ListTagsForResource" ]
    }
  }
}