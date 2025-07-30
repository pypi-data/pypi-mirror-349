SCHEMA = {
  "typeName" : "AWS::ManagedBlockchain::Member",
  "description" : "Resource Type definition for AWS::ManagedBlockchain::Member",
  "additionalProperties" : False,
  "properties" : {
    "MemberId" : {
      "type" : "string"
    },
    "NetworkConfiguration" : {
      "$ref" : "#/definitions/NetworkConfiguration"
    },
    "MemberConfiguration" : {
      "$ref" : "#/definitions/MemberConfiguration"
    },
    "NetworkId" : {
      "type" : "string"
    },
    "InvitationId" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "MemberConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Description" : {
          "type" : "string"
        },
        "MemberFrameworkConfiguration" : {
          "$ref" : "#/definitions/MemberFrameworkConfiguration"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ]
    },
    "NetworkFabricConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Edition" : {
          "type" : "string"
        }
      },
      "required" : [ "Edition" ]
    },
    "ApprovalThresholdPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ThresholdComparator" : {
          "type" : "string"
        },
        "ThresholdPercentage" : {
          "type" : "integer"
        },
        "ProposalDurationInHours" : {
          "type" : "integer"
        }
      }
    },
    "NetworkConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Description" : {
          "type" : "string"
        },
        "FrameworkVersion" : {
          "type" : "string"
        },
        "VotingPolicy" : {
          "$ref" : "#/definitions/VotingPolicy"
        },
        "Framework" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        },
        "NetworkFrameworkConfiguration" : {
          "$ref" : "#/definitions/NetworkFrameworkConfiguration"
        }
      },
      "required" : [ "FrameworkVersion", "VotingPolicy", "Framework", "Name" ]
    },
    "MemberFabricConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AdminUsername" : {
          "type" : "string"
        },
        "AdminPassword" : {
          "type" : "string"
        }
      },
      "required" : [ "AdminUsername", "AdminPassword" ]
    },
    "VotingPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ApprovalThresholdPolicy" : {
          "$ref" : "#/definitions/ApprovalThresholdPolicy"
        }
      }
    },
    "MemberFrameworkConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MemberFabricConfiguration" : {
          "$ref" : "#/definitions/MemberFabricConfiguration"
        }
      }
    },
    "NetworkFrameworkConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NetworkFabricConfiguration" : {
          "$ref" : "#/definitions/NetworkFabricConfiguration"
        }
      }
    }
  },
  "required" : [ "MemberConfiguration" ],
  "primaryIdentifier" : [ "/properties/MemberId" ],
  "readOnlyProperties" : [ "/properties/MemberId" ]
}