# QuickSight resources for Fantasy Football Dashboard
# 
# IMPORTANT: Before applying this, you need to:
# 1. Sign up for QuickSight in the AWS Console
# 2. Note your QuickSight username (usually your email or IAM username)
# 3. Set var.quicksight_user in your terraform.tfvars

# Note: aws_caller_identity.current is defined in iam.tf

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = var.aws_region
}

# --- QuickSight Data Source (Athena) ---
resource "aws_quicksight_data_source" "athena" {
  data_source_id = "${var.project}-athena-source"
  name           = "${var.project} Athena Data Source"
  type           = "ATHENA"

  parameters {
    athena {
      work_group = aws_athena_workgroup.wg.name
    }
  }

  permission {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSource",
      "quicksight:DescribeDataSourcePermissions",
      "quicksight:PassDataSource",
      "quicksight:UpdateDataSource",
      "quicksight:DeleteDataSource",
      "quicksight:UpdateDataSourcePermissions"
    ]
  }

  aws_account_id = local.account_id
}

# --- QuickSight Datasets ---

# Dataset: Win History
resource "aws_quicksight_data_set" "win_history" {
  data_set_id = "${var.project}-win-history"
  name        = "Win History"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "win-history-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_win_history"

      input_columns {
        name = "championship_year"
        type = "INTEGER"
      }
      input_columns {
        name = "place"
        type = "INTEGER"
      }
      input_columns {
        name = "member_id"
        type = "INTEGER"
      }
      input_columns {
        name = "member"
        type = "STRING"
      }
      input_columns {
        name = "money_won"
        type = "INTEGER"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}

# Dataset: Regular Season
resource "aws_quicksight_data_set" "regular_season" {
  data_set_id = "${var.project}-regular-season"
  name        = "Regular Season"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "regular-season-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_regular_season"

      input_columns {
        name = "season"
        type = "INTEGER"
      }
      input_columns {
        name = "week"
        type = "INTEGER"
      }
      input_columns {
        name = "team_name"
        type = "STRING"
      }
      input_columns {
        name = "opponent"
        type = "STRING"
      }
      input_columns {
        name = "points_for"
        type = "DECIMAL"
      }
      input_columns {
        name = "points_against"
        type = "DECIMAL"
      }
      input_columns {
        name = "margin"
        type = "DECIMAL"
      }
      input_columns {
        name = "result"
        type = "STRING"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}

# Dataset: Matchup Data
resource "aws_quicksight_data_set" "matchup_data" {
  data_set_id = "${var.project}-matchup-data"
  name        = "Matchup Data"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "matchup-data-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_matchup_data"

      input_columns {
        name = "season"
        type = "INTEGER"
      }
      input_columns {
        name = "week"
        type = "INTEGER"
      }
      input_columns {
        name = "matchup_id"
        type = "INTEGER"
      }
      input_columns {
        name = "team_name"
        type = "STRING"
      }
      input_columns {
        name = "points"
        type = "DECIMAL"
      }
      input_columns {
        name = "result"
        type = "STRING"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}

# Dataset: Lineup Efficiency
resource "aws_quicksight_data_set" "lineup_efficiency" {
  data_set_id = "${var.project}-lineup-efficiency"
  name        = "Lineup Efficiency"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "lineup-efficiency-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_lineup_efficiency_weekly"

      input_columns {
        name = "member_id"
        type = "INTEGER"
      }
      input_columns {
        name = "member"
        type = "STRING"
      }
      input_columns {
        name = "year"
        type = "INTEGER"
      }
      input_columns {
        name = "week"
        type = "INTEGER"
      }
      input_columns {
        name = "actual_points"
        type = "DECIMAL"
      }
      input_columns {
        name = "optimal_points"
        type = "DECIMAL"
      }
      input_columns {
        name = "points_left_on_bench"
        type = "DECIMAL"
      }
      input_columns {
        name = "lineup_efficiency_pct"
        type = "DECIMAL"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}

# Dataset: Player Details
resource "aws_quicksight_data_set" "player_details" {
  data_set_id = "${var.project}-player-details"
  name        = "Player Details by Team"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "player-details-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_player_details_by_team"

      input_columns {
        name = "season"
        type = "INTEGER"
      }
      input_columns {
        name = "team_name"
        type = "STRING"
      }
      input_columns {
        name = "player_name"
        type = "STRING"
      }
      input_columns {
        name = "position"
        type = "STRING"
      }
      input_columns {
        name = "total_points"
        type = "DECIMAL"
      }
      input_columns {
        name = "games_played"
        type = "INTEGER"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}

# Dataset: Player Total Points
resource "aws_quicksight_data_set" "player_points" {
  data_set_id = "${var.project}-player-points"
  name        = "Player Total Points"
  import_mode = "DIRECT_QUERY"

  physical_table_map {
    physical_table_map_id = "player-points-table"
    relational_table {
      data_source_arn = aws_quicksight_data_source.athena.arn
      catalog         = "AwsDataCatalog"
      schema          = aws_glue_catalog_database.raw.name
      name            = "stg_player_total_points"

      input_columns {
        name = "player_name"
        type = "STRING"
      }
      input_columns {
        name = "position"
        type = "STRING"
      }
      input_columns {
        name = "team"
        type = "STRING"
      }
      input_columns {
        name = "total_points"
        type = "DECIMAL"
      }
      input_columns {
        name = "games_played"
        type = "INTEGER"
      }
      input_columns {
        name = "avg_points"
        type = "DECIMAL"
      }
      input_columns {
        name = "source_system"
        type = "STRING"
      }
      input_columns {
        name = "imported_on"
        type = "STRING"
      }
    }
  }

  permissions {
    principal = "arn:aws:quicksight:${local.region}:${local.account_id}:user/default/${var.quicksight_user}"
    actions = [
      "quicksight:DescribeDataSet",
      "quicksight:DescribeDataSetPermissions",
      "quicksight:PassDataSet",
      "quicksight:DescribeIngestion",
      "quicksight:ListIngestions",
      "quicksight:UpdateDataSet",
      "quicksight:DeleteDataSet",
      "quicksight:CreateIngestion",
      "quicksight:CancelIngestion",
      "quicksight:UpdateDataSetPermissions"
    ]
  }
}
