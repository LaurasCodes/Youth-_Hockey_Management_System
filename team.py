from datetime import datetime

class Team:
    """
    Represents a youth hockey team.
    Encapsulates team data with private attributes.
    """
    
    def __init__(self, team_id: int, name: str, team_type: str):
        """
        Initialize a new team.
        :param team_id: Unique integer ID.
        :param name: Team name (str).
        :param team_type: 'boys' or 'girls' (str).
        """
        self.__id = team_id
        self.__created_date = datetime.now().strftime('%Y-%m-%d')
        self.__name = name
        self.__type = team_type
        self.__fee_paid = False
        self.__cancelled_date = None
    
    # Getters
    def get_id(self) -> int:
        return self.__id
    
    def get_created_date(self) -> str:
        return self.__created_date
    
    def get_name(self) -> str:
        return self.__name
    
    def get_type(self) -> str:
        return self.__type
    
    def get_fee_paid(self) -> bool:
        return self.__fee_paid
    
    def get_cancelled_date(self) -> str | None:
        return self.__cancelled_date
    
    # Setters (only for updatable fields)
    def set_name(self, name: str):
        self.__name = name
    
    def set_type(self, team_type: str):
        self.__type = team_type
    
    def set_fee_paid(self, paid: bool):
        self.__fee_paid = paid
    
    def set_cancelled_date(self, date: str):
        self.__cancelled_date = date
    
    def __str__(self) -> str:
        status = "Paid" if self.__fee_paid else "Not Paid"
        cancelled = f" (Cancelled: {self.__cancelled_date})" if self.__cancelled_date else ""
        return (f"ID: {self.__id}, Name: {self.__name}, Type: {self.__type}, "
                f"Created: {self.__created_date}, Fee: {status}{cancelled}")