import json
from datetime import datetime
from typing import List
from cup import Cup
from team import Team

class Repository:
    """
    Handles saving and loading Cup data to/from JSON file.
    """
    
    def __init__(self, filename: str = 'teams.json'):
        self.filename = filename
    
    def save(self, cup: Cup):
        """
        Save Cup data to JSON file.
        :param cup: The Cup instance to save.
        """
        data = {
            'next_id': cup.get_next_id(),
            'teams': []
        }
        for team in cup.get_teams():
            team_data = {
                'id': team.get_id(),
                'created_date': team.get_created_date(),
                'name': team.get_name(),
                'type': team.get_type(),
                'fee_paid': team.get_fee_paid(),
                'cancelled_date': team.get_cancelled_date()
            }
            data['teams'].append(team_data)
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load(self) -> Cup:
        """
        Load Cup data from JSON file.
        :return: Loaded Cup instance.
        """
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            cup = Cup()
            cup.set_next_id(data.get('next_id', 1))
            
            for team_data in data.get('teams', []):
                team = Team(
                    team_data['id'],
                    team_data['name'],
                    team_data['type']
                )
                team.set_fee_paid(team_data['fee_paid'])
                cancelled_date = team_data.get('cancelled_date')
                if cancelled_date:
                    team.set_cancelled_date(cancelled_date)
                cup.get_teams().append(team)  # Direct append since private, but for load
            
            # Update next_id to max +1
            if cup.get_teams():
                max_id = max(t.get_id() for t in cup.get_teams())
                cup.set_next_id(max_id + 1)
            
            return cup
        except FileNotFoundError:
            return Cup()
        except json.JSONDecodeError:
            print("Error loading file: Invalid JSON. Starting with empty data.")
            return Cup()