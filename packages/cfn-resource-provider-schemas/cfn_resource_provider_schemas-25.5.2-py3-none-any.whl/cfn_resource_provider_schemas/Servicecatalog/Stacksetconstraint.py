SCHEMA = {
  "typeName" : "AWS::ServiceCatalog::StackSetConstraint",
  "description" : "Resource Type definition for AWS::ServiceCatalog::StackSetConstraint",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "StackInstanceControl" : {
      "type" : "string"
    },
    "AcceptLanguage" : {
      "type" : "string"
    },
    "PortfolioId" : {
      "type" : "string"
    },
    "ProductId" : {
      "type" : "string"
    },
    "RegionList" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "AdminRole" : {
      "type" : "string"
    },
    "AccountList" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "ExecutionRole" : {
      "type" : "string"
    }
  },
  "required" : [ "Description", "StackInstanceControl", "PortfolioId", "ProductId", "RegionList", "AdminRole", "AccountList", "ExecutionRole" ],
  "createOnlyProperties" : [ "/properties/PortfolioId", "/properties/ProductId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}