const fs = require('fs');

// Function to calculate the total fantasy points
function calculateFantasyPoints(matchId,teamName, fantasyTeamFilePath, matchStatsFilePath) {
  // Read the fantasy team and match statistics JSON files
  const fantasyData = JSON.parse(fs.readFileSync(fantasyTeamFilePath, 'utf-8'));
  const matchStats = JSON.parse(fs.readFileSync(matchStatsFilePath, 'utf-8'));

  // Create a map of playerId to stats for quick lookup
  const statsMap = matchStats.players.reduce((map, player) => {
    map[player.playerId] = player.totalPoints;
    return map;
  }, {});

  // Initialize total points counters
  let totalTeamPoints = 0;

  // Iterate over the fantasy team and calculate the points
  fantasyData.data.fantasy_team.forEach(player => {
    const playerStats = statsMap[player.player_id] || 0; // Default to 0 if no stats found

    // Calculate the total points based on role (captain/vice-captain)
    let playerPoints = playerStats;

    if (fantasyData.data.captain.player_id === player.player_id) {
      playerPoints *= 2; // Double points for captain
    } else if (fantasyData.data.vice_captain.player_id === player.player_id) {
      playerPoints *= 1.5; // 1.5x points for vice-captain
    }

    // Assign the calculated points back to the player
    player.totalPoints = playerPoints;

    // Add the player's points to the total team points
    totalTeamPoints += playerPoints;
  });

  fantasyData.data.totalTeamPoints = totalTeamPoints;

  // Write the updated fantasy team data to a new JSON file
  const updatedFantasyData = { ...fantasyData };
  const outputFilePath = `./${matchId}_${teamName}_team_stats.json`;
  fs.writeFileSync(outputFilePath, JSON.stringify(updatedFantasyData, null, 2));

  // Return the updated total team points and fantasy team data
  return { totalTeamPoints, fantasyData: updatedFantasyData };
}

function computeData(matchId) {
    const fantasyTeamFilePath = '../response/DC_CSK_10_Balanced.json';  // Path to the fantasy team data
    const matchStatsFilePath = `./stats/${matchId}_inning_stats.json`;  // Path to the match stats data
    
    const { totalTeamPoints, fantasyData: updatedFantasyData } = calculateFantasyPoints(matchId, 'DC_CSK_10_Balanced', fantasyTeamFilePath, matchStatsFilePath);
    
    console.log("Total Team Points:", totalTeamPoints);
    console.log("Updated Fantasy Team Data:", updatedFantasyData);
}
// Example usage

computeData("1422131")