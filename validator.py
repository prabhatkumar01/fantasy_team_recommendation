def validate_fantasy_team(response, rules):
    data = response['data']
    team = data['fantasy_team']
    total_credit_used = data['total_credit_used']
    team_balance = data['team_balance']
    validation = data['validation']
    
    # Validate total players
    if len(team) != rules['team_composition']['total_players']:
        return False, "Invalid number of total players"
    
    # Validate roles
    roles_count = {
        'batsmen': 0,
        'bowlers': 0,
        'allrounders': 0,
        'wicketkeepers': 0
    }
    for player in team:
        role = player['role'].lower()
        if role in roles_count:
            roles_count[role] += 1
        elif role == 'batsman':
            roles_count['batsmen'] += 1
        elif role == 'bowler':
            roles_count['bowlers'] += 1
        elif role == 'allrounder':
            roles_count['allrounders'] += 1
        elif role == 'wicketkeeper':
            roles_count['wicketkeepers'] += 1
    
    for role, limits in rules['team_composition']['roles'].items():
        if not (limits['min'] <= roles_count[role] <= limits['max']):
            return False, f"Invalid number of {role}"
    
    # Validate total credits
    if total_credit_used > rules['credit_system']['total_credits']:
        return False, "Total credits used exceed the limit"
    
    # Validate max players per team
    for team_name, count in team_balance.items():
        if count > rules['player_selection_rules']['max_players_per_team']:
            return False, f"Too many players from {team_name}"
    
    # Validate captain and vice-captain
    captain = data['captain']
    vice_captain = data['vice_captain']
    captain_found = False
    vice_captain_found = False
    for player in team:
        if player['player_id'] == captain['player_id']:
            captain_found = True
        if player['player_id'] == vice_captain['player_id']:
            vice_captain_found = True
    
    if not captain_found:
        return False, "Captain not found in the team"
    if not vice_captain_found:
        return False, "Vice-captain not found in the team"
    
    # Validate validation flags
    if not validation['credit_usage_valid']:
        return False, "Credit usage is not valid"
    if not validation['roles_valid']:
        return False, "Roles are not valid"
    if not validation['team_balance_valid']:
        return False, "Team balance is not valid"
    
    return True, "Validation successful"