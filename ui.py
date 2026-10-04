from cup import Cup
from repository import Repository
from datetime import datetime

class UI:
    """
    Handles the command-line menu interface.
    """
    
    def __init__(self):
        self.repo = Repository()
        self.cup = self.repo.load()
    
    def display_menu(self):
        print("\n=== Hockey Cup Team Management ===")
        print("1. Add new team")
        print("2. View team by ID")
        print("3. List all teams")
        print("4. List boys teams")
        print("5. List girls teams")
        print("6. Update team")
        print("7. Delete team")
        print("8. Cancel team")
        print("9. Search teams by name")
        print("10. Filter teams by payment status")
        print("11. Show statistics")
        print("0. Exit")
        print("==================================")
    
    def get_int_input(self, prompt: str, min_val: int = 0) -> int:
        """
        Get validated integer input.
        :param prompt: Input prompt.
        :param min_val: Minimum allowed value.
        :return: Validated integer.
        """
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print(f"Value must be at least {min_val}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid integer.")
    
    def get_bool_input(self, prompt: str) -> bool:
        """
        Get validated boolean input (y/n).
        :param prompt: Input prompt.
        :return: Boolean value.
        """
        while True:
            response = input(prompt + " (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'.")
    
    def get_string_input(self, prompt: str) -> str:
        """
        Get non-empty string input.
        :param prompt: Input prompt.
        :return: Non-empty string.
        """
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Please enter a non-empty value.")
    
    def add_team(self):
        name = self.get_string_input("Enter team name: ")
        team_type = self.get_string_input("Enter team type (boys/girls): ").lower()
        if team_type not in ['boys', 'girls']:
            print("Invalid type. Must be 'boys' or 'girls'.")
            return
        team_id = self.cup.add_team(name, team_type)
        self.repo.save(self.cup)
        print(f"Team added successfully with ID: {team_id}")
    
    def view_team(self):
        team_id = self.get_int_input("Enter team ID: ")
        team = self.cup.get_team(team_id)
        if team:
            print(team)
        else:
            print("Team not found.")
    
    def list_teams(self, teams):
        if not teams:
            print("No teams found.")
            return
        for team in teams:
            print(team)
    
    def list_all(self):
        self.list_teams(self.cup.list_all())
    
    def list_boys(self):
        self.list_teams(self.cup.list_boys())
    
    def list_girls(self):
        self.list_teams(self.cup.list_girls())
    
    def update_team(self):
        team_id = self.get_int_input("Enter team ID: ")
        if not self.cup.get_team(team_id):
            print("Team not found.")
            return
        
        print("\nUpdate options:")
        print("1. Name")
        print("2. Type")
        print("3. Fee paid status")
        choice = self.get_int_input("Choose option (1-3): ", 1)
        
        if choice == 1:
            new_name = self.get_string_input("Enter new name: ")
            if self.cup.update_team(team_id, 'name', new_name):
                print("Name updated.")
            else:
                print("Update failed.")
        elif choice == 2:
            new_type = self.get_string_input("Enter new type (boys/girls): ").lower()
            if new_type not in ['boys', 'girls']:
                print("Invalid type.")
                return
            if self.cup.update_team(team_id, 'type', new_type):
                print("Type updated.")
            else:
                print("Update failed.")
        elif choice == 3:
            new_paid = self.get_bool_input("Is fee paid?")
            if self.cup.update_team(team_id, 'fee_paid', new_paid):
                print("Fee status updated.")
            else:
                print("Update failed.")
        
        self.repo.save(self.cup)
    
    def delete_team(self):
        team_id = self.get_int_input("Enter team ID: ")
        if self.cup.remove_team(team_id):
            print("Team deleted.")
            self.repo.save(self.cup)
        else:
            print("Team not found.")
    
    def cancel_team(self):
        team_id = self.get_int_input("Enter team ID: ")
        if self.cup.cancel_team(team_id):
            print("Team cancelled.")
            self.repo.save(self.cup)
        else:
            print("Team not found.")
    
    def search_by_name(self):
        partial = self.get_string_input("Enter partial name: ")
        teams = self.cup.search_by_name(partial)
        self.list_teams(teams)
    
    def filter_by_paid(self):
        paid = self.get_bool_input("Filter paid teams? (y for paid, n for not paid)")
        teams = self.cup.filter_by_paid(paid)
        status = "Paid" if paid else "Not Paid"
        print(f"\n{status} teams:")
        self.list_teams(teams)
    
    def show_statistics(self):
        stats = self.cup.get_statistics()
        print("\n=== Statistics ===")
        print(f"Total teams: {stats['total_teams']}")
        print(f"Percentage paid: {stats['percent_paid']:.1f}%")
        print(f"Cancelled teams: {stats['cancelled_teams']}")
        print(f"Participation fee per team: ${stats['fee_amount']}")
        print("==================")
    
    def run(self):
        """
        Main loop for the UI.
        """
        while True:
            self.display_menu()
            choice = self.get_int_input("Enter choice: ", 0)
            
            if choice == 0:
                print("Exiting program.")
                break
            elif choice == 1:
                self.add_team()
            elif choice == 2:
                self.view_team()
            elif choice == 3:
                self.list_all()
            elif choice == 4:
                self.list_boys()
            elif choice == 5:
                self.list_girls()
            elif choice == 6:
                self.update_team()
            elif choice == 7:
                self.delete_team()
            elif choice == 8:
                self.cancel_team()
            elif choice == 9:
                self.search_by_name()
            elif choice == 10:
                self.filter_by_paid()
            elif choice == 11:
                self.show_statistics()
            else:
                print("Invalid choice. Please try again.")