SCHEMA = {
  "tagging" : {
    "permissions" : [ "quicksight:TagResource", "quicksight:UntagResource", "quicksight:ListTagsForResource" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "cloudFormationSystemTags" : False
  },
  "typeName" : "AWS::QuickSight::Template",
  "readOnlyProperties" : [ "/properties/Arn", "/properties/CreatedTime", "/properties/LastUpdatedTime", "/properties/Version" ],
  "description" : "Definition of the AWS::QuickSight::Template Resource Type.",
  "createOnlyProperties" : [ "/properties/AwsAccountId", "/properties/TemplateId" ],
  "primaryIdentifier" : [ "/properties/AwsAccountId", "/properties/TemplateId" ],
  "required" : [ "AwsAccountId", "TemplateId" ],
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-quicksight",
  "handlers" : {
    "read" : {
      "permissions" : [ "quicksight:DescribeTemplate", "quicksight:DescribeTemplatePermissions", "quicksight:ListTagsForResource" ]
    },
    "create" : {
      "permissions" : [ "quicksight:DescribeTemplate", "quicksight:DescribeTemplatePermissions", "quicksight:CreateTemplate", "quicksight:DescribeAnalysis", "quicksight:TagResource", "quicksight:UntagResource", "quicksight:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "quicksight:DescribeTemplate", "quicksight:DescribeTemplatePermissions", "quicksight:UpdateTemplate", "quicksight:UpdateTemplatePermissions", "quicksight:PassDataSet", "quicksight:TagResource", "quicksight:UntagResource", "quicksight:ListTagsForResource" ]
    },
    "list" : {
      "permissions" : [ "quicksight:ListTemplates" ],
      "handlerSchema" : {
        "properties" : {
          "AwsAccountId" : {
            "$ref" : "resource-schema.json#/properties/AwsAccountId"
          }
        },
        "required" : [ "AwsAccountId" ]
      }
    },
    "delete" : {
      "permissions" : [ "quicksight:DescribeTemplate", "quicksight:DeleteTemplate" ]
    }
  },
  "writeOnlyProperties" : [ "/properties/Definition", "/properties/VersionDescription", "/properties/SourceEntity", "/properties/ValidationStrategy" ],
  "additionalProperties" : False,
  "definitions" : {
    "PivotTotalOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TotalAggregationOptions" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TotalAggregationOption"
          }
        },
        "CustomLabel" : {
          "type" : "string"
        },
        "ValueCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "ScrollStatus" : {
          "$ref" : "#/definitions/TableTotalsScrollStatus"
        },
        "Placement" : {
          "$ref" : "#/definitions/TableTotalsPlacement"
        },
        "TotalCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "TotalsVisibility" : { },
        "MetricHeaderCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        }
      }
    },
    "Entity" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Path" : {
          "pattern" : "\\S",
          "type" : "string"
        }
      }
    },
    "DateTimePickerControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        },
        "HelperTextVisibility" : { },
        "DateIconVisibility" : { },
        "DateTimeFormat" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "GeospatialMapConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "MapStyleOptions" : {
          "$ref" : "#/definitions/GeospatialMapStyleOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/GeospatialMapFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "WindowOptions" : {
          "$ref" : "#/definitions/GeospatialWindowOptions"
        },
        "PointStyleOptions" : {
          "$ref" : "#/definitions/GeospatialPointStyleOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "ThousandSeparatorOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Symbol" : {
          "$ref" : "#/definitions/NumericSeparatorSymbol"
        },
        "Visibility" : { },
        "GroupingStyle" : {
          "$ref" : "#/definitions/DigitGroupingStyle"
        }
      }
    },
    "PredefinedHierarchy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "DrillDownFilters" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DrillDownFilter"
          }
        },
        "Columns" : {
          "minItems" : 1,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnIdentifier"
          }
        }
      },
      "required" : [ "Columns", "HierarchyId" ]
    },
    "DateTimeFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumericFormatConfiguration" : {
          "$ref" : "#/definitions/NumericFormatConfiguration"
        },
        "NullValueFormatConfiguration" : {
          "$ref" : "#/definitions/NullValueFormatConfiguration"
        },
        "DateTimeFormat" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "FilterControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Slider" : {
          "$ref" : "#/definitions/FilterSliderControl"
        },
        "TextArea" : {
          "$ref" : "#/definitions/FilterTextAreaControl"
        },
        "Dropdown" : {
          "$ref" : "#/definitions/FilterDropDownControl"
        },
        "TextField" : {
          "$ref" : "#/definitions/FilterTextFieldControl"
        },
        "List" : {
          "$ref" : "#/definitions/FilterListControl"
        },
        "DateTimePicker" : {
          "$ref" : "#/definitions/FilterDateTimePickerControl"
        },
        "RelativeDateTime" : {
          "$ref" : "#/definitions/FilterRelativeDateTimeControl"
        },
        "CrossSheet" : {
          "$ref" : "#/definitions/FilterCrossSheetControl"
        }
      }
    },
    "PivotTableSubtotalLevel" : {
      "type" : "string",
      "enum" : [ "ALL", "CUSTOM", "LAST" ]
    },
    "FormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumberFormatConfiguration" : {
          "$ref" : "#/definitions/NumberFormatConfiguration"
        },
        "DateTimeFormatConfiguration" : {
          "$ref" : "#/definitions/DateTimeFormatConfiguration"
        },
        "StringFormatConfiguration" : {
          "$ref" : "#/definitions/StringFormatConfiguration"
        }
      }
    },
    "ResourceStatus" : {
      "type" : "string",
      "enum" : [ "CREATION_IN_PROGRESS", "CREATION_SUCCESSFUL", "CREATION_FAILED", "UPDATE_IN_PROGRESS", "UPDATE_SUCCESSFUL", "UPDATE_FAILED", "DELETED" ]
    },
    "CommitMode" : {
      "type" : "string",
      "enum" : [ "AUTO", "MANUAL" ]
    },
    "RadarChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RadarChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/RadarChartAggregatedFieldWells"
        }
      }
    },
    "RollingDateConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "Expression" ]
    },
    "SeriesItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldSeriesItem" : {
          "$ref" : "#/definitions/FieldSeriesItem"
        },
        "DataFieldSeriesItem" : {
          "$ref" : "#/definitions/DataFieldSeriesItem"
        }
      }
    },
    "LineChartLineStyleSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LineInterpolation" : {
          "$ref" : "#/definitions/LineInterpolation"
        },
        "LineStyle" : {
          "$ref" : "#/definitions/LineChartLineStyle"
        },
        "LineVisibility" : { },
        "LineWidth" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      }
    },
    "FilledMapSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "MappedDataSetParameter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataSetParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "DataSetIdentifier", "DataSetParameterName" ]
    },
    "ReferenceLineLabelHorizontalPosition" : {
      "type" : "string",
      "enum" : [ "LEFT", "CENTER", "RIGHT" ]
    },
    "RelativeDateTimeControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        },
        "DateTimeFormat" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "BarChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/BarChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "ClusterMarkerConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ClusterMarker" : {
          "$ref" : "#/definitions/ClusterMarker"
        }
      }
    },
    "TableCellConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "TextFormat" : {
          "$ref" : "#/definitions/TextConditionalFormat"
        }
      },
      "required" : [ "FieldId" ]
    },
    "AssetOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Timezone" : {
          "type" : "string"
        },
        "WeekStart" : {
          "$ref" : "#/definitions/DayOfTheWeek"
        }
      }
    },
    "DateAxisOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MissingDateVisibility" : { }
      }
    },
    "KPIActualValueConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "Icon" : {
          "$ref" : "#/definitions/ConditionalFormattingIcon"
        }
      }
    },
    "TableUnaggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/UnaggregatedField"
          }
        }
      }
    },
    "TreeMapVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/TreeMapConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "AxisDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataOptions" : {
          "$ref" : "#/definitions/AxisDataOptions"
        },
        "TickLabelOptions" : {
          "$ref" : "#/definitions/AxisTickLabelOptions"
        },
        "AxisOffset" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "AxisLineVisibility" : { },
        "GridLineVisibility" : { },
        "ScrollbarOptions" : {
          "$ref" : "#/definitions/ScrollBarOptions"
        }
      }
    },
    "DataPathLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Visibility" : { },
        "FieldValue" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "FreeFormSectionLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Elements" : {
          "minItems" : 0,
          "maxItems" : 430,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FreeFormLayoutElement"
          }
        }
      },
      "required" : [ "Elements" ]
    },
    "DrillDownFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumericEqualityFilter" : {
          "$ref" : "#/definitions/NumericEqualityDrillDownFilter"
        },
        "TimeRangeFilter" : {
          "$ref" : "#/definitions/TimeRangeDrillDownFilter"
        },
        "CategoryFilter" : {
          "$ref" : "#/definitions/CategoryDrillDownFilter"
        }
      }
    },
    "CustomNarrativeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Narrative" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 150000
        }
      },
      "required" : [ "Narrative" ]
    },
    "LineChartDefaultSeriesSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LineStyleSettings" : {
          "$ref" : "#/definitions/LineChartLineStyleSettings"
        },
        "AxisBinding" : {
          "$ref" : "#/definitions/AxisBinding"
        },
        "MarkerStyleSettings" : {
          "$ref" : "#/definitions/LineChartMarkerStyleSettings"
        }
      }
    },
    "MaximumMinimumComputationType" : {
      "type" : "string",
      "enum" : [ "MAXIMUM", "MINIMUM" ]
    },
    "FunnelChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/FunnelChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "FilterSelectableValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "LineChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/LineChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "ReferenceLines" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ReferenceLine"
          }
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "SingleAxisOptions" : {
          "$ref" : "#/definitions/SingleAxisOptions"
        },
        "SmallMultiplesOptions" : {
          "$ref" : "#/definitions/SmallMultiplesOptions"
        },
        "PrimaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/LineSeriesAxisDisplayOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "XAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "DefaultSeriesSettings" : {
          "$ref" : "#/definitions/LineChartDefaultSeriesSettings"
        },
        "SecondaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "ForecastConfigurations" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ForecastConfiguration"
          }
        },
        "Series" : {
          "minItems" : 0,
          "maxItems" : 2000,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SeriesItem"
          }
        },
        "Type" : {
          "$ref" : "#/definitions/LineChartType"
        },
        "PrimaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "ContributionAnalysisDefaults" : {
          "minItems" : 1,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ContributionAnalysisDefault"
          }
        },
        "FieldWells" : {
          "$ref" : "#/definitions/LineChartFieldWells"
        },
        "SecondaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/LineSeriesAxisDisplayOptions"
        },
        "XAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "SectionAfterPageBreak" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/SectionPageBreakStatus"
        }
      }
    },
    "ComboChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BarValues" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Colors" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "LineValues" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "LayerMapVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : { },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "DataSetIdentifier", "VisualId" ]
    },
    "RelativeDateType" : {
      "type" : "string",
      "enum" : [ "PREVIOUS", "THIS", "LAST", "NOW", "NEXT" ]
    },
    "GaugeChartOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Arc" : {
          "$ref" : "#/definitions/ArcConfiguration"
        },
        "Comparison" : {
          "$ref" : "#/definitions/ComparisonConfiguration"
        },
        "PrimaryValueDisplayType" : {
          "$ref" : "#/definitions/PrimaryValueDisplayType"
        },
        "ArcAxis" : {
          "$ref" : "#/definitions/ArcAxisConfiguration"
        },
        "PrimaryValueFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      }
    },
    "MeasureField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DateMeasureField" : {
          "$ref" : "#/definitions/DateMeasureField"
        },
        "NumericalMeasureField" : {
          "$ref" : "#/definitions/NumericalMeasureField"
        },
        "CategoricalMeasureField" : {
          "$ref" : "#/definitions/CategoricalMeasureField"
        },
        "CalculatedMeasureField" : {
          "$ref" : "#/definitions/CalculatedMeasureField"
        }
      }
    },
    "ScatterPlotVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/ScatterPlotConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "AxisScale" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Logarithmic" : {
          "$ref" : "#/definitions/AxisLogarithmicScale"
        },
        "Linear" : {
          "$ref" : "#/definitions/AxisLinearScale"
        }
      }
    },
    "HeatMapAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Columns" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Rows" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "DefaultFilterDropDownControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DropDownControlDisplayOptions"
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/FilterSelectableValues"
        }
      }
    },
    "GaugeChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TargetValues" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "AxisLinearScale" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StepSize" : {
          "default" : None,
          "type" : "number"
        },
        "StepCount" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "ColumnRole" : {
      "type" : "string",
      "enum" : [ "DIMENSION", "MEASURE" ]
    },
    "BodySectionDynamicCategoryDimensionConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "SortByMetrics" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnSort"
          }
        },
        "Limit" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 1
        }
      },
      "required" : [ "Column" ]
    },
    "NegativeValueConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DisplayMode" : {
          "$ref" : "#/definitions/NegativeValueDisplayMode"
        }
      },
      "required" : [ "DisplayMode" ]
    },
    "PivotTableTotalOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColumnSubtotalOptions" : {
          "$ref" : "#/definitions/SubtotalOptions"
        },
        "RowSubtotalOptions" : {
          "$ref" : "#/definitions/SubtotalOptions"
        },
        "RowTotalOptions" : {
          "$ref" : "#/definitions/PivotTotalOptions"
        },
        "ColumnTotalOptions" : {
          "$ref" : "#/definitions/PivotTotalOptions"
        }
      }
    },
    "DynamicDefaultValue" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupNameColumn" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "DefaultValueColumn" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "UserNameColumn" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        }
      },
      "required" : [ "DefaultValueColumn" ]
    },
    "BodySectionConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Content" : {
          "$ref" : "#/definitions/BodySectionContent"
        },
        "Style" : {
          "$ref" : "#/definitions/SectionStyle"
        },
        "PageBreakConfiguration" : {
          "$ref" : "#/definitions/SectionPageBreakConfiguration"
        },
        "SectionId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "RepeatConfiguration" : {
          "$ref" : "#/definitions/BodySectionRepeatConfiguration"
        }
      },
      "required" : [ "Content", "SectionId" ]
    },
    "WordCloudAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupBy" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Size" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "DefaultGridLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/GridLayoutCanvasSizeOptions"
        }
      },
      "required" : [ "CanvasSizeOptions" ]
    },
    "GradientStop" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GradientOffset" : {
          "default" : 0,
          "type" : "number"
        },
        "DataValue" : {
          "default" : None,
          "type" : "number"
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      },
      "required" : [ "GradientOffset" ]
    },
    "GaugeChartPrimaryValueConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "Icon" : {
          "$ref" : "#/definitions/ConditionalFormattingIcon"
        }
      }
    },
    "PluginVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "PluginArn" : {
          "type" : "string"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/PluginVisualConfiguration"
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "PluginArn", "VisualId" ]
    },
    "BoxPlotFillStyle" : {
      "type" : "string",
      "enum" : [ "SOLID", "TRANSPARENT" ]
    },
    "ImageInteractionOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ImageMenuOption" : {
          "$ref" : "#/definitions/ImageMenuOption"
        }
      }
    },
    "DataLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MaximumLabelType" : {
          "$ref" : "#/definitions/MaximumLabelType"
        },
        "DataPathLabelType" : {
          "$ref" : "#/definitions/DataPathLabelType"
        },
        "RangeEndsLabelType" : {
          "$ref" : "#/definitions/RangeEndsLabelType"
        },
        "FieldLabelType" : {
          "$ref" : "#/definitions/FieldLabelType"
        },
        "MinimumLabelType" : {
          "$ref" : "#/definitions/MinimumLabelType"
        }
      }
    },
    "WordCloudCloudLayout" : {
      "type" : "string",
      "enum" : [ "FLUID", "NORMAL" ]
    },
    "MaximumLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "TooltipTarget" : {
      "type" : "string",
      "enum" : [ "BOTH", "BAR", "LINE" ]
    },
    "DataLabelPosition" : {
      "type" : "string",
      "enum" : [ "INSIDE", "OUTSIDE", "LEFT", "TOP", "BOTTOM", "RIGHT" ]
    },
    "GeospatialMapStyleOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BaseMapStyle" : {
          "$ref" : "#/definitions/BaseMapStyleType"
        }
      }
    },
    "Layout" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Configuration" : {
          "$ref" : "#/definitions/LayoutConfiguration"
        }
      },
      "required" : [ "Configuration" ]
    },
    "ReferenceLineValueLabelConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FormatConfiguration" : {
          "$ref" : "#/definitions/NumericFormatConfiguration"
        },
        "RelativePosition" : {
          "$ref" : "#/definitions/ReferenceLineValueLabelRelativePosition"
        }
      }
    },
    "StringValueWhenUnsetConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ValueWhenUnsetOption" : {
          "$ref" : "#/definitions/ValueWhenUnsetOption"
        },
        "CustomValue" : {
          "type" : "string"
        }
      }
    },
    "PivotTableSortBy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Field" : {
          "$ref" : "#/definitions/FieldSort"
        },
        "DataPath" : {
          "$ref" : "#/definitions/DataPathSort"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnSort"
        }
      }
    },
    "SimpleClusterMarker" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "SheetImageSource" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SheetImageStaticFileSource" : {
          "$ref" : "#/definitions/SheetImageStaticFileSource"
        }
      }
    },
    "FilterDateTimePickerControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlDateTimePickerType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DateTimePickerControlDisplayOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "LegendPosition" : {
      "type" : "string",
      "enum" : [ "AUTO", "RIGHT", "BOTTOM", "TOP" ]
    },
    "PluginVisualFieldWell" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Unaggregated" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/UnaggregatedField"
          }
        },
        "AxisName" : {
          "$ref" : "#/definitions/PluginVisualAxisName"
        },
        "Measures" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Dimensions" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "KPIVisualLayoutOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StandardLayout" : {
          "$ref" : "#/definitions/KPIVisualStandardLayout"
        }
      }
    },
    "TimeRangeFilterValue" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RollingDate" : {
          "$ref" : "#/definitions/RollingDateConfiguration"
        },
        "StaticValue" : {
          "format" : "date-time",
          "type" : "string"
        },
        "Parameter" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "PivotTableRowsLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "Visibility" : { }
      }
    },
    "WordCloudOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WordOrientation" : {
          "$ref" : "#/definitions/WordCloudWordOrientation"
        },
        "WordScaling" : {
          "$ref" : "#/definitions/WordCloudWordScaling"
        },
        "CloudLayout" : {
          "$ref" : "#/definitions/WordCloudCloudLayout"
        },
        "MaximumStringLength" : {
          "maximum" : 100,
          "type" : "number",
          "minimum" : 1
        },
        "WordCasing" : {
          "$ref" : "#/definitions/WordCloudWordCasing"
        },
        "WordPadding" : {
          "$ref" : "#/definitions/WordCloudWordPadding"
        }
      }
    },
    "ParameterDropDownControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DropDownControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "CascadingControlConfiguration" : {
          "$ref" : "#/definitions/CascadingControlConfiguration"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/ParameterSelectableValues"
        }
      },
      "required" : [ "ParameterControlId", "SourceParameterName", "Title" ]
    },
    "TableFieldOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "URLStyling" : {
          "$ref" : "#/definitions/TableFieldURLConfiguration"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Visibility" : { },
        "Width" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      },
      "required" : [ "FieldId" ]
    },
    "IntegerParameterDeclaration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MappedDataSetParameters" : {
          "minItems" : 0,
          "maxItems" : 150,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MappedDataSetParameter"
          }
        },
        "DefaultValues" : {
          "$ref" : "#/definitions/IntegerDefaultValues"
        },
        "ParameterValueType" : {
          "$ref" : "#/definitions/ParameterValueType"
        },
        "ValueWhenUnset" : {
          "$ref" : "#/definitions/IntegerValueWhenUnsetConfiguration"
        },
        "Name" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "Name", "ParameterValueType" ]
    },
    "FontConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FontFamily" : {
          "type" : "string"
        },
        "FontStyle" : {
          "$ref" : "#/definitions/FontStyle"
        },
        "FontSize" : {
          "$ref" : "#/definitions/FontSize"
        },
        "FontDecoration" : {
          "$ref" : "#/definitions/FontDecoration"
        },
        "FontColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "FontWeight" : {
          "$ref" : "#/definitions/FontWeight"
        }
      }
    },
    "VisualSubtitleLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "FormatText" : {
          "$ref" : "#/definitions/LongFormatText"
        }
      }
    },
    "DataPathType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PivotTableDataPathType" : {
          "$ref" : "#/definitions/PivotTableDataPathType"
        }
      }
    },
    "ArcAxisConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Range" : {
          "$ref" : "#/definitions/ArcAxisDisplayRange"
        },
        "ReserveRange" : {
          "default" : 0,
          "type" : "number"
        }
      }
    },
    "NumericEqualityFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "Value" : {
          "default" : None,
          "type" : "number"
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "MatchOperator" : {
          "$ref" : "#/definitions/NumericEqualityMatchOperator"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/NumericFilterSelectAllOptions"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FilterId", "MatchOperator", "NullOption" ]
    },
    "ShapeConditionalFormat" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BackgroundColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        }
      },
      "required" : [ "BackgroundColor" ]
    },
    "GaugeChartArcConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ForegroundColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        }
      }
    },
    "AxisLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "type" : "string"
        },
        "ApplyTo" : {
          "$ref" : "#/definitions/AxisLabelReferenceOptions"
        },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      }
    },
    "DataSetReference" : {
      "description" : "<p>Dataset reference.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataSetArn" : {
          "description" : "<p>Dataset Amazon Resource Name (ARN).</p>",
          "type" : "string"
        },
        "DataSetPlaceholder" : {
          "pattern" : "\\S",
          "description" : "<p>Dataset placeholder.</p>",
          "type" : "string"
        }
      },
      "required" : [ "DataSetArn", "DataSetPlaceholder" ]
    },
    "ScatterPlotCategoricallyAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Size" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Label" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "XAxis" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "YAxis" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "LongFormatText" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RichText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "PlainText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      }
    },
    "RadarChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Color" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "FilterOperationTargetVisualsConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SameSheetTargetVisualConfiguration" : {
          "$ref" : "#/definitions/SameSheetTargetVisualConfiguration"
        }
      }
    },
    "GrowthRateComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "PeriodSize" : {
          "default" : 0,
          "maximum" : 52,
          "type" : "number",
          "minimum" : 2
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "KPIOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SecondaryValueFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "VisualLayoutOptions" : {
          "$ref" : "#/definitions/KPIVisualLayoutOptions"
        },
        "TrendArrows" : {
          "$ref" : "#/definitions/TrendArrowOptions"
        },
        "SecondaryValue" : {
          "$ref" : "#/definitions/SecondaryValueOptions"
        },
        "Comparison" : {
          "$ref" : "#/definitions/ComparisonConfiguration"
        },
        "PrimaryValueDisplayType" : {
          "$ref" : "#/definitions/PrimaryValueDisplayType"
        },
        "ProgressBar" : {
          "$ref" : "#/definitions/ProgressBarOptions"
        },
        "PrimaryValueFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "Sparkline" : {
          "$ref" : "#/definitions/KPISparklineOptions"
        }
      }
    },
    "AttributeAggregationFunction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SimpleAttributeAggregation" : {
          "$ref" : "#/definitions/SimpleAttributeAggregationFunction"
        },
        "ValueForMultipleValues" : {
          "type" : "string"
        }
      }
    },
    "SectionBasedLayoutCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PaperCanvasSizeOptions" : {
          "$ref" : "#/definitions/SectionBasedLayoutPaperCanvasSizeOptions"
        }
      }
    },
    "NumericRangeFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "IncludeMaximum" : {
          "default" : None,
          "type" : "boolean"
        },
        "RangeMinimum" : {
          "$ref" : "#/definitions/NumericRangeFilterValue"
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/NumericFilterSelectAllOptions"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "RangeMaximum" : {
          "$ref" : "#/definitions/NumericRangeFilterValue"
        },
        "IncludeMinimum" : {
          "default" : None,
          "type" : "boolean"
        }
      },
      "required" : [ "Column", "FilterId", "NullOption" ]
    },
    "FieldSortOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldSort" : {
          "$ref" : "#/definitions/FieldSort"
        },
        "ColumnSort" : {
          "$ref" : "#/definitions/ColumnSort"
        }
      }
    },
    "ColorsConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomColors" : {
          "minItems" : 0,
          "maxItems" : 50,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/CustomColor"
          }
        }
      }
    },
    "HistogramBinType" : {
      "type" : "string",
      "enum" : [ "BIN_COUNT", "BIN_WIDTH" ]
    },
    "ComboChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/ComboChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "ReferenceLines" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ReferenceLine"
          }
        },
        "ColorLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "BarDataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "SingleAxisOptions" : {
          "$ref" : "#/definitions/SingleAxisOptions"
        },
        "PrimaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "BarsArrangement" : {
          "$ref" : "#/definitions/BarsArrangement"
        },
        "SecondaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "LineDataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "CategoryAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "PrimaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/ComboChartFieldWells"
        },
        "SecondaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "TreeMapFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TreeMapAggregatedFieldWells" : {
          "$ref" : "#/definitions/TreeMapAggregatedFieldWells"
        }
      }
    },
    "DateTimeHierarchy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "DrillDownFilters" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DrillDownFilter"
          }
        }
      },
      "required" : [ "HierarchyId" ]
    },
    "PercentileAggregation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PercentileValue" : {
          "maximum" : 100,
          "type" : "number",
          "minimum" : 0
        }
      }
    },
    "WaterfallChartGroupColorConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NegativeBarColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "TotalBarColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "PositiveBarColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "FunnelChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FunnelChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/FunnelChartAggregatedFieldWells"
        }
      }
    },
    "StringParameterDeclaration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MappedDataSetParameters" : {
          "minItems" : 0,
          "maxItems" : 150,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MappedDataSetParameter"
          }
        },
        "DefaultValues" : {
          "$ref" : "#/definitions/StringDefaultValues"
        },
        "ParameterValueType" : {
          "$ref" : "#/definitions/ParameterValueType"
        },
        "ValueWhenUnset" : {
          "$ref" : "#/definitions/StringValueWhenUnsetConfiguration"
        },
        "Name" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "Name", "ParameterValueType" ]
    },
    "DataLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataLabelTypes" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataLabelType"
          }
        },
        "MeasureLabelVisibility" : { },
        "Position" : {
          "$ref" : "#/definitions/DataLabelPosition"
        },
        "LabelContent" : {
          "$ref" : "#/definitions/DataLabelContent"
        },
        "Visibility" : { },
        "TotalsVisibility" : { },
        "Overlap" : {
          "$ref" : "#/definitions/DataLabelOverlap"
        },
        "CategoryLabelVisibility" : { },
        "LabelColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "LabelFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      }
    },
    "TreeMapConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/TreeMapSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "ColorLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "SizeLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/TreeMapFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "ColorScale" : {
          "$ref" : "#/definitions/ColorScale"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "GroupLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        }
      }
    },
    "FontSize" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Relative" : {
          "$ref" : "#/definitions/RelativeFontSize"
        },
        "Absolute" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      }
    },
    "InnerFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryInnerFilter" : {
          "$ref" : "#/definitions/CategoryInnerFilter"
        }
      }
    },
    "PivotTableFieldCollapseStateTarget" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "type" : "string"
        },
        "FieldDataPathValues" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataPathValue"
          }
        }
      }
    },
    "SheetVisualScopingConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Scope" : {
          "$ref" : "#/definitions/FilterVisualScope"
        },
        "SheetId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "VisualIds" : {
          "minItems" : 0,
          "maxItems" : 50,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "^[\\w\\-]+$",
            "type" : "string",
            "maxLength" : 512
          }
        }
      },
      "required" : [ "Scope", "SheetId" ]
    },
    "WidgetStatus" : {
      "type" : "string",
      "enum" : [ "ENABLED", "DISABLED" ]
    },
    "SheetImageTooltipConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "TooltipText" : {
          "$ref" : "#/definitions/SheetImageTooltipText"
        }
      }
    },
    "BodySectionRepeatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DimensionConfigurations" : {
          "minItems" : 0,
          "maxItems" : 3,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/BodySectionRepeatDimensionConfiguration"
          }
        },
        "NonRepeatingVisuals" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "^[\\w\\-]+$",
            "type" : "string",
            "maxLength" : 512
          }
        },
        "PageBreakConfiguration" : {
          "$ref" : "#/definitions/BodySectionRepeatPageBreakConfiguration"
        }
      }
    },
    "SheetControlSliderType" : {
      "type" : "string",
      "enum" : [ "SINGLE_POINT", "RANGE" ]
    },
    "TableBorderOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Thickness" : {
          "maximum" : 4,
          "type" : "number",
          "minimum" : 1
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "Style" : {
          "$ref" : "#/definitions/TableBorderStyle"
        }
      }
    },
    "Icon" : {
      "type" : "string",
      "enum" : [ "CARET_UP", "CARET_DOWN", "PLUS", "MINUS", "ARROW_UP", "ARROW_DOWN", "ARROW_LEFT", "ARROW_UP_LEFT", "ARROW_DOWN_LEFT", "ARROW_RIGHT", "ARROW_UP_RIGHT", "ARROW_DOWN_RIGHT", "FACE_UP", "FACE_DOWN", "FACE_FLAT", "ONE_BAR", "TWO_BAR", "THREE_BAR", "CIRCLE", "TRIANGLE", "SQUARE", "FLAG", "THUMBS_UP", "THUMBS_DOWN", "CHECKMARK", "X" ]
    },
    "DefaultFilterControlConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ControlOptions" : {
          "$ref" : "#/definitions/DefaultFilterControlOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "ControlOptions", "Title" ]
    },
    "DataBarsOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PositiveColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "NegativeColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      },
      "required" : [ "FieldId" ]
    },
    "TablePaginatedReportOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "OverflowColumnHeaderVisibility" : { },
        "VerticalOverflowVisibility" : { }
      }
    },
    "EmptyVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "DataSetIdentifier", "VisualId" ]
    },
    "KPISparklineOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/KPISparklineType"
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "TooltipVisibility" : { },
        "Visibility" : { }
      },
      "required" : [ "Type" ]
    },
    "CustomFilterConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryValue" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 512
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "MatchOperator" : {
          "$ref" : "#/definitions/CategoryFilterMatchOperator"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/CategoryFilterSelectAllOptions"
        }
      },
      "required" : [ "MatchOperator", "NullOption" ]
    },
    "CustomContentImageScalingConfiguration" : {
      "type" : "string",
      "enum" : [ "FIT_TO_HEIGHT", "FIT_TO_WIDTH", "DO_NOT_SCALE", "SCALE_TO_VISUAL" ]
    },
    "DecimalDefaultValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DynamicValue" : {
          "$ref" : "#/definitions/DynamicDefaultValue"
        },
        "StaticValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "number"
          }
        }
      }
    },
    "TimeRangeFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RangeMinimumValue" : {
          "$ref" : "#/definitions/TimeRangeFilterValue"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "RangeMaximumValue" : {
          "$ref" : "#/definitions/TimeRangeFilterValue"
        },
        "IncludeMaximum" : {
          "default" : None,
          "type" : "boolean"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "IncludeMinimum" : {
          "default" : None,
          "type" : "boolean"
        },
        "ExcludePeriodConfiguration" : {
          "$ref" : "#/definitions/ExcludePeriodConfiguration"
        }
      },
      "required" : [ "Column", "FilterId", "NullOption" ]
    },
    "WordCloudSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "RadarChartAreaStyleSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "AxisDisplayDataDrivenRange" : {
      "additionalProperties" : False,
      "type" : "object"
    },
    "FilterGroup" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "Filters" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Filter"
          }
        },
        "CrossDataset" : {
          "$ref" : "#/definitions/CrossDatasetTypes"
        },
        "ScopeConfiguration" : {
          "$ref" : "#/definitions/FilterScopeConfiguration"
        },
        "FilterGroupId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "CrossDataset", "FilterGroupId", "Filters", "ScopeConfiguration" ]
    },
    "FontWeight" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/FontWeightName"
        }
      }
    },
    "TooltipItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldTooltipItem" : {
          "$ref" : "#/definitions/FieldTooltipItem"
        },
        "ColumnTooltipItem" : {
          "$ref" : "#/definitions/ColumnTooltipItem"
        }
      }
    },
    "AxisDataOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DateAxisOptions" : {
          "$ref" : "#/definitions/DateAxisOptions"
        },
        "NumericAxisOptions" : {
          "$ref" : "#/definitions/NumericAxisOptions"
        }
      }
    },
    "FilterOperationSelectedFieldsConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SelectedColumns" : {
          "minItems" : 0,
          "maxItems" : 10,
          "description" : "<p>The selected columns of a dataset.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnIdentifier"
          }
        },
        "SelectedFields" : {
          "minItems" : 1,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "type" : "string",
            "maxLength" : 512
          }
        },
        "SelectedFieldOptions" : {
          "$ref" : "#/definitions/SelectedFieldOptions"
        }
      }
    },
    "BarsArrangement" : {
      "type" : "string",
      "enum" : [ "CLUSTERED", "STACKED", "STACKED_PERCENT" ]
    },
    "ExcludePeriodConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "Amount" : {
          "default" : None,
          "type" : "number"
        },
        "Granularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        }
      },
      "required" : [ "Amount", "Granularity" ]
    },
    "RadarChartShape" : {
      "type" : "string",
      "enum" : [ "CIRCLE", "POLYGON" ]
    },
    "ScrollBarOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "VisibleRange" : {
          "$ref" : "#/definitions/VisibleRangeOptions"
        },
        "Visibility" : { }
      }
    },
    "ConditionalFormattingCustomIconOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "UnicodeIcon" : {
          "pattern" : "^[^\\u0000-\\u00FF]$",
          "type" : "string"
        },
        "Icon" : {
          "$ref" : "#/definitions/Icon"
        }
      }
    },
    "DefaultInteractiveLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FreeForm" : {
          "$ref" : "#/definitions/DefaultFreeFormLayoutConfiguration"
        },
        "Grid" : {
          "$ref" : "#/definitions/DefaultGridLayoutConfiguration"
        }
      }
    },
    "LineChartSeriesSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LineStyleSettings" : {
          "$ref" : "#/definitions/LineChartLineStyleSettings"
        },
        "MarkerStyleSettings" : {
          "$ref" : "#/definitions/LineChartMarkerStyleSettings"
        }
      }
    },
    "SortDirection" : {
      "type" : "string",
      "enum" : [ "ASC", "DESC" ]
    },
    "ScatterPlotConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "YAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "SortConfiguration" : {
          "$ref" : "#/definitions/ScatterPlotSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "YAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/ScatterPlotFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "XAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "XAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        }
      }
    },
    "CustomContentType" : {
      "type" : "string",
      "enum" : [ "IMAGE", "OTHER_EMBEDDED_CONTENT" ]
    },
    "DefaultTextAreaControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Delimiter" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextAreaControlDisplayOptions"
        }
      }
    },
    "TemplateVersionDefinition" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Options" : {
          "$ref" : "#/definitions/AssetOptions"
        },
        "FilterGroups" : {
          "minItems" : 0,
          "maxItems" : 2000,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FilterGroup"
          }
        },
        "QueryExecutionOptions" : {
          "$ref" : "#/definitions/QueryExecutionOptions"
        },
        "CalculatedFields" : {
          "minItems" : 0,
          "maxItems" : 500,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/CalculatedField"
          }
        },
        "DataSetConfigurations" : {
          "minItems" : 0,
          "maxItems" : 30,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataSetConfiguration"
          }
        },
        "ColumnConfigurations" : {
          "minItems" : 0,
          "maxItems" : 2000,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnConfiguration"
          }
        },
        "AnalysisDefaults" : {
          "$ref" : "#/definitions/AnalysisDefaults"
        },
        "Sheets" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetDefinition"
          }
        },
        "ParameterDeclarations" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ParameterDeclaration"
          }
        }
      },
      "required" : [ "DataSetConfigurations" ]
    },
    "VisualCustomActionTrigger" : {
      "type" : "string",
      "enum" : [ "DATA_POINT_CLICK", "DATA_POINT_MENU" ]
    },
    "SankeyDiagramAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Destination" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Source" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Weight" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "TableConditionalFormattingOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Row" : {
          "$ref" : "#/definitions/TableRowConditionalFormatting"
        },
        "Cell" : {
          "$ref" : "#/definitions/TableCellConditionalFormatting"
        }
      }
    },
    "ArcThickness" : {
      "type" : "string",
      "enum" : [ "SMALL", "MEDIUM", "LARGE", "WHOLE" ]
    },
    "CalculatedMeasureField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Expression", "FieldId" ]
    },
    "FieldSeriesItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "AxisBinding" : {
          "$ref" : "#/definitions/AxisBinding"
        },
        "Settings" : {
          "$ref" : "#/definitions/LineChartSeriesSettings"
        }
      },
      "required" : [ "AxisBinding", "FieldId" ]
    },
    "FilterDropDownControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DropDownControlDisplayOptions"
        },
        "CascadingControlConfiguration" : {
          "$ref" : "#/definitions/CascadingControlConfiguration"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/FilterSelectableValues"
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "BoxPlotAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupBy" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 5,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "RelativeDatesFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RelativeDateValue" : {
          "default" : None,
          "type" : "number"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "RelativeDateType" : {
          "$ref" : "#/definitions/RelativeDateType"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "AnchorDateConfiguration" : {
          "$ref" : "#/definitions/AnchorDateConfiguration"
        },
        "MinimumGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "ExcludePeriodConfiguration" : {
          "$ref" : "#/definitions/ExcludePeriodConfiguration"
        }
      },
      "required" : [ "AnchorDateConfiguration", "Column", "FilterId", "NullOption", "RelativeDateType", "TimeGranularity" ]
    },
    "ParameterControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Slider" : {
          "$ref" : "#/definitions/ParameterSliderControl"
        },
        "TextArea" : {
          "$ref" : "#/definitions/ParameterTextAreaControl"
        },
        "Dropdown" : {
          "$ref" : "#/definitions/ParameterDropDownControl"
        },
        "TextField" : {
          "$ref" : "#/definitions/ParameterTextFieldControl"
        },
        "List" : {
          "$ref" : "#/definitions/ParameterListControl"
        },
        "DateTimePicker" : {
          "$ref" : "#/definitions/ParameterDateTimePickerControl"
        }
      }
    },
    "DigitGroupingStyle" : {
      "type" : "string",
      "enum" : [ "DEFAULT", "LAKHS" ]
    },
    "ReferenceLineLabelConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HorizontalPosition" : {
          "$ref" : "#/definitions/ReferenceLineLabelHorizontalPosition"
        },
        "ValueLabelConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineValueLabelConfiguration"
        },
        "CustomLabelConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineCustomLabelConfiguration"
        },
        "FontColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "VerticalPosition" : {
          "$ref" : "#/definitions/ReferenceLineLabelVerticalPosition"
        }
      }
    },
    "HistogramVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/HistogramConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "VisualId" ]
    },
    "DateTimeValueWhenUnsetConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ValueWhenUnsetOption" : {
          "$ref" : "#/definitions/ValueWhenUnsetOption"
        },
        "CustomValue" : {
          "format" : "date-time",
          "type" : "string"
        }
      }
    },
    "PivotTableVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "ConditionalFormatting" : {
          "$ref" : "#/definitions/PivotTableConditionalFormatting"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/PivotTableConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "VisualId" ]
    },
    "PluginVisualItemsLimitConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ItemsLimit" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "GridLayoutElement" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ElementType" : {
          "$ref" : "#/definitions/LayoutElementType"
        },
        "ColumnSpan" : {
          "maximum" : 36,
          "type" : "number",
          "minimum" : 1
        },
        "ColumnIndex" : {
          "maximum" : 35,
          "type" : "number",
          "minimum" : 0
        },
        "RowIndex" : {
          "maximum" : 9009,
          "type" : "number",
          "minimum" : 0
        },
        "RowSpan" : {
          "maximum" : 21,
          "type" : "number",
          "minimum" : 1
        },
        "ElementId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "ColumnSpan", "ElementId", "ElementType", "RowSpan" ]
    },
    "FreeFormLayoutElement" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ElementType" : {
          "$ref" : "#/definitions/LayoutElementType"
        },
        "BorderStyle" : {
          "$ref" : "#/definitions/FreeFormLayoutElementBorderStyle"
        },
        "Height" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "Visibility" : { },
        "RenderingRules" : {
          "minItems" : 0,
          "maxItems" : 10000,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetElementRenderingRule"
          }
        },
        "YAxisLocation" : {
          "description" : "String based length that is composed of value and unit in px with Integer.MAX_VALUE as maximum value",
          "type" : "string"
        },
        "LoadingAnimation" : {
          "$ref" : "#/definitions/LoadingAnimation"
        },
        "Width" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "BackgroundStyle" : {
          "$ref" : "#/definitions/FreeFormLayoutElementBackgroundStyle"
        },
        "ElementId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "XAxisLocation" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "SelectedBorderStyle" : {
          "$ref" : "#/definitions/FreeFormLayoutElementBorderStyle"
        }
      },
      "required" : [ "ElementId", "ElementType", "Height", "Width", "XAxisLocation", "YAxisLocation" ]
    },
    "LineInterpolation" : {
      "type" : "string",
      "enum" : [ "LINEAR", "SMOOTH", "STEPPED" ]
    },
    "CustomValuesConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "IncludeNullValue" : {
          "type" : "boolean"
        },
        "CustomValues" : {
          "$ref" : "#/definitions/CustomParameterValues"
        }
      },
      "required" : [ "CustomValues" ]
    },
    "DefaultNewSheetConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SheetContentType" : {
          "$ref" : "#/definitions/SheetContentType"
        },
        "InteractiveLayoutConfiguration" : {
          "$ref" : "#/definitions/DefaultInteractiveLayoutConfiguration"
        },
        "PaginatedLayoutConfiguration" : {
          "$ref" : "#/definitions/DefaultPaginatedLayoutConfiguration"
        }
      }
    },
    "GaugeChartConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ConditionalFormattingOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/GaugeChartConditionalFormattingOption"
          }
        }
      }
    },
    "FilledMapFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilledMapAggregatedFieldWells" : {
          "$ref" : "#/definitions/FilledMapAggregatedFieldWells"
        }
      }
    },
    "AxisDisplayRange" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataDriven" : {
          "$ref" : "#/definitions/AxisDisplayDataDrivenRange"
        },
        "MinMax" : {
          "$ref" : "#/definitions/AxisDisplayMinMaxRange"
        }
      }
    },
    "ForecastComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PeriodsBackward" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 0
        },
        "PeriodsForward" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 1
        },
        "PredictionInterval" : {
          "maximum" : 95,
          "type" : "number",
          "minimum" : 50
        },
        "Seasonality" : {
          "$ref" : "#/definitions/ForecastComputationSeasonality"
        },
        "CustomSeasonalityValue" : {
          "default" : None,
          "maximum" : 180,
          "type" : "number",
          "minimum" : 1
        },
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "UpperBoundary" : {
          "default" : None,
          "type" : "number"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        },
        "LowerBoundary" : {
          "default" : None,
          "type" : "number"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "WordCloudWordPadding" : {
      "type" : "string",
      "enum" : [ "NONE", "SMALL", "MEDIUM", "LARGE" ]
    },
    "PivotTableDataPathOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataPathList" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataPathValue"
          }
        },
        "Width" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      },
      "required" : [ "DataPathList" ]
    },
    "TextFieldControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "PlaceholderOptions" : {
          "$ref" : "#/definitions/TextControlPlaceholderOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        }
      }
    },
    "TransposedTableOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColumnWidth" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "ColumnIndex" : {
          "maximum" : 9999,
          "type" : "number",
          "minimum" : 0
        },
        "ColumnType" : {
          "$ref" : "#/definitions/TransposedColumnType"
        }
      },
      "required" : [ "ColumnType" ]
    },
    "AxisBinding" : {
      "type" : "string",
      "enum" : [ "PRIMARY_YAXIS", "SECONDARY_YAXIS" ]
    },
    "PivotTableSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldSortOptions" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotFieldSortOptions"
          }
        }
      }
    },
    "ReferenceLinePatternType" : {
      "type" : "string",
      "enum" : [ "SOLID", "DASHED", "DOTTED" ]
    },
    "NumericAxisOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Scale" : {
          "$ref" : "#/definitions/AxisScale"
        },
        "Range" : {
          "$ref" : "#/definitions/AxisDisplayRange"
        }
      }
    },
    "VisualCustomActionOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NavigationOperation" : {
          "$ref" : "#/definitions/CustomActionNavigationOperation"
        },
        "SetParametersOperation" : {
          "$ref" : "#/definitions/CustomActionSetParametersOperation"
        },
        "FilterOperation" : {
          "$ref" : "#/definitions/CustomActionFilterOperation"
        },
        "URLOperation" : {
          "$ref" : "#/definitions/CustomActionURLOperation"
        }
      }
    },
    "NumericRangeFilterValue" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StaticValue" : {
          "default" : None,
          "type" : "number"
        },
        "Parameter" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "BoxPlotVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/BoxPlotChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "CustomFilterListConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryValues" : {
          "minItems" : 0,
          "maxItems" : 100000,
          "type" : "array",
          "items" : {
            "minLength" : 0,
            "type" : "string",
            "maxLength" : 512
          }
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "MatchOperator" : {
          "$ref" : "#/definitions/CategoryFilterMatchOperator"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/CategoryFilterSelectAllOptions"
        }
      },
      "required" : [ "MatchOperator", "NullOption" ]
    },
    "FreeFormLayoutElementBackgroundStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        },
        "Visibility" : { }
      }
    },
    "SheetImageScalingType" : {
      "type" : "string",
      "enum" : [ "SCALE_TO_WIDTH", "SCALE_TO_HEIGHT", "SCALE_TO_CONTAINER", "SCALE_NONE" ]
    },
    "BoxPlotFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BoxPlotAggregatedFieldWells" : {
          "$ref" : "#/definitions/BoxPlotAggregatedFieldWells"
        }
      }
    },
    "SheetElementRenderingRule" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "ConfigurationOverrides" : {
          "$ref" : "#/definitions/SheetElementConfigurationOverrides"
        }
      },
      "required" : [ "ConfigurationOverrides", "Expression" ]
    },
    "TrendArrowOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "ValidationStrategy" : {
      "description" : "<p>The option to relax the validation that is required to create and update analyses, dashboards, and templates with definition objects. When you set this value to <code>LENIENT</code>, validation is skipped for specific errors.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Mode" : {
          "$ref" : "#/definitions/ValidationStrategyMode"
        }
      },
      "required" : [ "Mode" ]
    },
    "ConditionalFormattingIconSetType" : {
      "type" : "string",
      "enum" : [ "PLUS_MINUS", "CHECK_X", "THREE_COLOR_ARROW", "THREE_GRAY_ARROW", "CARET_UP_MINUS_DOWN", "THREE_SHAPE", "THREE_CIRCLE", "FLAGS", "BARS", "FOUR_COLOR_ARROW", "FOUR_GRAY_ARROW" ]
    },
    "TableCellImageSizingConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TableCellImageScalingConfiguration" : {
          "$ref" : "#/definitions/TableCellImageScalingConfiguration"
        }
      }
    },
    "GeospatialHeatmapConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HeatmapColor" : {
          "$ref" : "#/definitions/GeospatialHeatmapColorScale"
        }
      }
    },
    "StaticFile" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ImageStaticFile" : {
          "$ref" : "#/definitions/ImageStaticFile"
        },
        "SpatialStaticFile" : {
          "$ref" : "#/definitions/SpatialStaticFile"
        }
      }
    },
    "PanelTitleOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "HorizontalTextAlignment" : {
          "$ref" : "#/definitions/HorizontalTextAlignment"
        }
      }
    },
    "FunnelChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "SelectAllValueOptions" : {
      "type" : "string",
      "enum" : [ "ALL_VALUES" ]
    },
    "GeospatialCoordinateBounds" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "West" : {
          "maximum" : 1800,
          "type" : "number",
          "minimum" : -1800
        },
        "South" : {
          "maximum" : 90,
          "type" : "number",
          "minimum" : -90
        },
        "North" : {
          "maximum" : 90,
          "type" : "number",
          "minimum" : -90
        },
        "East" : {
          "maximum" : 1800,
          "type" : "number",
          "minimum" : -1800
        }
      },
      "required" : [ "East", "North", "South", "West" ]
    },
    "PivotTableConditionalFormattingScopeRole" : {
      "type" : "string",
      "enum" : [ "FIELD", "FIELD_TOTAL", "GRAND_TOTAL" ]
    },
    "BoxPlotStyleOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FillStyle" : {
          "$ref" : "#/definitions/BoxPlotFillStyle"
        }
      }
    },
    "StringDefaultValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DynamicValue" : {
          "$ref" : "#/definitions/DynamicDefaultValue"
        },
        "StaticValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "SheetImageScalingConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScalingType" : {
          "$ref" : "#/definitions/SheetImageScalingType"
        }
      }
    },
    "FreeFormLayoutElementBorderStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        },
        "Visibility" : { }
      }
    },
    "CategoryFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Configuration" : {
          "$ref" : "#/definitions/CategoryFilterConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "Configuration", "FilterId" ]
    },
    "VerticalTextAlignment" : {
      "type" : "string",
      "enum" : [ "TOP", "MIDDLE", "BOTTOM", "AUTO" ]
    },
    "FilterNullOption" : {
      "type" : "string",
      "enum" : [ "ALL_VALUES", "NULLS_ONLY", "NON_NULLS_ONLY" ]
    },
    "FilledMapVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "ConditionalFormatting" : {
          "$ref" : "#/definitions/FilledMapConditionalFormatting"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/FilledMapConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "SmallMultiplesAxisScale" : {
      "type" : "string",
      "enum" : [ "SHARED", "INDEPENDENT" ]
    },
    "FilterSliderControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlSliderType"
        },
        "StepSize" : {
          "default" : 0,
          "type" : "number"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/SliderControlDisplayOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "MaximumValue" : {
          "default" : 0,
          "type" : "number"
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "MinimumValue" : {
          "default" : 0,
          "type" : "number"
        }
      },
      "required" : [ "FilterControlId", "MaximumValue", "MinimumValue", "SourceFilterId", "StepSize", "Title" ]
    },
    "PivotTableConditionalFormattingOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Cell" : {
          "$ref" : "#/definitions/PivotTableCellConditionalFormatting"
        }
      }
    },
    "DataLabelOverlap" : {
      "type" : "string",
      "enum" : [ "DISABLE_OVERLAP", "ENABLE_OVERLAP" ]
    },
    "ConditionalFormattingIconDisplayConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "IconDisplayOption" : {
          "$ref" : "#/definitions/ConditionalFormattingIconDisplayOption"
        }
      }
    },
    "SelectedFieldOptions" : {
      "type" : "string",
      "enum" : [ "ALL_FIELDS" ]
    },
    "TableFieldLinkConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Target" : {
          "$ref" : "#/definitions/URLTargetConfiguration"
        },
        "Content" : {
          "$ref" : "#/definitions/TableFieldLinkContentConfiguration"
        }
      },
      "required" : [ "Content", "Target" ]
    },
    "GeospatialHeatmapDataColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      },
      "required" : [ "Color" ]
    },
    "LineChartType" : {
      "type" : "string",
      "enum" : [ "LINE", "AREA", "STACKED_AREA" ]
    },
    "DefaultTextFieldControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextFieldControlDisplayOptions"
        }
      }
    },
    "TableTotalsPlacement" : {
      "type" : "string",
      "enum" : [ "START", "END", "AUTO" ]
    },
    "LayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GridLayout" : {
          "$ref" : "#/definitions/GridLayoutConfiguration"
        },
        "FreeFormLayout" : {
          "$ref" : "#/definitions/FreeFormLayoutConfiguration"
        },
        "SectionBasedLayout" : {
          "$ref" : "#/definitions/SectionBasedLayoutConfiguration"
        }
      }
    },
    "ImageStaticFile" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StaticFileId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Source" : {
          "$ref" : "#/definitions/StaticFileSource"
        }
      },
      "required" : [ "StaticFileId" ]
    },
    "PivotFieldSortOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortBy" : {
          "$ref" : "#/definitions/PivotTableSortBy"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FieldId", "SortBy" ]
    },
    "SimpleAttributeAggregationFunction" : {
      "type" : "string",
      "enum" : [ "UNIQUE_VALUE" ]
    },
    "ColorScale" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Colors" : {
          "minItems" : 2,
          "maxItems" : 3,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataColor"
          }
        },
        "ColorFillType" : {
          "$ref" : "#/definitions/ColorFillType"
        },
        "NullValueColor" : {
          "$ref" : "#/definitions/DataColor"
        }
      },
      "required" : [ "ColorFillType", "Colors" ]
    },
    "WordCloudWordOrientation" : {
      "type" : "string",
      "enum" : [ "HORIZONTAL", "HORIZONTAL_AND_VERTICAL" ]
    },
    "GridLayoutCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScreenCanvasSizeOptions" : {
          "$ref" : "#/definitions/GridLayoutScreenCanvasSizeOptions"
        }
      }
    },
    "ValueWhenUnsetOption" : {
      "type" : "string",
      "enum" : [ "RECOMMENDED_VALUE", "NULL" ]
    },
    "CategoryFilterMatchOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "DOES_NOT_EQUAL", "CONTAINS", "DOES_NOT_CONTAIN", "STARTS_WITH", "ENDS_WITH" ]
    },
    "ConditionalFormattingIconDisplayOption" : {
      "type" : "string",
      "enum" : [ "ICON_ONLY" ]
    },
    "GeospatialPolygonStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PolygonSymbolStyle" : {
          "$ref" : "#/definitions/GeospatialPolygonSymbolStyle"
        }
      }
    },
    "KPIProgressBarConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ForegroundColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        }
      }
    },
    "WaterfallChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Categories" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Breakdowns" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "MissingDataConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TreatmentOption" : {
          "$ref" : "#/definitions/MissingDataTreatmentOption"
        }
      }
    },
    "TableCellImageScalingConfiguration" : {
      "type" : "string",
      "enum" : [ "FIT_TO_CELL_HEIGHT", "FIT_TO_CELL_WIDTH", "DO_NOT_SCALE" ]
    },
    "HeatMapSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HeatMapRowSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "HeatMapRowItemsLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "HeatMapColumnItemsLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "HeatMapColumnSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "ColumnSchema" : {
      "description" : "<p>The column schema.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataType" : {
          "description" : "<p>The data type of the column schema.</p>",
          "type" : "string"
        },
        "GeographicRole" : {
          "description" : "<p>The geographic role of the column schema.</p>",
          "type" : "string"
        },
        "Name" : {
          "description" : "<p>The name of the column schema.</p>",
          "type" : "string"
        }
      }
    },
    "CategoricalAggregationFunction" : {
      "type" : "string",
      "enum" : [ "COUNT", "DISTINCT_COUNT" ]
    },
    "GeospatialMapFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GeospatialMapAggregatedFieldWells" : {
          "$ref" : "#/definitions/GeospatialMapAggregatedFieldWells"
        }
      }
    },
    "SelectedSheetsFilterScopeConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SheetVisualScopingConfigurations" : {
          "minItems" : 1,
          "maxItems" : 50,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetVisualScopingConfiguration"
          }
        }
      }
    },
    "PieChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SmallMultiplesSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "SmallMultiplesLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "FunnelChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/FunnelChartSortConfiguration"
        },
        "DataLabelOptions" : {
          "$ref" : "#/definitions/FunnelChartDataLabelOptions"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/FunnelChartFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "ValueLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "PluginVisualConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/PluginVisualSortConfiguration"
        },
        "VisualOptions" : {
          "$ref" : "#/definitions/PluginVisualOptions"
        },
        "FieldWells" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PluginVisualFieldWell"
          }
        }
      }
    },
    "FilterCrossSheetControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "CascadingControlConfiguration" : {
          "$ref" : "#/definitions/CascadingControlConfiguration"
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId" ]
    },
    "TotalAggregationFunction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SimpleTotalAggregationFunction" : {
          "$ref" : "#/definitions/SimpleTotalAggregationFunction"
        }
      }
    },
    "GaugeChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/GaugeChartFieldWells"
        },
        "TooltipOptions" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "GaugeChartOptions" : {
          "$ref" : "#/definitions/GaugeChartOptions"
        },
        "ColorConfiguration" : {
          "$ref" : "#/definitions/GaugeChartColorConfiguration"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "NumericalAggregationFunction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PercentileAggregation" : {
          "$ref" : "#/definitions/PercentileAggregation"
        },
        "SimpleNumericalAggregation" : {
          "$ref" : "#/definitions/SimpleNumericalAggregationFunction"
        }
      }
    },
    "CustomActionNavigationOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LocalNavigationConfiguration" : {
          "$ref" : "#/definitions/LocalNavigationConfiguration"
        }
      }
    },
    "GeospatialPointStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CircleSymbolStyle" : { }
      }
    },
    "HorizontalTextAlignment" : {
      "type" : "string",
      "enum" : [ "LEFT", "CENTER", "RIGHT", "AUTO" ]
    },
    "LayerCustomActionOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NavigationOperation" : {
          "$ref" : "#/definitions/CustomActionNavigationOperation"
        },
        "SetParametersOperation" : {
          "$ref" : "#/definitions/CustomActionSetParametersOperation"
        },
        "FilterOperation" : {
          "$ref" : "#/definitions/CustomActionFilterOperation"
        },
        "URLOperation" : {
          "$ref" : "#/definitions/CustomActionURLOperation"
        }
      }
    },
    "DecimalPlacesConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DecimalPlaces" : {
          "maximum" : 20,
          "type" : "number",
          "minimum" : 0
        }
      },
      "required" : [ "DecimalPlaces" ]
    },
    "SectionBasedLayoutPaperCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PaperMargin" : {
          "$ref" : "#/definitions/Spacing"
        },
        "PaperSize" : {
          "$ref" : "#/definitions/PaperSize"
        },
        "PaperOrientation" : {
          "$ref" : "#/definitions/PaperOrientation"
        }
      }
    },
    "FilledMapConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ConditionalFormattingOptions" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FilledMapConditionalFormattingOption"
          }
        }
      },
      "required" : [ "ConditionalFormattingOptions" ]
    },
    "BarChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SmallMultiplesSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "ColorSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "ColorItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "SmallMultiplesLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "SheetElementConfigurationOverrides" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "DonutCenterOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LabelVisibility" : { }
      }
    },
    "BodySectionContent" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Layout" : {
          "$ref" : "#/definitions/SectionLayoutConfiguration"
        }
      }
    },
    "TableRowConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "BackgroundColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        }
      }
    },
    "CategoryInnerFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Configuration" : {
          "$ref" : "#/definitions/CategoryFilterConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        }
      },
      "required" : [ "Column", "Configuration" ]
    },
    "PivotTableCellConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Scope" : {
          "$ref" : "#/definitions/PivotTableConditionalFormattingScope"
        },
        "Scopes" : {
          "minItems" : 0,
          "maxItems" : 3,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableConditionalFormattingScope"
          }
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "TextFormat" : {
          "$ref" : "#/definitions/TextConditionalFormat"
        }
      },
      "required" : [ "FieldId" ]
    },
    "ColumnGroupColumnSchema" : {
      "description" : "<p>A structure describing the name, data type, and geographic role of the columns.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Name" : {
          "description" : "<p>The name of the column group's column schema.</p>",
          "type" : "string"
        }
      }
    },
    "ListControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "SearchOptions" : {
          "$ref" : "#/definitions/ListControlSearchOptions"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/ListControlSelectAllOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        }
      }
    },
    "ScatterPlotUnaggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Size" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Label" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "XAxis" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "YAxis" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "PieChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "SmallMultiples" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "LineChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/LineChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "ScatterPlotFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScatterPlotUnaggregatedFieldWells" : {
          "$ref" : "#/definitions/ScatterPlotUnaggregatedFieldWells"
        },
        "ScatterPlotCategoricallyAggregatedFieldWells" : {
          "$ref" : "#/definitions/ScatterPlotCategoricallyAggregatedFieldWells"
        }
      }
    },
    "FontStyle" : {
      "type" : "string",
      "enum" : [ "NORMAL", "ITALIC" ]
    },
    "BarChartOrientation" : {
      "type" : "string",
      "enum" : [ "HORIZONTAL", "VERTICAL" ]
    },
    "DataColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataValue" : {
          "default" : None,
          "type" : "number"
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "SetParameterValueConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DestinationParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Value" : {
          "$ref" : "#/definitions/DestinationParameterValueConfiguration"
        }
      },
      "required" : [ "DestinationParameterName", "Value" ]
    },
    "KPISparklineType" : {
      "type" : "string",
      "enum" : [ "LINE", "AREA" ]
    },
    "TemplateVersion" : {
      "description" : "<p>A version of a template.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/ResourceStatus"
        },
        "Errors" : {
          "minItems" : 1,
          "description" : "<p>Errors associated with this template version.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TemplateError"
          }
        },
        "CreatedTime" : {
          "format" : "date-time",
          "description" : "<p>The time that this template version was created.</p>",
          "type" : "string"
        },
        "Description" : {
          "minLength" : 1,
          "description" : "<p>The description of the template.</p>",
          "type" : "string",
          "maxLength" : 512
        },
        "ThemeArn" : {
          "description" : "<p>The ARN of the theme associated with this version of the template.</p>",
          "type" : "string"
        },
        "DataSetConfigurations" : {
          "minItems" : 0,
          "maxItems" : 30,
          "description" : "<p>Schema of the dataset identified by the placeholder. Any dashboard created from this\n            template should be bound to new datasets matching the same schema described through this\n            API operation.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataSetConfiguration"
          }
        },
        "SourceEntityArn" : {
          "description" : "<p>The Amazon Resource Name (ARN) of an analysis or template that was used to create this\n            template.</p>",
          "type" : "string"
        },
        "VersionNumber" : {
          "description" : "<p>The version number of the template version.</p>",
          "type" : "number",
          "minimum" : 1
        },
        "Sheets" : {
          "minItems" : 0,
          "maxItems" : 20,
          "description" : "<p>A list of the associated sheets with the unique identifier and name of each sheet.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Sheet"
          }
        }
      }
    },
    "BoxPlotChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/BoxPlotSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "ReferenceLines" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ReferenceLine"
          }
        },
        "CategoryAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "PrimaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/BoxPlotFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "BoxPlotOptions" : {
          "$ref" : "#/definitions/BoxPlotOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "PrimaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "ScatterPlotSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScatterPlotLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "TimeRangeDrillDownFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "RangeMinimum" : {
          "format" : "date-time",
          "type" : "string"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "RangeMaximum" : {
          "format" : "date-time",
          "type" : "string"
        }
      },
      "required" : [ "Column", "RangeMaximum", "RangeMinimum", "TimeGranularity" ]
    },
    "DataFieldSeriesItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "AxisBinding" : {
          "$ref" : "#/definitions/AxisBinding"
        },
        "FieldValue" : {
          "type" : "string"
        },
        "Settings" : {
          "$ref" : "#/definitions/LineChartSeriesSettings"
        }
      },
      "required" : [ "AxisBinding", "FieldId" ]
    },
    "BinWidthOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BinCountLimit" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 0
        },
        "Value" : {
          "type" : "number",
          "minimum" : 0
        }
      }
    },
    "CascadingControlSource" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SourceSheetControlId" : {
          "type" : "string"
        },
        "ColumnToMatch" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        }
      }
    },
    "TableOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HeaderStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "CellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "Orientation" : {
          "$ref" : "#/definitions/TableOrientation"
        },
        "RowAlternateColorOptions" : {
          "$ref" : "#/definitions/RowAlternateColorOptions"
        }
      }
    },
    "ColumnConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Role" : {
          "$ref" : "#/definitions/ColumnRole"
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/FormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "ColorsConfiguration" : {
          "$ref" : "#/definitions/ColorsConfiguration"
        }
      },
      "required" : [ "Column" ]
    },
    "ListControlSelectAllOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "NumericFilterSelectAllOptions" : {
      "type" : "string",
      "enum" : [ "FILTER_ALL_VALUES" ]
    },
    "TableFieldIconSetType" : {
      "type" : "string",
      "enum" : [ "LINK" ]
    },
    "ProgressBarOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "SheetControlLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GridLayout" : {
          "$ref" : "#/definitions/GridLayoutConfiguration"
        }
      }
    },
    "YAxisOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "YAxis" : {
          "$ref" : "#/definitions/SingleYAxisOption"
        }
      },
      "required" : [ "YAxis" ]
    },
    "ResourcePermission" : {
      "description" : "<p>Permission for the resource.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Actions" : {
          "minItems" : 1,
          "maxItems" : 20,
          "description" : "<p>The IAM action to grant or revoke permissions on.</p>",
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "Principal" : {
          "minLength" : 1,
          "description" : "<p>The Amazon Resource Name (ARN) of the principal. This can be one of the\n            following:</p>\n         <ul>\n            <li>\n               <p>The ARN of an Amazon QuickSight user or group associated with a data source or dataset. (This is common.)</p>\n            </li>\n            <li>\n               <p>The ARN of an Amazon QuickSight user, group, or namespace associated with an analysis, dashboard, template, or theme. (This is common.)</p>\n            </li>\n            <li>\n               <p>The ARN of an Amazon Web Services account root: This is an IAM ARN rather than a QuickSight\n                    ARN. Use this option only to share resources (templates) across Amazon Web Services accounts.\n                    (This is less common.) </p>\n            </li>\n         </ul>",
          "type" : "string",
          "maxLength" : 256
        }
      },
      "required" : [ "Actions", "Principal" ]
    },
    "SubtotalOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "type" : "string"
        },
        "FieldLevelOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableFieldSubtotalOptions"
          }
        },
        "ValueCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "TotalCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "TotalsVisibility" : { },
        "FieldLevel" : {
          "$ref" : "#/definitions/PivotTableSubtotalLevel"
        },
        "MetricHeaderCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "StyleTargets" : {
          "minItems" : 0,
          "maxItems" : 3,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TableStyleTarget"
          }
        }
      }
    },
    "PivotTablePaginatedReportOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "OverflowColumnHeaderVisibility" : { },
        "VerticalOverflowVisibility" : { }
      }
    },
    "TableOrientation" : {
      "type" : "string",
      "enum" : [ "VERTICAL", "HORIZONTAL" ]
    },
    "ClusterMarker" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SimpleClusterMarker" : {
          "$ref" : "#/definitions/SimpleClusterMarker"
        }
      }
    },
    "FunnelChartMeasureDataLabelStyle" : {
      "type" : "string",
      "enum" : [ "VALUE_ONLY", "PERCENTAGE_BY_FIRST_STAGE", "PERCENTAGE_BY_PREVIOUS_STAGE", "VALUE_AND_PERCENTAGE_BY_FIRST_STAGE", "VALUE_AND_PERCENTAGE_BY_PREVIOUS_STAGE" ]
    },
    "ParameterValueType" : {
      "type" : "string",
      "enum" : [ "MULTI_VALUED", "SINGLE_VALUED" ]
    },
    "ParameterSelectableValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LinkToDataSetColumn" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "SectionLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FreeFormLayout" : {
          "$ref" : "#/definitions/FreeFormSectionLayoutConfiguration"
        }
      },
      "required" : [ "FreeFormLayout" ]
    },
    "SheetControlLayout" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Configuration" : {
          "$ref" : "#/definitions/SheetControlLayoutConfiguration"
        }
      },
      "required" : [ "Configuration" ]
    },
    "FontWeightName" : {
      "type" : "string",
      "enum" : [ "NORMAL", "BOLD" ]
    },
    "HeatMapFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HeatMapAggregatedFieldWells" : {
          "$ref" : "#/definitions/HeatMapAggregatedFieldWells"
        }
      }
    },
    "PercentVisibleRange" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "From" : {
          "default" : None,
          "maximum" : 100,
          "type" : "number",
          "minimum" : 0
        },
        "To" : {
          "default" : None,
          "maximum" : 100,
          "type" : "number",
          "minimum" : 0
        }
      }
    },
    "PivotTableMetricPlacement" : {
      "type" : "string",
      "enum" : [ "ROW", "COLUMN" ]
    },
    "Computation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PeriodToDate" : {
          "$ref" : "#/definitions/PeriodToDateComputation"
        },
        "GrowthRate" : {
          "$ref" : "#/definitions/GrowthRateComputation"
        },
        "TopBottomRanked" : {
          "$ref" : "#/definitions/TopBottomRankedComputation"
        },
        "TotalAggregation" : {
          "$ref" : "#/definitions/TotalAggregationComputation"
        },
        "Forecast" : {
          "$ref" : "#/definitions/ForecastComputation"
        },
        "MaximumMinimum" : {
          "$ref" : "#/definitions/MaximumMinimumComputation"
        },
        "PeriodOverPeriod" : {
          "$ref" : "#/definitions/PeriodOverPeriodComputation"
        },
        "MetricComparison" : {
          "$ref" : "#/definitions/MetricComparisonComputation"
        },
        "TopBottomMovers" : {
          "$ref" : "#/definitions/TopBottomMoversComputation"
        },
        "UniqueValues" : {
          "$ref" : "#/definitions/UniqueValuesComputation"
        }
      }
    },
    "GeospatialPolygonLayer" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Style" : {
          "$ref" : "#/definitions/GeospatialPolygonStyle"
        }
      },
      "required" : [ "Style" ]
    },
    "RelativeFontSize" : {
      "type" : "string",
      "enum" : [ "EXTRA_SMALL", "SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE" ]
    },
    "CascadingControlConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SourceControls" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/CascadingControlSource"
          }
        }
      }
    },
    "StaticFileSource" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "UrlOptions" : {
          "$ref" : "#/definitions/StaticFileUrlSourceOptions"
        },
        "S3Options" : {
          "$ref" : "#/definitions/StaticFileS3SourceOptions"
        }
      }
    },
    "LineChartLineStyle" : {
      "type" : "string",
      "enum" : [ "SOLID", "DOTTED", "DASHED" ]
    },
    "Visibility" : {
      "type" : "string",
      "enum" : [ "HIDDEN", "VISIBLE" ]
    },
    "VisualMenuOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AvailabilityStatus" : {
          "$ref" : "#/definitions/DashboardBehavior"
        }
      }
    },
    "ComparisonMethod" : {
      "type" : "string",
      "enum" : [ "DIFFERENCE", "PERCENT_DIFFERENCE", "PERCENT" ]
    },
    "CustomColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "FieldValue" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 2048
        },
        "SpecialValue" : {
          "$ref" : "#/definitions/SpecialValue"
        }
      },
      "required" : [ "Color" ]
    },
    "SingleYAxisOption" : {
      "type" : "string",
      "enum" : [ "PRIMARY_Y_AXIS" ]
    },
    "SpecialValue" : {
      "type" : "string",
      "enum" : [ "EMPTY", "NULL", "OTHER" ]
    },
    "DefaultSliderControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/SheetControlSliderType"
        },
        "StepSize" : {
          "default" : 0,
          "type" : "number"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/SliderControlDisplayOptions"
        },
        "MaximumValue" : {
          "default" : 0,
          "type" : "number"
        },
        "MinimumValue" : {
          "default" : 0,
          "type" : "number"
        }
      },
      "required" : [ "MaximumValue", "MinimumValue", "StepSize" ]
    },
    "WaterfallChartColorConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupColorConfiguration" : {
          "$ref" : "#/definitions/WaterfallChartGroupColorConfiguration"
        }
      }
    },
    "ParameterListControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/ListControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "CascadingControlConfiguration" : {
          "$ref" : "#/definitions/CascadingControlConfiguration"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/ParameterSelectableValues"
        }
      },
      "required" : [ "ParameterControlId", "SourceParameterName", "Title" ]
    },
    "PluginVisualTableQuerySort" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ItemsLimitConfiguration" : {
          "$ref" : "#/definitions/PluginVisualItemsLimitConfiguration"
        },
        "RowSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "ParameterDateTimePickerControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DateTimePickerControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "ParameterControlId", "SourceParameterName", "Title" ]
    },
    "PluginVisualAxisName" : {
      "type" : "string",
      "enum" : [ "GROUP_BY", "VALUE" ]
    },
    "TreeMapSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TreeMapSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "TreeMapGroupItemsLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "DataSetSchema" : {
      "description" : "<p>Dataset schema.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColumnSchemaList" : {
          "minItems" : 0,
          "maxItems" : 500,
          "description" : "<p>A structure containing the list of column schemas.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnSchema"
          }
        }
      }
    },
    "LineChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LineChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/LineChartAggregatedFieldWells"
        }
      }
    },
    "RadarChartSeriesSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AreaStyleSettings" : {
          "$ref" : "#/definitions/RadarChartAreaStyleSettings"
        }
      }
    },
    "NumberScale" : {
      "type" : "string",
      "enum" : [ "NONE", "AUTO", "THOUSANDS", "MILLIONS", "BILLIONS", "TRILLIONS", "LAKHS", "CRORES" ]
    },
    "BoxPlotSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "PaginationConfiguration" : {
          "$ref" : "#/definitions/PaginationConfiguration"
        }
      }
    },
    "ImageMenuOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AvailabilityStatus" : {
          "$ref" : "#/definitions/DashboardBehavior"
        }
      }
    },
    "CategoryDrillDownFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "CategoryValues" : {
          "minItems" : 0,
          "maxItems" : 100000,
          "type" : "array",
          "items" : {
            "minLength" : 0,
            "type" : "string",
            "maxLength" : 512
          }
        }
      },
      "required" : [ "CategoryValues", "Column" ]
    },
    "PivotTableFieldCollapseStateOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Target" : {
          "$ref" : "#/definitions/PivotTableFieldCollapseStateTarget"
        },
        "State" : {
          "$ref" : "#/definitions/PivotTableFieldCollapseState"
        }
      },
      "required" : [ "Target" ]
    },
    "DashboardBehavior" : {
      "type" : "string",
      "enum" : [ "ENABLED", "DISABLED" ]
    },
    "GridLayoutScreenCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "OptimizedViewPortWidth" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "ResizeOption" : {
          "$ref" : "#/definitions/ResizeOption"
        }
      },
      "required" : [ "ResizeOption" ]
    },
    "SankeyDiagramChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/SankeyDiagramSortConfiguration"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/SankeyDiagramFieldWells"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "WordCloudVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/WordCloudChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "FilterListConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryValues" : {
          "minItems" : 0,
          "maxItems" : 100000,
          "type" : "array",
          "items" : {
            "minLength" : 0,
            "type" : "string",
            "maxLength" : 512
          }
        },
        "NullOption" : {
          "$ref" : "#/definitions/FilterNullOption"
        },
        "MatchOperator" : {
          "$ref" : "#/definitions/CategoryFilterMatchOperator"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/CategoryFilterSelectAllOptions"
        }
      },
      "required" : [ "MatchOperator" ]
    },
    "SankeyDiagramVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/SankeyDiagramChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "VisualId" ]
    },
    "TopBottomComputationType" : {
      "type" : "string",
      "enum" : [ "TOP", "BOTTOM" ]
    },
    "ForecastConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ForecastProperties" : {
          "$ref" : "#/definitions/TimeBasedForecastProperties"
        },
        "Scenario" : {
          "$ref" : "#/definitions/ForecastScenario"
        }
      }
    },
    "SimpleTotalAggregationFunction" : {
      "type" : "string",
      "enum" : [ "DEFAULT", "SUM", "AVERAGE", "MIN", "MAX", "NONE" ]
    },
    "ConditionalFormattingSolidColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      },
      "required" : [ "Expression" ]
    },
    "WaterfallChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WaterfallChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/WaterfallChartAggregatedFieldWells"
        }
      }
    },
    "GeospatialHeatmapColorScale" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Colors" : {
          "minItems" : 2,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/GeospatialHeatmapDataColor"
          }
        }
      }
    },
    "DefaultFreeFormLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/FreeFormLayoutCanvasSizeOptions"
        }
      },
      "required" : [ "CanvasSizeOptions" ]
    },
    "FilledMapShapeConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Format" : {
          "$ref" : "#/definitions/ShapeConditionalFormat"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FieldId" ]
    },
    "InsightConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Computations" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Computation"
          }
        },
        "CustomNarrative" : {
          "$ref" : "#/definitions/CustomNarrativeOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "ReferenceLineStyleConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Pattern" : {
          "$ref" : "#/definitions/ReferenceLinePatternType"
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "ResizeOption" : {
      "type" : "string",
      "enum" : [ "FIXED", "RESPONSIVE" ]
    },
    "FunnelChartDataLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MeasureLabelVisibility" : { },
        "Position" : {
          "$ref" : "#/definitions/DataLabelPosition"
        },
        "Visibility" : { },
        "CategoryLabelVisibility" : { },
        "LabelColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "MeasureDataLabelStyle" : {
          "$ref" : "#/definitions/FunnelChartMeasureDataLabelStyle"
        },
        "LabelFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      }
    },
    "NumericEqualityMatchOperator" : {
      "type" : "string",
      "enum" : [ "EQUALS", "DOES_NOT_EQUAL" ]
    },
    "SecondaryValueOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "HeaderFooterSectionConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Layout" : {
          "$ref" : "#/definitions/SectionLayoutConfiguration"
        },
        "Style" : {
          "$ref" : "#/definitions/SectionStyle"
        },
        "SectionId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Layout", "SectionId" ]
    },
    "BodySectionRepeatPageBreakConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "After" : {
          "$ref" : "#/definitions/SectionAfterPageBreak"
        }
      }
    },
    "HeatMapConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/HeatMapSortConfiguration"
        },
        "ColumnLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/HeatMapFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "ColorScale" : {
          "$ref" : "#/definitions/ColorScale"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "RowLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        }
      }
    },
    "TransposedColumnType" : {
      "type" : "string",
      "enum" : [ "ROW_HEADER_COLUMN", "VALUE_COLUMN" ]
    },
    "FilterListControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/ListControlDisplayOptions"
        },
        "CascadingControlConfiguration" : {
          "$ref" : "#/definitions/CascadingControlConfiguration"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/FilterSelectableValues"
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "PeriodOverPeriodComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "Sheet" : {
      "description" : "<p>A <i>sheet</i>, which is an object that contains a set of visuals that\n            are viewed together on one page in Amazon QuickSight. Every analysis and dashboard\n            contains at least one sheet. Each sheet contains at least one visualization widget, for\n            example a chart, pivot table, or narrative insight. Sheets can be associated with other\n            components, such as controls, filters, and so on.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SheetId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "description" : "<p>The unique identifier associated with a sheet.</p>",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "minLength" : 1,
          "description" : "<p>The name of a sheet. This name is displayed on the sheet's tab in the Amazon QuickSight\n            console.</p>",
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "ArcOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ArcThickness" : {
          "$ref" : "#/definitions/ArcThickness"
        }
      }
    },
    "DefaultSectionBasedLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/SectionBasedLayoutCanvasSizeOptions"
        }
      },
      "required" : [ "CanvasSizeOptions" ]
    },
    "SectionStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Padding" : {
          "$ref" : "#/definitions/Spacing"
        },
        "Height" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      }
    },
    "BarChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BarChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/BarChartAggregatedFieldWells"
        }
      }
    },
    "GeospatialMapAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Colors" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Geospatial" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "GeospatialNullDataSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SymbolStyle" : {
          "$ref" : "#/definitions/GeospatialNullSymbolStyle"
        }
      },
      "required" : [ "SymbolStyle" ]
    },
    "SingleAxisOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "YAxisOptions" : {
          "$ref" : "#/definitions/YAxisOptions"
        }
      }
    },
    "DateMeasureField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/DateAggregationFunction"
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/DateTimeFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "GaugeChartColorConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ForegroundColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "BackgroundColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "TooltipTitleType" : {
      "type" : "string",
      "enum" : [ "NONE", "PRIMARY_VALUE" ]
    },
    "GeospatialMapVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/GeospatialMapConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "DefaultPaginatedLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SectionBased" : {
          "$ref" : "#/definitions/DefaultSectionBasedLayoutConfiguration"
        }
      }
    },
    "ChartAxisLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "SortIconVisibility" : { },
        "AxisLabelOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AxisLabelOptions"
          }
        }
      }
    },
    "PivotTableRowsLayout" : {
      "type" : "string",
      "enum" : [ "TABULAR", "HIERARCHY" ]
    },
    "WaterfallChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "SortConfiguration" : {
          "$ref" : "#/definitions/WaterfallChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "PrimaryYAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/WaterfallChartFieldWells"
        },
        "WaterfallChartOptions" : {
          "$ref" : "#/definitions/WaterfallChartOptions"
        },
        "ColorConfiguration" : {
          "$ref" : "#/definitions/WaterfallChartColorConfiguration"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "CategoryAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "PrimaryYAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "WhatIfPointScenario" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "default" : 0,
          "type" : "number"
        },
        "Date" : {
          "format" : "date-time",
          "type" : "string"
        }
      },
      "required" : [ "Date", "Value" ]
    },
    "AnalysisDefaults" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DefaultNewSheetConfiguration" : {
          "$ref" : "#/definitions/DefaultNewSheetConfiguration"
        }
      },
      "required" : [ "DefaultNewSheetConfiguration" ]
    },
    "NumericalDimensionField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/NumberFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "TableConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/TableSortConfiguration"
        },
        "PaginatedReportOptions" : {
          "$ref" : "#/definitions/TablePaginatedReportOptions"
        },
        "TableOptions" : {
          "$ref" : "#/definitions/TableOptions"
        },
        "TableInlineVisualizations" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TableInlineVisualization"
          }
        },
        "FieldWells" : {
          "$ref" : "#/definitions/TableFieldWells"
        },
        "FieldOptions" : {
          "$ref" : "#/definitions/TableFieldOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "TotalOptions" : {
          "$ref" : "#/definitions/TotalOptions"
        }
      }
    },
    "HistogramConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "YAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "BinOptions" : {
          "$ref" : "#/definitions/HistogramBinOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/HistogramFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "XAxisLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "XAxisDisplayOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        }
      }
    },
    "TreeMapAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Sizes" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Colors" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Groups" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "ConditionalFormattingIcon" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomCondition" : {
          "$ref" : "#/definitions/ConditionalFormattingCustomIconCondition"
        },
        "IconSet" : {
          "$ref" : "#/definitions/ConditionalFormattingIconSet"
        }
      }
    },
    "NumberFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FormatConfiguration" : {
          "$ref" : "#/definitions/NumericFormatConfiguration"
        }
      }
    },
    "LayoutElementType" : {
      "type" : "string",
      "enum" : [ "VISUAL", "FILTER_CONTROL", "PARAMETER_CONTROL", "TEXT_BOX", "IMAGE" ]
    },
    "WaterfallVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/WaterfallChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "DateTimeDefaultValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RollingDate" : {
          "$ref" : "#/definitions/RollingDateConfiguration"
        },
        "DynamicValue" : {
          "$ref" : "#/definitions/DynamicDefaultValue"
        },
        "StaticValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "format" : "date-time",
            "type" : "string"
          }
        }
      }
    },
    "ReferenceLineValueLabelRelativePosition" : {
      "type" : "string",
      "enum" : [ "BEFORE_CUSTOM_LABEL", "AFTER_CUSTOM_LABEL" ]
    },
    "BinCountOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "number",
          "minimum" : 0
        }
      }
    },
    "PivotTableOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RowFieldNamesStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "RowHeaderStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "CollapsedRowDimensionsVisibility" : { },
        "RowsLayout" : {
          "$ref" : "#/definitions/PivotTableRowsLayout"
        },
        "MetricPlacement" : {
          "$ref" : "#/definitions/PivotTableMetricPlacement"
        },
        "DefaultCellWidth" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "ColumnNamesVisibility" : { },
        "RowsLabelOptions" : {
          "$ref" : "#/definitions/PivotTableRowsLabelOptions"
        },
        "SingleMetricVisibility" : { },
        "ColumnHeaderStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "ToggleButtonsVisibility" : { },
        "CellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "RowAlternateColorOptions" : {
          "$ref" : "#/definitions/RowAlternateColorOptions"
        }
      }
    },
    "PeriodToDateComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PeriodTimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "TableAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupBy" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "ReferenceLineStaticDataConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "default" : 0,
          "type" : "number"
        }
      },
      "required" : [ "Value" ]
    },
    "DayOfTheWeek" : {
      "type" : "string",
      "enum" : [ "SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY" ]
    },
    "TopBottomRankedComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/TopBottomComputationType"
        },
        "Category" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ResultSize" : {
          "default" : 0,
          "maximum" : 20,
          "type" : "number",
          "minimum" : 1
        },
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId", "Type" ]
    },
    "BodySectionDynamicNumericDimensionConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "SortByMetrics" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnSort"
          }
        },
        "Limit" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 1
        }
      },
      "required" : [ "Column" ]
    },
    "ParameterSliderControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "StepSize" : {
          "default" : 0,
          "type" : "number"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/SliderControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "MaximumValue" : {
          "default" : 0,
          "type" : "number"
        },
        "MinimumValue" : {
          "default" : 0,
          "type" : "number"
        }
      },
      "required" : [ "MaximumValue", "MinimumValue", "ParameterControlId", "SourceParameterName", "StepSize", "Title" ]
    },
    "NegativeValueDisplayMode" : {
      "type" : "string",
      "enum" : [ "POSITIVE", "NEGATIVE" ]
    },
    "ColorFillType" : {
      "type" : "string",
      "enum" : [ "DISCRETE", "GRADIENT" ]
    },
    "SheetImageStaticFileSource" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StaticFileId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "StaticFileId" ]
    },
    "TableFieldCustomIconContent" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Icon" : {
          "$ref" : "#/definitions/TableFieldIconSetType"
        }
      }
    },
    "TableFieldURLConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LinkConfiguration" : {
          "$ref" : "#/definitions/TableFieldLinkConfiguration"
        },
        "ImageConfiguration" : {
          "$ref" : "#/definitions/TableFieldImageConfiguration"
        }
      }
    },
    "SheetControlInfoIconLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "InfoIconText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 100
        }
      }
    },
    "VisualPalette" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ChartColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "ColorMap" : {
          "minItems" : 0,
          "maxItems" : 5000,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataPathColor"
          }
        }
      }
    },
    "MissingDataTreatmentOption" : {
      "type" : "string",
      "enum" : [ "INTERPOLATE", "SHOW_AS_ZERO", "SHOW_AS_BLANK" ]
    },
    "ReferenceLineLabelVerticalPosition" : {
      "type" : "string",
      "enum" : [ "ABOVE", "BELOW" ]
    },
    "ItemsLimitConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ItemsLimit" : {
          "default" : None,
          "type" : "number"
        },
        "OtherCategories" : {
          "$ref" : "#/definitions/OtherCategories"
        }
      }
    },
    "FilterTextFieldControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextFieldControlDisplayOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "TablePinnedFieldOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PinnedLeftFields" : {
          "minItems" : 0,
          "maxItems" : 201,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "type" : "string",
            "maxLength" : 512
          }
        }
      }
    },
    "OtherCategories" : {
      "type" : "string",
      "enum" : [ "INCLUDE", "EXCLUDE" ]
    },
    "TimeEqualityFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "RollingDate" : {
          "$ref" : "#/definitions/RollingDateConfiguration"
        },
        "Value" : {
          "format" : "date-time",
          "type" : "string"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FilterId" ]
    },
    "NumericFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumberDisplayFormatConfiguration" : {
          "$ref" : "#/definitions/NumberDisplayFormatConfiguration"
        },
        "CurrencyDisplayFormatConfiguration" : {
          "$ref" : "#/definitions/CurrencyDisplayFormatConfiguration"
        },
        "PercentageDisplayFormatConfiguration" : {
          "$ref" : "#/definitions/PercentageDisplayFormatConfiguration"
        }
      }
    },
    "DataPathColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Element" : {
          "$ref" : "#/definitions/DataPathValue"
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        }
      },
      "required" : [ "Color", "Element" ]
    },
    "CustomContentConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ContentUrl" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "ContentType" : {
          "$ref" : "#/definitions/CustomContentType"
        },
        "ImageScaling" : {
          "$ref" : "#/definitions/CustomContentImageScalingConfiguration"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "MapZoomMode" : {
      "type" : "string",
      "enum" : [ "AUTO", "MANUAL" ]
    },
    "SheetControlListType" : {
      "type" : "string",
      "enum" : [ "MULTI_SELECT", "SINGLE_SELECT" ]
    },
    "ArcThicknessOptions" : {
      "type" : "string",
      "enum" : [ "SMALL", "MEDIUM", "LARGE" ]
    },
    "PivotTableDataPathType" : {
      "type" : "string",
      "enum" : [ "HIERARCHY_ROWS_LAYOUT_COLUMN", "MULTIPLE_ROW_METRICS_COLUMN", "EMPTY_COLUMN_HEADER", "COUNT_METRIC_COLUMN" ]
    },
    "RadarChartAxesRangeScale" : {
      "type" : "string",
      "enum" : [ "AUTO", "INDEPENDENT", "SHARED" ]
    },
    "ConditionalFormattingCustomIconCondition" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "DisplayConfiguration" : {
          "$ref" : "#/definitions/ConditionalFormattingIconDisplayConfiguration"
        },
        "IconOptions" : {
          "$ref" : "#/definitions/ConditionalFormattingCustomIconOptions"
        }
      },
      "required" : [ "Expression", "IconOptions" ]
    },
    "FilterTextAreaControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Delimiter" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextAreaControlDisplayOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "BaseMapStyleType" : {
      "type" : "string",
      "enum" : [ "LIGHT_GRAY", "DARK_GRAY", "STREET", "IMAGERY" ]
    },
    "InsightVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "InsightConfiguration" : {
          "$ref" : "#/definitions/InsightConfiguration"
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "DataSetIdentifier", "VisualId" ]
    },
    "TableSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RowSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "PaginationConfiguration" : {
          "$ref" : "#/definitions/PaginationConfiguration"
        }
      }
    },
    "FreeFormLayoutScreenCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "OptimizedViewPortWidth" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      },
      "required" : [ "OptimizedViewPortWidth" ]
    },
    "ContributionAnalysisDefault" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MeasureFieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "ContributorDimensions" : {
          "minItems" : 1,
          "maxItems" : 4,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnIdentifier"
          }
        }
      },
      "required" : [ "ContributorDimensions", "MeasureFieldId" ]
    },
    "GradientColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Stops" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/GradientStop"
          }
        }
      }
    },
    "TableFieldImageConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SizingOptions" : {
          "$ref" : "#/definitions/TableCellImageSizingConfiguration"
        }
      }
    },
    "GaugeChartConditionalFormattingOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Arc" : {
          "$ref" : "#/definitions/GaugeChartArcConditionalFormatting"
        },
        "PrimaryValue" : {
          "$ref" : "#/definitions/GaugeChartPrimaryValueConditionalFormatting"
        }
      }
    },
    "PieChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PieChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/PieChartAggregatedFieldWells"
        }
      }
    },
    "VisualCustomAction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "Trigger" : {
          "$ref" : "#/definitions/VisualCustomActionTrigger"
        },
        "CustomActionId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 256
        },
        "ActionOperations" : {
          "minItems" : 1,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomActionOperation"
          }
        }
      },
      "required" : [ "ActionOperations", "CustomActionId", "Name", "Trigger" ]
    },
    "TopBottomFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationSortConfigurations" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AggregationSortConfiguration"
          }
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Limit" : {
          "default" : None,
          "type" : "number"
        },
        "DefaultFilterControlConfiguration" : {
          "$ref" : "#/definitions/DefaultFilterControlConfiguration"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "AggregationSortConfigurations", "Column", "FilterId" ]
    },
    "KPIConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/KPISortConfiguration"
        },
        "KPIOptions" : {
          "$ref" : "#/definitions/KPIOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/KPIFieldWells"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "PivotTableFieldCollapseState" : {
      "type" : "string",
      "enum" : [ "COLLAPSED", "EXPANDED" ]
    },
    "MinimumLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "CategoryFilterConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomFilterListConfiguration" : {
          "$ref" : "#/definitions/CustomFilterListConfiguration"
        },
        "CustomFilterConfiguration" : {
          "$ref" : "#/definitions/CustomFilterConfiguration"
        },
        "FilterListConfiguration" : {
          "$ref" : "#/definitions/FilterListConfiguration"
        }
      }
    },
    "GeospatialSolidColor" : {
      "description" : "Describes the properties for a solid color",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "State" : { },
        "Color" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        }
      },
      "required" : [ "Color" ]
    },
    "TemplateSourceTemplate" : {
      "description" : "<p>The source template of the template.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Arn" : {
          "description" : "<p>The Amazon Resource Name (ARN) of the resource.</p>",
          "type" : "string"
        }
      },
      "required" : [ "Arn" ]
    },
    "NumericEqualityDrillDownFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "Value" : {
          "default" : 0,
          "type" : "number"
        }
      },
      "required" : [ "Column", "Value" ]
    },
    "TimeGranularity" : {
      "type" : "string",
      "enum" : [ "YEAR", "QUARTER", "MONTH", "WEEK", "DAY", "HOUR", "MINUTE", "SECOND", "MILLISECOND" ]
    },
    "GaugeChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "ConditionalFormatting" : {
          "$ref" : "#/definitions/GaugeChartConditionalFormatting"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/GaugeChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "VisualId" ]
    },
    "FilledMapConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/FilledMapSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "MapStyleOptions" : {
          "$ref" : "#/definitions/GeospatialMapStyleOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/FilledMapFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "WindowOptions" : {
          "$ref" : "#/definitions/GeospatialWindowOptions"
        }
      }
    },
    "VisibleRangeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PercentRange" : {
          "$ref" : "#/definitions/PercentVisibleRange"
        }
      }
    },
    "ForecastComputationSeasonality" : {
      "type" : "string",
      "enum" : [ "AUTOMATIC", "CUSTOM" ]
    },
    "KPIComparisonValueConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "Icon" : {
          "$ref" : "#/definitions/ConditionalFormattingIcon"
        }
      }
    },
    "RangeEndsLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "LegendOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Position" : {
          "$ref" : "#/definitions/LegendPosition"
        },
        "ValueFontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "Title" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "Visibility" : { },
        "Height" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "Width" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        }
      }
    },
    "ShortFormatText" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RichText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "PlainText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      }
    },
    "PieChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/PieChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "ComparisonConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ComparisonMethod" : {
          "$ref" : "#/definitions/ComparisonMethod"
        },
        "ComparisonFormat" : {
          "$ref" : "#/definitions/ComparisonFormatConfiguration"
        }
      }
    },
    "ConditionalFormattingGradientColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "Color" : {
          "$ref" : "#/definitions/GradientColor"
        }
      },
      "required" : [ "Color", "Expression" ]
    },
    "TableFieldCustomTextContent" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      },
      "required" : [ "FontConfiguration" ]
    },
    "ArcConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ArcAngle" : {
          "default" : None,
          "type" : "number"
        },
        "ArcThickness" : {
          "$ref" : "#/definitions/ArcThicknessOptions"
        }
      }
    },
    "LineChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryItemsLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "ColorItemsLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "SmallMultiplesSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "SmallMultiplesLimitConfiguration" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "TotalAggregationComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "DateTimeParameterDeclaration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MappedDataSetParameters" : {
          "minItems" : 0,
          "maxItems" : 150,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MappedDataSetParameter"
          }
        },
        "DefaultValues" : {
          "$ref" : "#/definitions/DateTimeDefaultValues"
        },
        "TimeGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        },
        "ValueWhenUnset" : {
          "$ref" : "#/definitions/DateTimeValueWhenUnsetConfiguration"
        },
        "Name" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "Name" ]
    },
    "ParameterTextAreaControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Delimiter" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextAreaControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "ParameterControlId", "SourceParameterName", "Title" ]
    },
    "TableCellStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "VerticalTextAlignment" : {
          "$ref" : "#/definitions/VerticalTextAlignment"
        },
        "Visibility" : { },
        "Height" : {
          "maximum" : 500,
          "type" : "number",
          "minimum" : 8
        },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        },
        "Border" : {
          "$ref" : "#/definitions/GlobalTableBorderOptions"
        },
        "TextWrap" : {
          "$ref" : "#/definitions/TextWrap"
        },
        "HorizontalTextAlignment" : {
          "$ref" : "#/definitions/HorizontalTextAlignment"
        },
        "BackgroundColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "IntegerValueWhenUnsetConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ValueWhenUnsetOption" : {
          "$ref" : "#/definitions/ValueWhenUnsetOption"
        },
        "CustomValue" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "PaperSize" : {
      "type" : "string",
      "enum" : [ "US_LETTER", "US_LEGAL", "US_TABLOID_LEDGER", "A0", "A1", "A2", "A3", "A4", "A5", "JIS_B4", "JIS_B5" ]
    },
    "ReferenceLine" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "DataConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineDataConfiguration"
        },
        "LabelConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineLabelConfiguration"
        },
        "StyleConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineStyleConfiguration"
        }
      },
      "required" : [ "DataConfiguration" ]
    },
    "HistogramAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "ColumnIdentifier" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColumnName" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 127
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "ColumnName", "DataSetIdentifier" ]
    },
    "PivotTableConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/PivotTableSortConfiguration"
        },
        "PaginatedReportOptions" : {
          "$ref" : "#/definitions/PivotTablePaginatedReportOptions"
        },
        "TableOptions" : {
          "$ref" : "#/definitions/PivotTableOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/PivotTableFieldWells"
        },
        "FieldOptions" : {
          "$ref" : "#/definitions/PivotTableFieldOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "TotalOptions" : {
          "$ref" : "#/definitions/PivotTableTotalOptions"
        }
      }
    },
    "LoadingAnimation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "TotalOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TotalAggregationOptions" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TotalAggregationOption"
          }
        },
        "CustomLabel" : {
          "type" : "string"
        },
        "ScrollStatus" : {
          "$ref" : "#/definitions/TableTotalsScrollStatus"
        },
        "Placement" : {
          "$ref" : "#/definitions/TableTotalsPlacement"
        },
        "TotalCellStyle" : {
          "$ref" : "#/definitions/TableCellStyle"
        },
        "TotalsVisibility" : { }
      }
    },
    "ForecastScenario" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WhatIfRangeScenario" : {
          "$ref" : "#/definitions/WhatIfRangeScenario"
        },
        "WhatIfPointScenario" : {
          "$ref" : "#/definitions/WhatIfPointScenario"
        }
      }
    },
    "RowAlternateColorOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "UsePrimaryBackgroundColor" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "RowAlternateColors" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "pattern" : "^#[A-F0-9]{6}$",
            "type" : "string"
          }
        }
      }
    },
    "DefaultRelativeDateTimeControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DisplayOptions" : {
          "$ref" : "#/definitions/RelativeDateTimeControlDisplayOptions"
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        }
      }
    },
    "SectionPageBreakConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "After" : {
          "$ref" : "#/definitions/SectionAfterPageBreak"
        }
      }
    },
    "SheetContentType" : {
      "type" : "string",
      "enum" : [ "PAGINATED", "INTERACTIVE" ]
    },
    "TextControlPlaceholderOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "DonutOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DonutCenterOptions" : {
          "$ref" : "#/definitions/DonutCenterOptions"
        },
        "ArcOptions" : {
          "$ref" : "#/definitions/ArcOptions"
        }
      }
    },
    "TableInlineVisualization" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataBars" : {
          "$ref" : "#/definitions/DataBarsOptions"
        }
      }
    },
    "CustomActionFilterOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SelectedFieldsConfiguration" : {
          "$ref" : "#/definitions/FilterOperationSelectedFieldsConfiguration"
        },
        "TargetVisualsConfiguration" : {
          "$ref" : "#/definitions/FilterOperationTargetVisualsConfiguration"
        }
      },
      "required" : [ "SelectedFieldsConfiguration", "TargetVisualsConfiguration" ]
    },
    "RadarChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/RadarChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "CalculatedField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 32000
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "Name" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 127
        }
      },
      "required" : [ "DataSetIdentifier", "Expression", "Name" ]
    },
    "ColumnGroupSchema" : {
      "description" : "<p>The column group schema.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColumnGroupColumnSchemaList" : {
          "minItems" : 0,
          "maxItems" : 500,
          "description" : "<p>A structure containing the list of schemas for column group columns.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnGroupColumnSchema"
          }
        },
        "Name" : {
          "description" : "<p>The name of the column group schema.</p>",
          "type" : "string"
        }
      }
    },
    "ValidationStrategyMode" : {
      "type" : "string",
      "enum" : [ "STRICT", "LENIENT" ]
    },
    "WaterfallChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BreakdownItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "ColumnHierarchy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DateTimeHierarchy" : {
          "$ref" : "#/definitions/DateTimeHierarchy"
        },
        "ExplicitHierarchy" : {
          "$ref" : "#/definitions/ExplicitHierarchy"
        },
        "PredefinedHierarchy" : {
          "$ref" : "#/definitions/PredefinedHierarchy"
        }
      }
    },
    "NestedFilter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "InnerFilter" : {
          "$ref" : "#/definitions/InnerFilter"
        },
        "IncludeInnerSet" : {
          "default" : False,
          "type" : "boolean"
        },
        "FilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FilterId", "IncludeInnerSet", "InnerFilter" ]
    },
    "MaximumMinimumComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/MaximumMinimumComputationType"
        },
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId", "Type" ]
    },
    "RadarChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColorSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "ColorItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "GridLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/GridLayoutCanvasSizeOptions"
        },
        "Elements" : {
          "minItems" : 0,
          "maxItems" : 430,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/GridLayoutElement"
          }
        }
      },
      "required" : [ "Elements" ]
    },
    "PluginVisualOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "VisualProperties" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PluginVisualProperty"
          }
        }
      }
    },
    "PluginVisualProperty" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "HistogramBinOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BinWidth" : {
          "$ref" : "#/definitions/BinWidthOptions"
        },
        "StartValue" : {
          "default" : None,
          "type" : "number"
        },
        "SelectedBinType" : {
          "$ref" : "#/definitions/HistogramBinType"
        },
        "BinCount" : {
          "$ref" : "#/definitions/BinCountOptions"
        }
      }
    },
    "TemplateErrorType" : {
      "type" : "string",
      "enum" : [ "SOURCE_NOT_FOUND", "DATA_SET_NOT_FOUND", "INTERNAL_FAILURE", "ACCESS_DENIED" ]
    },
    "TableBorderStyle" : {
      "type" : "string",
      "enum" : [ "NONE", "SOLID" ]
    },
    "PivotTableFieldSubtotalOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      }
    },
    "TimeBasedForecastProperties" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PeriodsBackward" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 0
        },
        "PeriodsForward" : {
          "maximum" : 1000,
          "type" : "number",
          "minimum" : 1
        },
        "PredictionInterval" : {
          "maximum" : 95,
          "type" : "number",
          "minimum" : 50
        },
        "Seasonality" : {
          "maximum" : 180,
          "type" : "number",
          "minimum" : 1
        },
        "UpperBoundary" : {
          "default" : None,
          "type" : "number"
        },
        "LowerBoundary" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "SelectedTooltipType" : {
      "type" : "string",
      "enum" : [ "BASIC", "DETAILED" ]
    },
    "SheetDefinition" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Description" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ParameterControls" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ParameterControl"
          }
        },
        "TextBoxes" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetTextBox"
          }
        },
        "Layouts" : {
          "minItems" : 1,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Layout"
          }
        },
        "ContentType" : {
          "$ref" : "#/definitions/SheetContentType"
        },
        "SheetId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "FilterControls" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FilterControl"
          }
        },
        "Images" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetImage"
          }
        },
        "SheetControlLayouts" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SheetControlLayout"
          }
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "Visuals" : {
          "minItems" : 0,
          "maxItems" : 50,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Visual"
          }
        },
        "Name" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "SheetId" ]
    },
    "Filter" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NestedFilter" : {
          "$ref" : "#/definitions/NestedFilter"
        },
        "NumericEqualityFilter" : {
          "$ref" : "#/definitions/NumericEqualityFilter"
        },
        "NumericRangeFilter" : {
          "$ref" : "#/definitions/NumericRangeFilter"
        },
        "TimeRangeFilter" : {
          "$ref" : "#/definitions/TimeRangeFilter"
        },
        "RelativeDatesFilter" : {
          "$ref" : "#/definitions/RelativeDatesFilter"
        },
        "TopBottomFilter" : {
          "$ref" : "#/definitions/TopBottomFilter"
        },
        "TimeEqualityFilter" : {
          "$ref" : "#/definitions/TimeEqualityFilter"
        },
        "CategoryFilter" : {
          "$ref" : "#/definitions/CategoryFilter"
        }
      }
    },
    "ReferenceLineCustomLabelConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "pattern" : "\\S",
          "type" : "string"
        }
      },
      "required" : [ "CustomLabel" ]
    },
    "KPIFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TargetValues" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "TrendGroups" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        }
      }
    },
    "WordCloudWordCasing" : {
      "type" : "string",
      "enum" : [ "LOWER_CASE", "EXISTING_CASE" ]
    },
    "TemplateError" : {
      "description" : "<p>List of errors that occurred when the template version creation failed.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/TemplateErrorType"
        },
        "Message" : {
          "pattern" : "\\S",
          "description" : "<p>Description of the error type.</p>",
          "type" : "string"
        },
        "ViolatedEntities" : {
          "minItems" : 0,
          "maxItems" : 200,
          "description" : "<p>An error path that shows which entities caused the template error.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Entity"
          }
        }
      }
    },
    "PaginationConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PageSize" : {
          "default" : None,
          "type" : "number"
        },
        "PageNumber" : {
          "type" : "number",
          "minimum" : 0
        }
      },
      "required" : [ "PageNumber", "PageSize" ]
    },
    "ComboChartFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ComboChartAggregatedFieldWells" : {
          "$ref" : "#/definitions/ComboChartAggregatedFieldWells"
        }
      }
    },
    "CrossDatasetTypes" : {
      "type" : "string",
      "enum" : [ "ALL_DATASETS", "SINGLE_DATASET" ]
    },
    "CustomActionSetParametersOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterValueConfigurations" : {
          "minItems" : 1,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SetParameterValueConfiguration"
          }
        }
      },
      "required" : [ "ParameterValueConfigurations" ]
    },
    "TableConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ConditionalFormattingOptions" : {
          "minItems" : 0,
          "maxItems" : 500,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TableConditionalFormattingOption"
          }
        }
      }
    },
    "WhatIfRangeScenario" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StartDate" : {
          "format" : "date-time",
          "type" : "string"
        },
        "Value" : {
          "default" : 0,
          "type" : "number"
        },
        "EndDate" : {
          "format" : "date-time",
          "type" : "string"
        }
      },
      "required" : [ "EndDate", "StartDate", "Value" ]
    },
    "PluginVisualSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PluginVisualTableQuerySort" : {
          "$ref" : "#/definitions/PluginVisualTableQuerySort"
        }
      }
    },
    "CategoricalMeasureField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/CategoricalAggregationFunction"
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/StringFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "ListControlSearchOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { }
      }
    },
    "UniqueValuesComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "SmallMultiplesAxisProperties" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Placement" : {
          "$ref" : "#/definitions/SmallMultiplesAxisPlacement"
        },
        "Scale" : {
          "$ref" : "#/definitions/SmallMultiplesAxisScale"
        }
      }
    },
    "KPIVisualStandardLayoutType" : {
      "type" : "string",
      "enum" : [ "CLASSIC", "VERTICAL" ]
    },
    "LabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "type" : "string"
        },
        "Visibility" : { },
        "FontConfiguration" : {
          "$ref" : "#/definitions/FontConfiguration"
        }
      }
    },
    "UnaggregatedField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FormatConfiguration" : {
          "$ref" : "#/definitions/FormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "BarChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/BarChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "ReferenceLines" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ReferenceLine"
          }
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "ColorLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "SmallMultiplesOptions" : {
          "$ref" : "#/definitions/SmallMultiplesOptions"
        },
        "Orientation" : {
          "$ref" : "#/definitions/BarChartOrientation"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "ValueLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "BarsArrangement" : {
          "$ref" : "#/definitions/BarsArrangement"
        },
        "CategoryAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "ContributionAnalysisDefaults" : {
          "minItems" : 1,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ContributionAnalysisDefault"
          }
        },
        "FieldWells" : {
          "$ref" : "#/definitions/BarChartFieldWells"
        },
        "ValueAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "FieldTooltipItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TooltipTarget" : {
          "$ref" : "#/definitions/TooltipTarget"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Label" : {
          "type" : "string"
        },
        "Visibility" : { }
      },
      "required" : [ "FieldId" ]
    },
    "TableSideBorderOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Left" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "Top" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "InnerHorizontal" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "Right" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "Bottom" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "InnerVertical" : {
          "$ref" : "#/definitions/TableBorderOptions"
        }
      }
    },
    "LineChartMarkerStyleSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MarkerShape" : {
          "$ref" : "#/definitions/LineChartMarkerShape"
        },
        "MarkerSize" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "MarkerVisibility" : { },
        "MarkerColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "ComparisonFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumberDisplayFormatConfiguration" : {
          "$ref" : "#/definitions/NumberDisplayFormatConfiguration"
        },
        "PercentageDisplayFormatConfiguration" : {
          "$ref" : "#/definitions/PercentageDisplayFormatConfiguration"
        }
      }
    },
    "FilterRelativeDateTimeControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FilterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/RelativeDateTimeControlDisplayOptions"
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        },
        "SourceFilterId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FilterControlId", "SourceFilterId", "Title" ]
    },
    "PivotTableConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ConditionalFormattingOptions" : {
          "minItems" : 0,
          "maxItems" : 500,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableConditionalFormattingOption"
          }
        }
      }
    },
    "TableFieldOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Order" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "type" : "string",
            "maxLength" : 512
          }
        },
        "PinnedFieldOptions" : {
          "$ref" : "#/definitions/TablePinnedFieldOptions"
        },
        "TransposedTableOptions" : {
          "minItems" : 0,
          "maxItems" : 10001,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TransposedTableOption"
          }
        },
        "SelectedFieldOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TableFieldOption"
          }
        }
      }
    },
    "ReferenceLineSeriesType" : {
      "type" : "string",
      "enum" : [ "BAR", "LINE" ]
    },
    "ReferenceLineDynamicDataConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "MeasureAggregationFunction" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "Calculation" : {
          "$ref" : "#/definitions/NumericalAggregationFunction"
        }
      },
      "required" : [ "Calculation", "Column" ]
    },
    "SheetTextBox" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SheetTextBoxId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Content" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 150000
        }
      },
      "required" : [ "SheetTextBoxId" ]
    },
    "DateDimensionField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/DateTimeFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "DateGranularity" : {
          "$ref" : "#/definitions/TimeGranularity"
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "DefaultFilterListControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/SheetControlListType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/ListControlDisplayOptions"
        },
        "SelectableValues" : {
          "$ref" : "#/definitions/FilterSelectableValues"
        }
      }
    },
    "PrimaryValueDisplayType" : {
      "type" : "string",
      "enum" : [ "HIDDEN", "COMPARISON", "ACTUAL" ]
    },
    "KPIVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "ConditionalFormatting" : {
          "$ref" : "#/definitions/KPIConditionalFormatting"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/KPIConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "AggregationSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "SortDirection" : {
          "$ref" : "#/definitions/SortDirection"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        }
      },
      "required" : [ "Column", "SortDirection" ]
    },
    "PercentageDisplayFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NegativeValueConfiguration" : {
          "$ref" : "#/definitions/NegativeValueConfiguration"
        },
        "DecimalPlacesConfiguration" : {
          "$ref" : "#/definitions/DecimalPlacesConfiguration"
        },
        "NullValueFormatConfiguration" : {
          "$ref" : "#/definitions/NullValueFormatConfiguration"
        },
        "Suffix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        },
        "SeparatorConfiguration" : {
          "$ref" : "#/definitions/NumericSeparatorConfiguration"
        },
        "Prefix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "TableVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "ConditionalFormatting" : {
          "$ref" : "#/definitions/TableConditionalFormatting"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/TableConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "VisualId" ]
    },
    "ComboChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ColorSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "ColorItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "SheetImage" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ImageCustomAction"
          }
        },
        "SheetImageId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Tooltip" : {
          "$ref" : "#/definitions/SheetImageTooltipConfiguration"
        },
        "Scaling" : {
          "$ref" : "#/definitions/SheetImageScalingConfiguration"
        },
        "Interactions" : {
          "$ref" : "#/definitions/ImageInteractionOptions"
        },
        "Source" : {
          "$ref" : "#/definitions/SheetImageSource"
        },
        "ImageContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "SheetImageId", "Source" ]
    },
    "TextAreaControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "PlaceholderOptions" : {
          "$ref" : "#/definitions/TextControlPlaceholderOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        }
      }
    },
    "DataPathSort" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortPaths" : {
          "minItems" : 0,
          "maxItems" : 20,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataPathValue"
          }
        },
        "Direction" : {
          "$ref" : "#/definitions/SortDirection"
        }
      },
      "required" : [ "Direction", "SortPaths" ]
    },
    "DecimalParameterDeclaration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MappedDataSetParameters" : {
          "minItems" : 0,
          "maxItems" : 150,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MappedDataSetParameter"
          }
        },
        "DefaultValues" : {
          "$ref" : "#/definitions/DecimalDefaultValues"
        },
        "ParameterValueType" : {
          "$ref" : "#/definitions/ParameterValueType"
        },
        "ValueWhenUnset" : {
          "$ref" : "#/definitions/DecimalValueWhenUnsetConfiguration"
        },
        "Name" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "Name", "ParameterValueType" ]
    },
    "FilterVisualScope" : {
      "type" : "string",
      "enum" : [ "ALL_VISUALS", "SELECTED_VISUALS" ]
    },
    "ImageCustomAction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "Trigger" : {
          "$ref" : "#/definitions/ImageCustomActionTrigger"
        },
        "CustomActionId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 256
        },
        "ActionOperations" : {
          "minItems" : 1,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ImageCustomActionOperation"
          }
        }
      },
      "required" : [ "ActionOperations", "CustomActionId", "Name", "Trigger" ]
    },
    "TopBottomMoversComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/TopBottomComputationType"
        },
        "Category" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "Value" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "SortOrder" : {
          "$ref" : "#/definitions/TopBottomSortOrder"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "MoverSize" : {
          "default" : 0,
          "maximum" : 20,
          "type" : "number",
          "minimum" : 1
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId", "Type" ]
    },
    "TextWrap" : {
      "type" : "string",
      "enum" : [ "NONE", "WRAP" ]
    },
    "AnchorOption" : {
      "type" : "string",
      "enum" : [ "NOW" ]
    },
    "FieldSort" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Direction" : {
          "$ref" : "#/definitions/SortDirection"
        }
      },
      "required" : [ "Direction", "FieldId" ]
    },
    "AxisDisplayMinMaxRange" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Minimum" : {
          "default" : None,
          "type" : "number"
        },
        "Maximum" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "SectionPageBreakStatus" : {
      "type" : "string",
      "enum" : [ "ENABLED", "DISABLED" ]
    },
    "AxisLabelReferenceOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "DateAggregationFunction" : {
      "type" : "string",
      "enum" : [ "COUNT", "DISTINCT_COUNT", "MIN", "MAX" ]
    },
    "TopBottomSortOrder" : {
      "type" : "string",
      "enum" : [ "PERCENT_DIFFERENCE", "ABSOLUTE_DIFFERENCE" ]
    },
    "DropDownControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "SelectAllOptions" : {
          "$ref" : "#/definitions/ListControlSelectAllOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        }
      }
    },
    "FieldLabelType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Visibility" : { }
      }
    },
    "SpatialStaticFile" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StaticFileId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Source" : {
          "$ref" : "#/definitions/StaticFileSource"
        }
      },
      "required" : [ "StaticFileId" ]
    },
    "AxisLogarithmicScale" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Base" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "KPISortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TrendGroupSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "GlobalTableBorderOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "UniformBorder" : {
          "$ref" : "#/definitions/TableBorderOptions"
        },
        "SideSpecificBorder" : {
          "$ref" : "#/definitions/TableSideBorderOptions"
        }
      }
    },
    "TableTotalsScrollStatus" : {
      "type" : "string",
      "enum" : [ "PINNED", "SCROLLED" ]
    },
    "StyledCellType" : {
      "type" : "string",
      "enum" : [ "TOTAL", "METRIC_HEADER", "VALUE" ]
    },
    "TotalAggregationOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TotalAggregationFunction" : {
          "$ref" : "#/definitions/TotalAggregationFunction"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "FieldId", "TotalAggregationFunction" ]
    },
    "DataPathValue" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataPathType" : {
          "$ref" : "#/definitions/DataPathType"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "FieldValue" : {
          "minLength" : 0,
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "PivotTableFieldOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomLabel" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "Visibility" : { }
      },
      "required" : [ "FieldId" ]
    },
    "LayerCustomAction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "$ref" : "#/definitions/WidgetStatus"
        },
        "Trigger" : {
          "$ref" : "#/definitions/LayerCustomActionTrigger"
        },
        "CustomActionId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "Name" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 256
        },
        "ActionOperations" : {
          "minItems" : 1,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/LayerCustomActionOperation"
          }
        }
      },
      "required" : [ "ActionOperations", "CustomActionId", "Name", "Trigger" ]
    },
    "SectionBasedLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/SectionBasedLayoutCanvasSizeOptions"
        },
        "FooterSections" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/HeaderFooterSectionConfiguration"
          }
        },
        "BodySections" : {
          "minItems" : 0,
          "maxItems" : 28,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/BodySectionConfiguration"
          }
        },
        "HeaderSections" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/HeaderFooterSectionConfiguration"
          }
        }
      },
      "required" : [ "BodySections", "CanvasSizeOptions", "FooterSections", "HeaderSections" ]
    },
    "ConditionalFormattingColor" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Gradient" : {
          "$ref" : "#/definitions/ConditionalFormattingGradientColor"
        },
        "Solid" : {
          "$ref" : "#/definitions/ConditionalFormattingSolidColor"
        }
      }
    },
    "FreeFormLayoutCanvasSizeOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScreenCanvasSizeOptions" : {
          "$ref" : "#/definitions/FreeFormLayoutScreenCanvasSizeOptions"
        }
      }
    },
    "NumericSeparatorSymbol" : {
      "type" : "string",
      "enum" : [ "COMMA", "DOT", "SPACE" ]
    },
    "QueryExecutionMode" : {
      "type" : "string",
      "enum" : [ "AUTO", "MANUAL" ]
    },
    "TemplateSourceAnalysis" : {
      "description" : "<p>The source analysis of the template.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DataSetReferences" : {
          "minItems" : 1,
          "description" : "<p>A structure containing information about the dataset references used as placeholders\n            in the template.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DataSetReference"
          }
        },
        "Arn" : {
          "description" : "<p>The Amazon Resource Name (ARN) of the resource.</p>",
          "type" : "string"
        }
      },
      "required" : [ "Arn", "DataSetReferences" ]
    },
    "TargetVisualOptions" : {
      "type" : "string",
      "enum" : [ "ALL_VISUALS" ]
    },
    "DecimalValueWhenUnsetConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ValueWhenUnsetOption" : {
          "$ref" : "#/definitions/ValueWhenUnsetOption"
        },
        "CustomValue" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "QueryExecutionOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "QueryExecutionMode" : {
          "$ref" : "#/definitions/QueryExecutionMode"
        }
      }
    },
    "ColumnSort" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "SortBy" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "Direction" : {
          "$ref" : "#/definitions/SortDirection"
        }
      },
      "required" : [ "Direction", "SortBy" ]
    },
    "DefaultDateTimePickerControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/SheetControlDateTimePickerType"
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/DateTimePickerControlDisplayOptions"
        },
        "CommitMode" : {
          "$ref" : "#/definitions/CommitMode"
        }
      }
    },
    "GeospatialPointLayer" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Style" : {
          "$ref" : "#/definitions/GeospatialPointStyle"
        }
      },
      "required" : [ "Style" ]
    },
    "NumericalMeasureField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AggregationFunction" : {
          "$ref" : "#/definitions/NumericalAggregationFunction"
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/NumberFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "PanelBorderStyle" : {
      "type" : "string",
      "enum" : [ "SOLID", "DASHED", "DOTTED" ]
    },
    "Spacing" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Left" : {
          "description" : "String based length that is composed of value and unit",
          "type" : "string"
        },
        "Top" : {
          "description" : "String based length that is composed of value and unit",
          "type" : "string"
        },
        "Right" : {
          "description" : "String based length that is composed of value and unit",
          "type" : "string"
        },
        "Bottom" : {
          "description" : "String based length that is composed of value and unit",
          "type" : "string"
        }
      }
    },
    "KPIVisualStandardLayout" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/KPIVisualStandardLayoutType"
        }
      },
      "required" : [ "Type" ]
    },
    "LineChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Colors" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "SmallMultiples" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "CategoryFilterSelectAllOptions" : {
      "type" : "string",
      "enum" : [ "FILTER_ALL_VALUES" ]
    },
    "CustomActionURLOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "URLTemplate" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "URLTarget" : {
          "$ref" : "#/definitions/URLTargetConfiguration"
        }
      },
      "required" : [ "URLTarget", "URLTemplate" ]
    },
    "FreeFormLayoutConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CanvasSizeOptions" : {
          "$ref" : "#/definitions/FreeFormLayoutCanvasSizeOptions"
        },
        "Elements" : {
          "minItems" : 0,
          "maxItems" : 430,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FreeFormLayoutElement"
          }
        }
      },
      "required" : [ "Elements" ]
    },
    "MetricComparisonComputation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TargetValue" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Time" : {
          "$ref" : "#/definitions/DimensionField"
        },
        "ComputationId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "FromValue" : {
          "$ref" : "#/definitions/MeasureField"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ComputationId" ]
    },
    "TableFieldLinkContentConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomIconContent" : {
          "$ref" : "#/definitions/TableFieldCustomIconContent"
        },
        "CustomTextContent" : {
          "$ref" : "#/definitions/TableFieldCustomTextContent"
        }
      }
    },
    "TextConditionalFormat" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "Icon" : {
          "$ref" : "#/definitions/ConditionalFormattingIcon"
        },
        "BackgroundColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        }
      }
    },
    "PivotTableConditionalFormattingScope" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Role" : {
          "$ref" : "#/definitions/PivotTableConditionalFormattingScopeRole"
        }
      }
    },
    "ImageCustomActionTrigger" : {
      "type" : "string",
      "enum" : [ "CLICK", "MENU" ]
    },
    "ColumnTooltipItem" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Aggregation" : {
          "$ref" : "#/definitions/AggregationFunction"
        },
        "TooltipTarget" : {
          "$ref" : "#/definitions/TooltipTarget"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "Label" : {
          "type" : "string"
        },
        "Visibility" : { }
      },
      "required" : [ "Column" ]
    },
    "PivotTableFieldOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CollapseStateOptions" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableFieldCollapseStateOption"
          }
        },
        "DataPathOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableDataPathOption"
          }
        },
        "SelectedFieldOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PivotTableFieldOption"
          }
        }
      }
    },
    "Tag" : {
      "description" : "<p>The key or keys of the key-value pairs for the resource tag or tags assigned to the\n            resource.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "minLength" : 1,
          "description" : "<p>Tag value.</p>",
          "type" : "string",
          "maxLength" : 256
        },
        "Key" : {
          "minLength" : 1,
          "description" : "<p>Tag key.</p>",
          "type" : "string",
          "maxLength" : 128
        }
      },
      "required" : [ "Key", "Value" ]
    },
    "FilterScopeConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AllSheets" : {
          "$ref" : "#/definitions/AllSheetsFilterScopeConfiguration"
        },
        "SelectedSheets" : {
          "$ref" : "#/definitions/SelectedSheetsFilterScopeConfiguration"
        }
      }
    },
    "AnchorDateConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AnchorOption" : {
          "$ref" : "#/definitions/AnchorOption"
        },
        "ParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        }
      }
    },
    "DestinationParameterValueConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CustomValuesConfiguration" : {
          "$ref" : "#/definitions/CustomValuesConfiguration"
        },
        "SourceParameterName" : {
          "type" : "string"
        },
        "SelectAllValueOptions" : {
          "$ref" : "#/definitions/SelectAllValueOptions"
        },
        "SourceField" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "SourceColumn" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        }
      }
    },
    "FilledMapConditionalFormattingOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Shape" : {
          "$ref" : "#/definitions/FilledMapShapeConditionalFormatting"
        }
      },
      "required" : [ "Shape" ]
    },
    "CategoricalDimensionField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "FormatConfiguration" : {
          "$ref" : "#/definitions/StringFormatConfiguration"
        },
        "Column" : {
          "$ref" : "#/definitions/ColumnIdentifier"
        },
        "FieldId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "Column", "FieldId" ]
    },
    "IntegerDefaultValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DynamicValue" : {
          "$ref" : "#/definitions/DynamicDefaultValue"
        },
        "StaticValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "number"
          }
        }
      }
    },
    "StringFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NumericFormatConfiguration" : {
          "$ref" : "#/definitions/NumericFormatConfiguration"
        },
        "NullValueFormatConfiguration" : {
          "$ref" : "#/definitions/NullValueFormatConfiguration"
        }
      }
    },
    "GeospatialPointStyleOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SelectedPointStyle" : {
          "$ref" : "#/definitions/GeospatialSelectedPointStyle"
        },
        "ClusterMarkerConfiguration" : {
          "$ref" : "#/definitions/ClusterMarkerConfiguration"
        },
        "HeatmapConfiguration" : {
          "$ref" : "#/definitions/GeospatialHeatmapConfiguration"
        }
      }
    },
    "NullValueFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NullString" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      },
      "required" : [ "NullString" ]
    },
    "DefaultFilterControlOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DefaultSliderOptions" : {
          "$ref" : "#/definitions/DefaultSliderControlOptions"
        },
        "DefaultRelativeDateTimeOptions" : {
          "$ref" : "#/definitions/DefaultRelativeDateTimeControlOptions"
        },
        "DefaultTextFieldOptions" : {
          "$ref" : "#/definitions/DefaultTextFieldControlOptions"
        },
        "DefaultTextAreaOptions" : {
          "$ref" : "#/definitions/DefaultTextAreaControlOptions"
        },
        "DefaultDropdownOptions" : {
          "$ref" : "#/definitions/DefaultFilterDropDownControlOptions"
        },
        "DefaultDateTimePickerOptions" : {
          "$ref" : "#/definitions/DefaultDateTimePickerControlOptions"
        },
        "DefaultListOptions" : {
          "$ref" : "#/definitions/DefaultFilterListControlOptions"
        }
      }
    },
    "ExplicitHierarchy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HierarchyId" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 512
        },
        "DrillDownFilters" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DrillDownFilter"
          }
        },
        "Columns" : {
          "minItems" : 2,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnIdentifier"
          }
        }
      },
      "required" : [ "Columns", "HierarchyId" ]
    },
    "StaticFileUrlSourceOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Url" : {
          "type" : "string"
        }
      },
      "required" : [ "Url" ]
    },
    "SheetImageTooltipText" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PlainText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      }
    },
    "TooltipOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SelectedTooltipType" : {
          "$ref" : "#/definitions/SelectedTooltipType"
        },
        "TooltipVisibility" : { },
        "FieldBasedTooltip" : {
          "$ref" : "#/definitions/FieldBasedTooltip"
        }
      }
    },
    "FieldBasedTooltip" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TooltipFields" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TooltipItem"
          }
        },
        "AggregationVisibility" : { },
        "TooltipTitleType" : {
          "$ref" : "#/definitions/TooltipTitleType"
        }
      }
    },
    "FilledMapAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Geospatial" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "BarChartAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Category" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Colors" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Values" : {
          "minItems" : 0,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "SmallMultiples" : {
          "minItems" : 0,
          "maxItems" : 1,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "WordCloudWordScaling" : {
      "type" : "string",
      "enum" : [ "EMPHASIZE", "NORMAL" ]
    },
    "GeospatialSelectedPointStyle" : {
      "type" : "string",
      "enum" : [ "POINT", "CLUSTER", "HEATMAP" ]
    },
    "LayerCustomActionTrigger" : {
      "type" : "string",
      "enum" : [ "DATA_POINT_CLICK", "DATA_POINT_MENU" ]
    },
    "ComboChartVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/ComboChartConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "ConditionalFormattingIconSet" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Expression" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 4096
        },
        "IconSetType" : {
          "$ref" : "#/definitions/ConditionalFormattingIconSetType"
        }
      },
      "required" : [ "Expression" ]
    },
    "AxisTickLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "RotationAngle" : {
          "default" : None,
          "type" : "number"
        },
        "LabelOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        }
      }
    },
    "DimensionField" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DateDimensionField" : {
          "$ref" : "#/definitions/DateDimensionField"
        },
        "NumericalDimensionField" : {
          "$ref" : "#/definitions/NumericalDimensionField"
        },
        "CategoricalDimensionField" : {
          "$ref" : "#/definitions/CategoricalDimensionField"
        }
      }
    },
    "FontDecoration" : {
      "type" : "string",
      "enum" : [ "UNDERLINE", "NONE" ]
    },
    "PivotTableAggregatedFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Values" : {
          "minItems" : 0,
          "maxItems" : 40,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MeasureField"
          }
        },
        "Columns" : {
          "minItems" : 0,
          "maxItems" : 40,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        },
        "Rows" : {
          "minItems" : 0,
          "maxItems" : 40,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/DimensionField"
          }
        }
      }
    },
    "FunnelChartSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CategoryItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "CategorySort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        }
      }
    },
    "ImageCustomActionOperation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NavigationOperation" : {
          "$ref" : "#/definitions/CustomActionNavigationOperation"
        },
        "SetParametersOperation" : {
          "$ref" : "#/definitions/CustomActionSetParametersOperation"
        },
        "URLOperation" : {
          "$ref" : "#/definitions/CustomActionURLOperation"
        }
      }
    },
    "AllSheetsFilterScopeConfiguration" : {
      "additionalProperties" : False,
      "type" : "object"
    },
    "HistogramFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "HistogramAggregatedFieldWells" : {
          "$ref" : "#/definitions/HistogramAggregatedFieldWells"
        }
      }
    },
    "PieChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/PieChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "DataLabels" : {
          "$ref" : "#/definitions/DataLabelOptions"
        },
        "ContributionAnalysisDefaults" : {
          "minItems" : 1,
          "maxItems" : 200,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ContributionAnalysisDefault"
          }
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/PieChartFieldWells"
        },
        "Tooltip" : {
          "$ref" : "#/definitions/TooltipOptions"
        },
        "DonutOptions" : {
          "$ref" : "#/definitions/DonutOptions"
        },
        "SmallMultiplesOptions" : {
          "$ref" : "#/definitions/SmallMultiplesOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "ValueLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        }
      }
    },
    "SheetControlDateTimePickerType" : {
      "type" : "string",
      "enum" : [ "SINGLE_VALUED", "DATE_RANGE" ]
    },
    "ReferenceLineDataConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DynamicConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineDynamicDataConfiguration"
        },
        "AxisBinding" : {
          "$ref" : "#/definitions/AxisBinding"
        },
        "SeriesType" : {
          "$ref" : "#/definitions/ReferenceLineSeriesType"
        },
        "StaticConfiguration" : {
          "$ref" : "#/definitions/ReferenceLineStaticDataConfiguration"
        }
      }
    },
    "CurrencyDisplayFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NegativeValueConfiguration" : {
          "$ref" : "#/definitions/NegativeValueConfiguration"
        },
        "DecimalPlacesConfiguration" : {
          "$ref" : "#/definitions/DecimalPlacesConfiguration"
        },
        "NumberScale" : {
          "$ref" : "#/definitions/NumberScale"
        },
        "NullValueFormatConfiguration" : {
          "$ref" : "#/definitions/NullValueFormatConfiguration"
        },
        "Suffix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        },
        "SeparatorConfiguration" : {
          "$ref" : "#/definitions/NumericSeparatorConfiguration"
        },
        "Symbol" : {
          "pattern" : "^[A-Z]{3}$",
          "type" : "string"
        },
        "Prefix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "SameSheetTargetVisualConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TargetVisualOptions" : {
          "$ref" : "#/definitions/TargetVisualOptions"
        },
        "TargetVisuals" : {
          "minItems" : 1,
          "maxItems" : 50,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "^[\\w\\-]+$",
            "type" : "string",
            "maxLength" : 512
          }
        }
      }
    },
    "SliderControlDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TitleOptions" : {
          "$ref" : "#/definitions/LabelOptions"
        },
        "InfoIconLabelOptions" : {
          "$ref" : "#/definitions/SheetControlInfoIconLabelOptions"
        }
      }
    },
    "GeospatialPolygonSymbolStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FillColor" : { },
        "StrokeWidth" : { },
        "StrokeColor" : { }
      }
    },
    "DataSetConfiguration" : {
      "description" : "<p>Dataset configuration.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Placeholder" : {
          "description" : "<p>Placeholder.</p>",
          "type" : "string"
        },
        "DataSetSchema" : {
          "$ref" : "#/definitions/DataSetSchema"
        },
        "ColumnGroupSchemaList" : {
          "minItems" : 0,
          "maxItems" : 500,
          "description" : "<p>A structure containing the list of column group schemas.</p>",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnGroupSchema"
          }
        }
      }
    },
    "LineSeriesAxisDisplayOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MissingDataConfigurations" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/MissingDataConfiguration"
          }
        },
        "AxisOptions" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        }
      }
    },
    "HeatMapVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/HeatMapConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        },
        "ColumnHierarchies" : {
          "minItems" : 0,
          "maxItems" : 2,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnHierarchy"
          }
        }
      },
      "required" : [ "VisualId" ]
    },
    "SankeyDiagramSortConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WeightSort" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldSortOptions"
          }
        },
        "SourceItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        },
        "DestinationItemsLimit" : {
          "$ref" : "#/definitions/ItemsLimitConfiguration"
        }
      }
    },
    "LocalNavigationConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TargetSheetId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "TargetSheetId" ]
    },
    "DataLabelContent" : {
      "type" : "string",
      "enum" : [ "VALUE", "PERCENT", "VALUE_AND_PERCENT" ]
    },
    "WaterfallChartOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TotalBarLabel" : {
          "type" : "string"
        }
      }
    },
    "SankeyDiagramFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SankeyDiagramAggregatedFieldWells" : {
          "$ref" : "#/definitions/SankeyDiagramAggregatedFieldWells"
        }
      }
    },
    "SmallMultiplesAxisPlacement" : {
      "type" : "string",
      "enum" : [ "OUTSIDE", "INSIDE" ]
    },
    "TableFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TableUnaggregatedFieldWells" : {
          "$ref" : "#/definitions/TableUnaggregatedFieldWells"
        },
        "TableAggregatedFieldWells" : {
          "$ref" : "#/definitions/TableAggregatedFieldWells"
        }
      }
    },
    "RadarChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/RadarChartSortConfiguration"
        },
        "Legend" : {
          "$ref" : "#/definitions/LegendOptions"
        },
        "Shape" : {
          "$ref" : "#/definitions/RadarChartShape"
        },
        "BaseSeriesSettings" : {
          "$ref" : "#/definitions/RadarChartSeriesSettings"
        },
        "ColorLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "AxesRangeScale" : {
          "$ref" : "#/definitions/RadarChartAxesRangeScale"
        },
        "VisualPalette" : {
          "$ref" : "#/definitions/VisualPalette"
        },
        "AlternateBandColorsVisibility" : { },
        "StartAngle" : {
          "maximum" : 360,
          "type" : "number",
          "minimum" : -360
        },
        "CategoryAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/RadarChartFieldWells"
        },
        "ColorAxis" : {
          "$ref" : "#/definitions/AxisDisplayOptions"
        },
        "AlternateBandOddColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        },
        "AlternateBandEvenColor" : {
          "pattern" : "^#[A-F0-9]{6}$",
          "type" : "string"
        }
      }
    },
    "VisualTitleLabelOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Visibility" : { },
        "FormatText" : {
          "$ref" : "#/definitions/ShortFormatText"
        }
      }
    },
    "ParameterTextFieldControl" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ParameterControlId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "DisplayOptions" : {
          "$ref" : "#/definitions/TextFieldControlDisplayOptions"
        },
        "SourceParameterName" : {
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9]+$",
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        }
      },
      "required" : [ "ParameterControlId", "SourceParameterName", "Title" ]
    },
    "URLTargetConfiguration" : {
      "type" : "string",
      "enum" : [ "NEW_TAB", "NEW_WINDOW", "SAME_TAB" ]
    },
    "WordCloudFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WordCloudAggregatedFieldWells" : {
          "$ref" : "#/definitions/WordCloudAggregatedFieldWells"
        }
      }
    },
    "TemplateSourceEntity" : {
      "description" : "<p>The source entity of the template.</p>",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SourceAnalysis" : {
          "$ref" : "#/definitions/TemplateSourceAnalysis"
        },
        "SourceTemplate" : {
          "$ref" : "#/definitions/TemplateSourceTemplate"
        }
      }
    },
    "AggregationFunction" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AttributeAggregationFunction" : {
          "$ref" : "#/definitions/AttributeAggregationFunction"
        },
        "DateAggregationFunction" : {
          "$ref" : "#/definitions/DateAggregationFunction"
        },
        "NumericalAggregationFunction" : {
          "$ref" : "#/definitions/NumericalAggregationFunction"
        },
        "CategoricalAggregationFunction" : {
          "$ref" : "#/definitions/CategoricalAggregationFunction"
        }
      }
    },
    "TableStyleTarget" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CellType" : {
          "$ref" : "#/definitions/StyledCellType"
        }
      },
      "required" : [ "CellType" ]
    },
    "GeospatialWindowOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Bounds" : {
          "$ref" : "#/definitions/GeospatialCoordinateBounds"
        },
        "MapZoomMode" : {
          "$ref" : "#/definitions/MapZoomMode"
        }
      }
    },
    "KPIConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ConditionalFormattingOptions" : {
          "minItems" : 0,
          "maxItems" : 100,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/KPIConditionalFormattingOption"
          }
        }
      }
    },
    "KPIConditionalFormattingOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PrimaryValue" : {
          "$ref" : "#/definitions/KPIPrimaryValueConditionalFormatting"
        },
        "ActualValue" : {
          "$ref" : "#/definitions/KPIActualValueConditionalFormatting"
        },
        "ComparisonValue" : {
          "$ref" : "#/definitions/KPIComparisonValueConditionalFormatting"
        },
        "ProgressBar" : {
          "$ref" : "#/definitions/KPIProgressBarConditionalFormatting"
        }
      }
    },
    "LineChartMarkerShape" : {
      "type" : "string",
      "enum" : [ "CIRCLE", "TRIANGLE", "SQUARE", "DIAMOND", "ROUNDED_SQUARE" ]
    },
    "GeospatialStaticFileSource" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StaticFileId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        }
      },
      "required" : [ "StaticFileId" ]
    },
    "ArcAxisDisplayRange" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "default" : None,
          "type" : "number"
        },
        "Max" : {
          "default" : None,
          "type" : "number"
        }
      }
    },
    "ParameterDeclaration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StringParameterDeclaration" : {
          "$ref" : "#/definitions/StringParameterDeclaration"
        },
        "DateTimeParameterDeclaration" : {
          "$ref" : "#/definitions/DateTimeParameterDeclaration"
        },
        "DecimalParameterDeclaration" : {
          "$ref" : "#/definitions/DecimalParameterDeclaration"
        },
        "IntegerParameterDeclaration" : {
          "$ref" : "#/definitions/IntegerParameterDeclaration"
        }
      }
    },
    "Visual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FunnelChartVisual" : {
          "$ref" : "#/definitions/FunnelChartVisual"
        },
        "BoxPlotVisual" : {
          "$ref" : "#/definitions/BoxPlotVisual"
        },
        "GeospatialMapVisual" : {
          "$ref" : "#/definitions/GeospatialMapVisual"
        },
        "ScatterPlotVisual" : {
          "$ref" : "#/definitions/ScatterPlotVisual"
        },
        "RadarChartVisual" : {
          "$ref" : "#/definitions/RadarChartVisual"
        },
        "ComboChartVisual" : {
          "$ref" : "#/definitions/ComboChartVisual"
        },
        "WordCloudVisual" : {
          "$ref" : "#/definitions/WordCloudVisual"
        },
        "SankeyDiagramVisual" : {
          "$ref" : "#/definitions/SankeyDiagramVisual"
        },
        "GaugeChartVisual" : {
          "$ref" : "#/definitions/GaugeChartVisual"
        },
        "FilledMapVisual" : {
          "$ref" : "#/definitions/FilledMapVisual"
        },
        "WaterfallVisual" : {
          "$ref" : "#/definitions/WaterfallVisual"
        },
        "CustomContentVisual" : {
          "$ref" : "#/definitions/CustomContentVisual"
        },
        "PieChartVisual" : {
          "$ref" : "#/definitions/PieChartVisual"
        },
        "KPIVisual" : {
          "$ref" : "#/definitions/KPIVisual"
        },
        "HistogramVisual" : {
          "$ref" : "#/definitions/HistogramVisual"
        },
        "PluginVisual" : {
          "$ref" : "#/definitions/PluginVisual"
        },
        "TableVisual" : {
          "$ref" : "#/definitions/TableVisual"
        },
        "PivotTableVisual" : {
          "$ref" : "#/definitions/PivotTableVisual"
        },
        "BarChartVisual" : {
          "$ref" : "#/definitions/BarChartVisual"
        },
        "HeatMapVisual" : {
          "$ref" : "#/definitions/HeatMapVisual"
        },
        "TreeMapVisual" : {
          "$ref" : "#/definitions/TreeMapVisual"
        },
        "InsightVisual" : {
          "$ref" : "#/definitions/InsightVisual"
        },
        "LineChartVisual" : {
          "$ref" : "#/definitions/LineChartVisual"
        },
        "EmptyVisual" : {
          "$ref" : "#/definitions/EmptyVisual"
        }
      }
    },
    "WordCloudChartConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SortConfiguration" : {
          "$ref" : "#/definitions/WordCloudSortConfiguration"
        },
        "CategoryLabelOptions" : {
          "$ref" : "#/definitions/ChartAxisLabelOptions"
        },
        "FieldWells" : {
          "$ref" : "#/definitions/WordCloudFieldWells"
        },
        "WordCloudOptions" : {
          "$ref" : "#/definitions/WordCloudOptions"
        },
        "Interactions" : {
          "$ref" : "#/definitions/VisualInteractionOptions"
        }
      }
    },
    "CustomContentVisual" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Subtitle" : {
          "$ref" : "#/definitions/VisualSubtitleLabelOptions"
        },
        "VisualId" : {
          "minLength" : 1,
          "pattern" : "^[\\w\\-]+$",
          "type" : "string",
          "maxLength" : 512
        },
        "ChartConfiguration" : {
          "$ref" : "#/definitions/CustomContentConfiguration"
        },
        "Actions" : {
          "minItems" : 0,
          "maxItems" : 10,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/VisualCustomAction"
          }
        },
        "DataSetIdentifier" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 2048
        },
        "Title" : {
          "$ref" : "#/definitions/VisualTitleLabelOptions"
        },
        "VisualContentAltText" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 1024
        }
      },
      "required" : [ "DataSetIdentifier", "VisualId" ]
    },
    "PanelConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BorderThickness" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "BorderStyle" : {
          "$ref" : "#/definitions/PanelBorderStyle"
        },
        "GutterSpacing" : {
          "description" : "String based length that is composed of value and unit in px",
          "type" : "string"
        },
        "BackgroundVisibility" : { },
        "BorderVisibility" : { },
        "BorderColor" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        },
        "Title" : {
          "$ref" : "#/definitions/PanelTitleOptions"
        },
        "GutterVisibility" : { },
        "BackgroundColor" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        }
      }
    },
    "StaticFileS3SourceOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "BucketName" : {
          "type" : "string"
        },
        "ObjectKey" : {
          "type" : "string"
        },
        "Region" : {
          "type" : "string"
        }
      },
      "required" : [ "BucketName", "ObjectKey", "Region" ]
    },
    "SmallMultiplesOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MaxVisibleRows" : {
          "maximum" : 10,
          "type" : "number",
          "minimum" : 1
        },
        "PanelConfiguration" : {
          "$ref" : "#/definitions/PanelConfiguration"
        },
        "MaxVisibleColumns" : {
          "maximum" : 10,
          "type" : "number",
          "minimum" : 1
        },
        "XAxis" : {
          "$ref" : "#/definitions/SmallMultiplesAxisProperties"
        },
        "YAxis" : {
          "$ref" : "#/definitions/SmallMultiplesAxisProperties"
        }
      }
    },
    "BodySectionRepeatDimensionConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DynamicNumericDimensionConfiguration" : {
          "$ref" : "#/definitions/BodySectionDynamicNumericDimensionConfiguration"
        },
        "DynamicCategoryDimensionConfiguration" : {
          "$ref" : "#/definitions/BodySectionDynamicCategoryDimensionConfiguration"
        }
      }
    },
    "PaperOrientation" : {
      "type" : "string",
      "enum" : [ "PORTRAIT", "LANDSCAPE" ]
    },
    "GeospatialNullSymbolStyle" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "FillColor" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        },
        "StrokeWidth" : {
          "type" : "number",
          "minimum" : 0
        },
        "StrokeColor" : {
          "pattern" : "^#[A-F0-9]{6}(?:[A-F0-9]{2})?$",
          "type" : "string"
        }
      }
    },
    "NumericSeparatorConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DecimalSeparator" : {
          "$ref" : "#/definitions/NumericSeparatorSymbol"
        },
        "ThousandsSeparator" : {
          "$ref" : "#/definitions/ThousandSeparatorOptions"
        }
      }
    },
    "ContextMenuOption" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AvailabilityStatus" : {
          "$ref" : "#/definitions/DashboardBehavior"
        }
      }
    },
    "CustomParameterValues" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DecimalValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "number"
          }
        },
        "IntegerValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "number"
          }
        },
        "StringValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "DateTimeValues" : {
          "minItems" : 0,
          "maxItems" : 50000,
          "type" : "array",
          "items" : {
            "format" : "date-time",
            "type" : "string"
          }
        }
      }
    },
    "SimpleNumericalAggregationFunction" : {
      "type" : "string",
      "enum" : [ "SUM", "AVERAGE", "MIN", "MAX", "COUNT", "DISTINCT_COUNT", "VAR", "VARP", "STDEV", "STDEVP", "MEDIAN" ]
    },
    "BoxPlotOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StyleOptions" : {
          "$ref" : "#/definitions/BoxPlotStyleOptions"
        },
        "OutlierVisibility" : { },
        "AllDataPointsVisibility" : { }
      }
    },
    "KPIPrimaryValueConditionalFormatting" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TextColor" : {
          "$ref" : "#/definitions/ConditionalFormattingColor"
        },
        "Icon" : {
          "$ref" : "#/definitions/ConditionalFormattingIcon"
        }
      }
    },
    "NumberDisplayFormatConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NegativeValueConfiguration" : {
          "$ref" : "#/definitions/NegativeValueConfiguration"
        },
        "DecimalPlacesConfiguration" : {
          "$ref" : "#/definitions/DecimalPlacesConfiguration"
        },
        "NumberScale" : {
          "$ref" : "#/definitions/NumberScale"
        },
        "NullValueFormatConfiguration" : {
          "$ref" : "#/definitions/NullValueFormatConfiguration"
        },
        "Suffix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        },
        "SeparatorConfiguration" : {
          "$ref" : "#/definitions/NumericSeparatorConfiguration"
        },
        "Prefix" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 128
        }
      }
    },
    "VisualInteractionOptions" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ContextMenuOption" : {
          "$ref" : "#/definitions/ContextMenuOption"
        },
        "VisualMenuOption" : {
          "$ref" : "#/definitions/VisualMenuOption"
        }
      }
    },
    "PivotTableFieldWells" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PivotTableAggregatedFieldWells" : {
          "$ref" : "#/definitions/PivotTableAggregatedFieldWells"
        }
      }
    }
  },
  "properties" : {
    "CreatedTime" : {
      "format" : "date-time",
      "description" : "<p>Time when this was created.</p>",
      "type" : "string"
    },
    "VersionDescription" : {
      "minLength" : 1,
      "type" : "string",
      "maxLength" : 512
    },
    "SourceEntity" : {
      "$ref" : "#/definitions/TemplateSourceEntity"
    },
    "Definition" : {
      "$ref" : "#/definitions/TemplateVersionDefinition"
    },
    "LastUpdatedTime" : {
      "format" : "date-time",
      "description" : "<p>Time when this was last updated.</p>",
      "type" : "string"
    },
    "ValidationStrategy" : {
      "$ref" : "#/definitions/ValidationStrategy"
    },
    "Name" : {
      "minLength" : 1,
      "type" : "string",
      "maxLength" : 2048
    },
    "Version" : {
      "$ref" : "#/definitions/TemplateVersion"
    },
    "AwsAccountId" : {
      "minLength" : 12,
      "pattern" : "^[0-9]{12}$",
      "type" : "string",
      "maxLength" : 12
    },
    "Permissions" : {
      "minItems" : 1,
      "maxItems" : 64,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ResourcePermission"
      }
    },
    "Arn" : {
      "description" : "<p>The Amazon Resource Name (ARN) of the template.</p>",
      "type" : "string"
    },
    "Tags" : {
      "minItems" : 1,
      "maxItems" : 200,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "TemplateId" : {
      "minLength" : 1,
      "pattern" : "^[\\w\\-]+$",
      "type" : "string",
      "maxLength" : 512
    }
  }
}