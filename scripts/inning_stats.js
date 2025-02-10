const fs = require('fs');
const axios = require('axios');

const point_system = {
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
  };

  function calculatePoints(player) {
    let totalPoints = 0;
  
    // Batting Points
    if (player.totalRuns === 0 && player.ballsFaced > 0) {
      totalPoints += point_system.batting.duck;
    } else if (player.totalRuns > 0) {
      let runsCategory = "0";
      if (player.totalRuns >= 90) runsCategory = "90+";
      else if (player.totalRuns >= 70) runsCategory = "70-89";
      else if (player.totalRuns >= 50) runsCategory = "50-69";
      else if (player.totalRuns >= 30) runsCategory = "30-49";
      else if (player.totalRuns >= 10) runsCategory = "10-29";
      else if (player.totalRuns >= 1) runsCategory = "1-9";
      totalPoints += point_system.batting.runs[runsCategory];
      totalPoints += player.totalRuns;
      totalPoints += player.fours * point_system.batting.boundaries["4"];
      totalPoints += player.sixes * point_system.batting.boundaries["6"];
  
      if (player.strikeRate > 150) totalPoints += point_system.batting.strike_rate.above_150;
      else if (player.strikeRate >= 120) totalPoints += point_system.batting.strike_rate.between_120_and_150;
      else if (player.strikeRate <= 40) {
          totalPoints  -= player.ballsFaced * 0.5
      }
  
    }
  
    //Bowling Points
    if (player.wicketsTaken > 0) {
          let wicketsCategory = "0";
          if (player.wicketsTaken >= 5) wicketsCategory = "5+";
          else if (player.wicketsTaken === 4) wicketsCategory = "4";
          else if (player.wicketsTaken === 3) wicketsCategory = "3";
          else if (player.wicketsTaken === 2) wicketsCategory = "2";
          else if (player.wicketsTaken === 1) wicketsCategory = "1";
          totalPoints += point_system.bowling.wickets[wicketsCategory];
          totalPoints += player.wickets * 25;
  
          if (player.economy <= 6 && player.economy>0) totalPoints += point_system.bowling.economy_rate.under_6;
          else if (player.economy <= 7) totalPoints += point_system.bowling.economy_rate.between_6_and_7;
          else if (player.economy <= 8) totalPoints += point_system.bowling.economy_rate.between_7_and_8;
  
  
        }
        //Fielding points
      totalPoints += (player.catches || 0) * point_system.fielding.catch;
      totalPoints += (player.runOuts || 0) * point_system.fielding.run_out;
      totalPoints += (player.stumps || 0) * point_system.fielding.stumping;
  
  
    return totalPoints;
  }
  


function computePlayerStats(innings, matchId) {
  try {
    let playerStats = [];
    innings.forEach((inningData) => {
        const inningBatsmen = inningData.inningBatsmen || [];
    const inningBowlers = inningData.inningBowlers || [];

    // 3.  Process Batsmen Data
    playerStats = inningBatsmen.map((batsman) => {
      return {
        playerId: batsman.player.objectId,
        name: batsman.player.longName,
        totalRuns: batsman.runs || 0,
        ballsFaced: batsman.balls || 0,
        strikeRate: batsman.strikerate || 0.0,
        fours: batsman.fours || 0,
        sixes: batsman.sixes || 0,
        wickets: 0, // Initialize to 0, since these are batsmen
        catches: 0, // Initialize to 0, updated later if they took a catch
        runOuts: 0, // Initialize to 0, updated later if they did a runout
        stumps: 0 // Initialize to 0, updated later if they did a stump
      };
    });

     // 4. Process bowler data. If bowler is also a batsmen data will be updated or new data will be created.
     inningBowlers.forEach(bowler => {
        const existingPlayer = playerStats.find(p => p.playerId === bowler.player.objectId);
        if (existingPlayer) {
            existingPlayer.oversBowled = bowler.overs || 0;
            existingPlayer.runsConceded = bowler.conceded || 0;
            existingPlayer.wicketsTaken = bowler.wickets || 0;
            existingPlayer.economy = bowler.economy || 0;
            existingPlayer.role = 'allrounder';
        } else {
            playerStats.push({
                playerId: bowler.player.objectId,
                role: 'bowler',
                name: bowler.player.longName,
                totalRuns: 0,
                ballsFaced: 0,
                strikeRate: 0,
                fours: 0,
                sixes: 0,
                wickets: 0,
                catches: 0,
                runOuts: 0,
                stumps: 0,
                oversBowled: bowler.overs || 0,
                runsConceded: bowler.conceded || 0,
                wicketsTaken: bowler.wickets || 0,
                economy: bowler.economy || 0
            });
        }
    });
    //5.Find catch data

    inningBatsmen.forEach(batsman => {
       if (batsman.dismissalFielders && batsman.dismissalFielders.length > 0 && batsman.dismissalFielders[0].player) {
         const fielderId = batsman.dismissalFielders[0].player.objectId;
         const fielder = playerStats.find(p => p.playerId === fielderId);
        
         if (fielder) {
           fielder.catches = (fielder.catches || 0) + 1;
         }else{
           // fielder information if no batting stat
           playerStats.push({
             role: "batsman",
             playerId: fielderId,
             name: batsman.dismissalFielders[0].player.name,
             totalRuns: 0,
             ballsFaced: 0,
             strikeRate: 0,
             fours: 0,
             sixes: 0,
             oversBowled: 0,
             runsConceded: 0,
             wicketsTaken: 0,
             economy: 0,
             catches:1,
             runOuts:0,
             stumps: 0
           });
         }
       }
     });

    })
    // 2. Extract batsmen and bowlers data
    

    // 6. Create the final JSON response
    const jsonResponse = {
        players: playerStats.map(player => ({
            ...player,
            totalPoints: calculatePoints(player)
          }))
    };

    const outputFilePath = `./stats/${matchId}_inning_stats.json`;
    fs.writeFileSync(outputFilePath, JSON.stringify(jsonResponse, null, 2), 'utf8');
    console.log(`Player stats written to ${outputFilePath}`);

    return jsonResponse;

  } catch (error) {
    console.error("Error processing inning stats:", error);
    return null;
  }
}

const apiUrl = 'https://pp-hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?seriesId=1410320';
const playersApiUrl = 'https://pp-hs-consumer-api.espncricinfo.com/v1/pages/match/team-players?seriesId=1410320';   // Replace with your actual API URL
const headers = {
    'x-hsci-auth-key': '',  // Replace with your actual API key or auth token
    'Content-Type': 'application/json',
};

async function fetchInningsScore(matchId) {
    try {
        const response = await axios.get(`${apiUrl}&matchId=${matchId}`, { headers });
        return response.data.content.innings || [];
    } catch (error) {
        console.error(`Error fetching players for team ${matchId}:`, error);
        return [];
    }
}

const matchIds = ['1422131'];

async function fetchData () {
    for(id of matchIds) {
        const innings = await fetchInningsScore(id);
        computePlayerStats(innings, id);
    }
}

fetchData();