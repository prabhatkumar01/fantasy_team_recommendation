const fs = require('fs');
const axios = require('axios');
const csv = require('csv-parser');

// API URL to fetch player stats
const playerStatsApiUrl = 'https://pp-hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary';
const headers = {
    'x-hsci-auth-key': '',  // Replace with your actual API key or auth token
    'Content-Type': 'application/json',
};


// Function to fetch player stats by playerId
async function fetchPlayerStats(playerId) {
    try {
        console.log("Fetching for player id", playerId);
        const response = await axios.get(`${playerStatsApiUrl}?playerId=${playerId}&recordClassId=3&type=BOWLING`, { headers });
        return response.data.summary;
    } catch (error) {
        console.error(`Error fetching stats for player ${playerId}:`, error.message);
        return null;
    }
}



// Function to read playerIds from CSV and fetch stats
async function fetchPlayersStatsFromCSV() {
    const playersIds = [];

    // Read the CSV file containing player information
    fs.createReadStream('player.csv')
        .pipe(csv())
        .on('data', async (row) => {
            const playerId = row.id;

            playersIds.push({
                id: playerId, 
                player_name: row.name,
                roles: row.roles,
                team_id: row.teamId,
                team_name: row.teamName
            });

            // Fetch player stats

        })
        .on('end', () => {
            getData(playersIds);
            // Once all players are processed, write the player stats to a JSON file
            //console.log('Player stats have been written to players_stats.json');
        });
}


async function getData(playersIds) {
    const stats = []
    console.log("ids length", playersIds.length);
    for (const player of playersIds) {
        const playerStats = await fetchPlayerStats(player.id);
        if (playerStats) {

            stats.push({
                player_id: player.id,
                player_name: player.player_name,
                team_id: player.team_id,
                team_name: player.team_name,
                type: playerStats.type,
                //match: playerStats.groups[0].stats[0].mt,
               // runs: playerStats.groups[0].stats[0].rn,
                avg: playerStats.groups[0].stats[0].bwa,
                best_bowling: playerStats.groups[0].stats[0].hs || playerStats.groups[0].stats[0].bbi,
               wickets:  playerStats.groups[0].stats[0].wk || 0,
               economy:  playerStats.groups[0].stats[0].bwe,
               strike_rate: playerStats.groups[0].stats[0].bwsr,
                five_wicket: playerStats.groups[0].stats[0].fwk,
                roles: player.roles
            });
        }
    }

    fs.writeFileSync('players_stats_boller.json', JSON.stringify(stats, null, 2));

}

fetchPlayersStatsFromCSV();