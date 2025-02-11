# fantasy_team_recommendation



input (team1, team2, ground, risk_percent, team_type[batting_heavy balling_heavy, all_rounder_heavy, balanced, team1_heavy, team2_heavy])

1. fetch ground stats
2. fetch player stats for ground (one time job to create player_ground stats, and add to prompt)
3. fetch player overall stats
4. fetch player innings stats
5. for risk percent ex(60%: then consider giving more weight to ground stats, carrier stats and against team stats, compartively low on recent form(innings stats))


