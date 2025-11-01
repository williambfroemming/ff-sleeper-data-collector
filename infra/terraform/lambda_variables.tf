# Variables for Lambda data collection

variable "current_league_id" {
  description = "Sleeper league ID for current season"
  type        = string
}

variable "current_year" {
  description = "Current fantasy season year"
  type        = number
  default     = 2025
}

variable "historical_leagues" {
  description = "Map of year to league ID for historical seasons"
  type        = map(string)
  default = {
    "2020" = "596553726760632320"
    "2021" = "726144978962747392"
    "2022" = "862818439088189440"
    "2023" = "994041566085910528"
    "2024" = "1124822672346198016"
  }
}

variable "name_map" {
  description = "Mapping of Sleeper display names to real names"
  type        = map(string)
  default = {
    "11kaplandh"      = "Daniel"
    "Jgersowsky"      = "Justin"
    "blinton2"        = "Bryan"
    "BillFroemming"   = "Bill"
    "OGJonnyB"        = "Jon"
    "jcarney3344"     = "Jack"
    "nsaed"           = "Nate"
    "gizzle4"         = "Eric"
    "mlguagliardo"    = "Mario"
    "bgabrielsen"     = "Brian"
  }
}

variable "scoring_settings" {
  description = "League scoring settings"
  type        = map(number)
  default = {
    # Passing
    pass_yd      = 0.04
    pass_td      = 4
    pass_2pt     = 2
    pass_int     = -2
    pass_int_td  = -1
    
    # Rushing
    rush_yd  = 0.1
    rush_td  = 6
    rush_2pt = 2
    rush_fd  = 0.5
    
    # Receiving
    rec_yd  = 0.1
    rec_td  = 6
    rec_2pt = 2
    rec_fd  = 0.5
    
    # Kicking
    fgm_0_19  = 3
    fgm_20_29 = 3
    fgm_30_39 = 3
    fgm_40_49 = 4
    fgm_50p   = 5
    xpm       = 1
    fgmiss    = -1
    xpmiss    = -1
    
    # Defense
    def_td         = 6
    def_st_td      = 6
    def_int        = 2
    def_sack       = 1
    def_safe       = 3
    def_blk_kick   = 2
    def_3_and_out  = 0.5
    def_4_down_stop = 0.5
    def_st_fum_rec = 2
    def_st_ff      = 1
    def_fum_rec    = 2
    fum_rec_td     = 6
    
    # Defense Points Allowed
    pts_allow_0     = 11
    pts_allow_1_6   = 8
    pts_allow_7_13  = 5
    pts_allow_14_20 = 2
    pts_allow_21_27 = 0
    pts_allow_28_34 = -2
    pts_allow_35p   = -5
    
    # Fumbles
    fum_lost = -2
    
    # Bonuses
    bonus_rush_yd_100 = 2
    bonus_rush_yd_200 = 4
    bonus_rec_yd_100  = 2
    bonus_rec_yd_200  = 4
    bonus_pass_yd_300 = 2
    bonus_pass_yd_400 = 4
  }
}

# Schedule control variables
variable "enable_weekly_collection" {
  description = "Enable weekly Wednesday data collection"
  type        = bool
  default     = true
}

variable "enable_season_finale_collection" {
  description = "Enable January season finale collection"
  type        = bool
  default     = true
}
