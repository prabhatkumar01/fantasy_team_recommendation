import getPlayingXI
import generatePrompt
import scoreboards

team1 = input("Enter the name of Team 1: ")
team2 = input("Enter the name of Team 2: ")

players_info = getPlayingXI.getPlayingXI(team1, team2)
# print(players_info)


rules = {
    "team_composition": {
      "total_players": 11,
      "roles": {
        "batsmen": {
          "min": 3,
          "max": 5
        },
        "bowlers": {
          "min": 3,
          "max": 5
        },
        "allrounders": {
          "min": 1,
          "max": 3
        },
        "wicketkeepers": {
          "min": 1,
          "max": 2
        }
      }
    },
    "credit_system": {
      "total_credits": 100
    },
    "player_selection_rules": {
      "max_players_per_team": 7,
      "captain_multiplier": 2,
      "vice_captain_multiplier": 1.5
    }
}

point_system = {
    "batting": {
      "runs": {
        "0": -1,
        "1-9": 1,
        "10-29": 2,
        "30-49": 4,
        "50-69": 6,
        "70-89": 8,
        "90+": 10
      },
      "boundaries": {
        "4": 1,
        "6": 2
      },
      "strike_rate": {
        "above_150": 2,
        "between_120_and_150": 1
      },
      "duck": -2,
      "out_by": {
        "catch": 2,
        "bowled": 2,
        "run_out": 2,
        "lbw": 2,
        "stumped": 2
      }
    },
    "bowling": {
      "wickets": {
        "0": -1,
        "1": 10,
        "2": 20,
        "3": 30,
        "4": 40,
        "5+": 50
      },
      "economy_rate": {
        "under_6": 4,
        "between_6_and_7": 2,
        "between_7_and_8": 1
      },
      "maiden_over": 3,
      "extras_conceded": {
        "wide": 1,
        "no_ball": 1
      },
      "dot_ball": 1,
      "runs_conceded": {
        "under_20": 2,
        "between_20_and_30": 1,
        "above_30": -2
      }
    },
    "fielding": {
      "catch": 4,
      "stumping": 6,
      "run_out": 4,
      "assist": 2,
      "direct_hit_run_out": 6
    },
    "keeping": {
      "dismissal": {
        "catch": 6,
        "stump": 8
      },
      "byes": {
        "each": -0.5
      },
      "leg_byes": {
        "each": -0.5
      }
    },
    "overall": {
      "captain_bonus": 2,
      "vice_captain_bonus": 1
    }
  }

scoreboards = scoreboards.download_files_from_gcs("ipl-scoreboards-2024")

prompt = generatePrompt.generate_prompt(players_info, rules, scoreboards)

generatePrompt.generate(prompt)


