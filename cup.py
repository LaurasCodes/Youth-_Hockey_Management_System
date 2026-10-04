from typing import List, Optional
from team import Team
from datetime import datetime

class Cup:
    """
    Manages a collection of teams for the hockey cup.
    Handles adding, removing, updating, and statistics.
    """
    
    FEE_AMOUNT = 100.0  # The participation fee per team (constant)
    
    def __init__(self):
        self.__teams: List[Team] = []
        self.__next_id = 1
    
    def add_team(self, name: str, team_type: str) -> int:
        """
        Add a new team and return its ID.
        :param name: Team name.
        :param team_type: 'boys' or 'girls'.
        :return: The assigned ID.
        """
        team = Team(self.__next_id, name, team_type)
        self.__teams.append(team)
        self.__next_id += 1
        return team.get_id()
    
    def remove_team(self, team_id: int) -> bool:
        """
        Remove a team by ID.
        :param team_id: The team ID.
        :return: True if removed, False if not found.
        """
        for i, team in enumerate(self.__teams):
            if team.get_id() == team_id:
                self.__teams.pop(i)
                return True
        return False
    
    def get_team(self, team_id: int) -> Optional[Team]:
        """
        Get a team by ID.
        :param team_id: The team ID.
        :return: Team object or None.
        """
        for team in self.__teams:
            if team.get_id() == team_id:
                return team
        return None
    
    def list_all(self) -> List[Team]:
        return self.__teams[:]
    
    def list_boys(self) -> List[Team]:
        return [t for t in self.__teams if t.get_type() == 'boys']
    
    def list_girls(self) -> List[Team]:
        return [t for t in self.__teams if t.get_type() == 'girls']
    
    def update_team(self, team_id: int, field: str, value: any) -> bool:
        """
        Update a team's field.
        :param team_id: The team ID.
        :param field: 'name', 'type', or 'fee_paid'.
        :param value: New value.
        :return: True if updated, False if not found.
        """
        team = self.get_team(team_id)
        if not team:
            return False
        if field == 'name':
            team.set_name(value)
        elif field == 'type':
            team.set_type(value)
        elif field == 'fee_paid':
            team.set_fee_paid(value)
        else:
            return False
        return True
    
    def cancel_team(self, team_id: int) -> bool:
        """
        Cancel a team by setting cancellation date.
        :param team_id: The team ID.
        :return: True if cancelled, False if not found.
        """
        team = self.get_team(team_id)
        if not team:
            return False
        team.set_cancelled_date(datetime.now().strftime('%Y-%m-%d'))
        return True
    
    def search_by_name(self, partial_name: str) -> List[Team]:
        """
        Search teams by partial name (case-insensitive).
        :param partial_name: Partial name to search.
        :return: List of matching teams.
        """
        return [t for t in self.__teams if partial_name.lower() in t.get_name().lower()]
    
    def filter_by_paid(self, paid: bool) -> List[Team]:
        """
        Filter teams by payment status.
        :param paid: True for paid, False for not paid.
        :return: List of matching teams.
        """
        return [t for t in self.__teams if t.get_fee_paid() == paid]
    
    def count_total(self) -> int:
        return len(self.__teams)
    
    def percent_paid(self) -> float:
        """
        Percentage of teams that have paid (excluding cancelled).
        :return: Percentage as float (0-100).
        """
        active_teams = [t for t in self.__teams if not t.get_cancelled_date()]
        if not active_teams:
            return 0.0
        paid = sum(1 for t in active_teams if t.get_fee_paid())
        return (paid / len(active_teams)) * 100
    
    def count_cancelled(self) -> int:
        return sum(1 for t in self.__teams if t.get_cancelled_date())
    
    def get_statistics(self) -> dict:
        """
        Get statistics dictionary.
        :return: Dict with total, percent_paid, cancelled.
        """
        return {
            'total_teams': self.count_total(),
            'percent_paid': self.percent_paid(),
            'cancelled_teams': self.count_cancelled(),
            'fee_amount': self.FEE_AMOUNT
        }
    
    def get_next_id(self) -> int:
        return self.__next_id
    
    def set_next_id(self, next_id: int):
        self.__next_id = next_id
    
    def get_teams(self) -> List[Team]:
        return self.__teams