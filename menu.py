import os

from save_file import save_file
from steamunlocked import SteamUL


def menu() -> None:
    """Present the main menu for SteamUL."""
    title = """
             _____  _                            _   _  _     
            /  ___|| |                          | | | || |    
            \ `--. | |_   ___   __ _  _ __ ___  | | | || |    
             `--. \| __| / _ \ / _` || '_ ` _ \ | | | || |    
            /\__/ /| |_ |  __/| (_| || | | | | || |_| || |____
            \____/  \__| \___| \__,_||_| |_| |_| \___/ \_____/            
            """
    print(title)
    print("SteamUL v1.0 by Buu (Discord: Kid I3uu#9827)")
    print("Python CLI to grab DDL for games off steamunlocked.net")
    print()

    # Create SteamUL object for user-inputted query and grab the search results
    query = SteamUL(input("Search:\t"))
    query.search_results()

    # Show the search results for user selection
    show_results(query)


def show_results(query: SteamUL) -> None:
    """Present the search results of the user-inputted SteamUL query."""
    # Print names of the found games
    print("\nSearch results...")
    i = 1
    for item in query.results:
        print(f"[{i}] {query.results[item]['name']}")
        i += 1
    print('-' * 80)

    # Get the user to select their game
    select_game(query)


def select_game(query: SteamUL) -> None:
    """Get the user's choice of the game they want to download."""
    # Ask user for their game of interest
    choice = int(input("Selection:\t"))

    # Grab and show download link for the selected number
    ddl = query.download_link(choice)
    print("DDL:\t" + ddl)

    # Ask the user to download or not
    immediate_dl(query, choice, ddl)


def immediate_dl(query: SteamUL, choice: int, ddl: str) -> None:
    """Ask the user whether they'd like to download the game immediately."""
    # Ask user whether the game should be downloaded or not
    print(f"Would you like to download '{query.results[choice]['name']}' now?")
    print("\t[1]\tY\n\t[2]\tN")
    dl_now = input("Selection:\t")

    # If they choose to download immediately
    if str(dl_now) == '1':
        # Check for/create directory where the file will be saved
        if not os.path.exists("./SteamUL Downloads/Archives"):
            os.makedirs("./SteamUL Downloads/Archives")

        # Remove special characters from filename
        name = query.results[choice]['name']
        name = f"{name.replace(':', '-').replace('?', '-')}.zip"

        file_path = os.path.join("./SteamUL Downloads/Archives", name)

        # Save the file
        save_file(ddl, file_path)

        restart()

    # If not
    else:
        restart()


def restart() -> None:
    """Ask the user whether they'd like to quit or return to the main menu."""
    choice = input("Press [1] to quit or [2] to return to the main menu...\t")
    if choice == '1':
        pass
    elif choice == '2':
        menu()


if __name__ == '__main__':
    menu()
