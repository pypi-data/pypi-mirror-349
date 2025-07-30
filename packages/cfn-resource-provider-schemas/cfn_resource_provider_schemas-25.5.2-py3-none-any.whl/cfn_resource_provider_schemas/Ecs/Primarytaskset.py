SCHEMA = {
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ecs.git",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "read" : {
      "permissions" : [ ]
    },
    "create" : {
      "permissions" : [ "ecs:DescribeTaskSets", "ecs:UpdateServicePrimaryTaskSet" ]
    },
    "update" : {
      "permissions" : [ "ecs:DescribeTaskSets", "ecs:UpdateServicePrimaryTaskSet" ]
    },
    "delete" : {
      "permissions" : [ ]
    }
  },
  "typeName" : "AWS::ECS::PrimaryTaskSet",
  "description" : "A pseudo-resource that manages which of your ECS task sets is primary.",
  "createOnlyProperties" : [ "/properties/Cluster", "/properties/Service" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/Cluster", "/properties/Service" ],
  "properties" : {
    "TaskSetId" : {
      "description" : "The ID or full Amazon Resource Name (ARN) of the task set.",
      "type" : "string"
    },
    "Cluster" : {
      "description" : "The short name or full Amazon Resource Name (ARN) of the cluster that hosts the service to create the task set in.",
      "type" : "string"
    },
    "Service" : {
      "description" : "The short name or full Amazon Resource Name (ARN) of the service to create the task set in.",
      "type" : "string"
    }
  },
  "required" : [ "Cluster", "Service", "TaskSetId" ]
}