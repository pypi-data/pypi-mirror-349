SCHEMA = {
  "typeName" : "AWS::SQS::QueuePolicy",
  "description" : "The ``AWS::SQS::QueuePolicy`` type applies a policy to SQS queues. For an example snippet, see [Declaring an policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-sqs-policy) in the *User Guide*.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-sqs.git",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string",
      "description" : ""
    },
    "PolicyDocument" : {
      "type" : [ "object", "string" ],
      "description" : "A policy document that contains the permissions for the specified SQS queues. For more information about SQS policies, see [Using custom policies with the access policy language](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html) in the *Developer Guide*."
    },
    "Queues" : {
      "type" : "array",
      "description" : "The URLs of the queues to which you want to add the policy. You can use the ``Ref`` function to specify an ``AWS::SQS::Queue`` resource.",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "required" : [ "PolicyDocument", "Queues" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "sqs:SetQueueAttributes" ]
    },
    "update" : {
      "permissions" : [ "sqs:SetQueueAttributes" ]
    },
    "delete" : {
      "permissions" : [ "sqs:SetQueueAttributes" ]
    }
  }
}