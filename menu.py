import os
import zipfile
from typing import Any

from tqdm import tqdm

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
    print("SteamUL v1.2 by Buu (Discord: Kid I3uu#9827)")
    print("Python CLI to grab DDL for games off steamunlocked.net")
    print()

    # Create SteamUL object for user-inputted query and grab the search results
    query = SteamUL(input("Search:\t"))
    query.search_results()

    # Show the search results for user selection
    show_results(query)


def show_results(query: SteamUL) -> None:
    """Present the search results of the user-inputted SteamUL query."""

    # If there are results returned from the search, print the results
    if query.results != {}:
        print("\nSearch results...")
        i = 1
        for item in query.results:
            print(f"[{i}] {query.results[item]['name']}")
            i += 1
        print('-' * 80)

        # Get the user to select their game
        select_game(query)

    else:
        print(f"No results have been found for '{query.query}'")

        # Get the user to input another query
        query = SteamUL(input("Search:\t"))
        query.search_results()
        show_results(query)


def select_game(query: SteamUL) -> None:
    """Get the user's choice of the game they want to download."""

    # Ask user for their game of interest
    flag = True
    while flag:
        try:
            choice = int(input("Selection:\t"))
            query.results[choice]
            flag = False
        except ValueError:
            print("Please enter the number beside the title of your choice.")
        except KeyError:
            print("Please enter a valid number.")

    # Grab and show information for the selected number
    query.steam_info(choice)

    # Ask whether they want to download the game
    print(f"Would you like to proceed to grabbing the download link for '{query.results[choice]['name']}'?")
    print("\t[1]\tY\n\t[2]\tN")

    flag = True
    while flag:
        try:
            link_now = int(input("Selection:\t"))
            {1: 'one', 2: 'two'}[link_now]
            flag = not(link_now == 1 or link_now == 2)
        except ValueError:
            print("Please enter the number beside your choice.")
        except KeyError:
            print("Please enter a valid number.")

    if str(link_now) == '1':
        # Grab the download link for the selected number
        ddl = query.download_link(choice)
        # Ask the user to download or not
        immediate_dl(query, choice, ddl)
    elif str(link_now) == '2':
        restart()


def immediate_dl(query: SteamUL, choice: int, ddl: str) -> None:
    """Ask the user whether they'd like to download the game immediately."""

    # Ask user whether the game should be downloaded or not
    print(f"Would you like to download '{query.results[choice]['name']}' now?")
    print("\t[1]\tY\n\t[2]\tN")
    flag = True
    while flag:
        try:
            dl_now = int(input("Selection:\t"))
            {1: 'one', 2: 'two'}[dl_now]
            flag = not(dl_now == 1 or dl_now == 2)
        except ValueError:
            print("Please enter the number beside your choice.")
        except KeyError:
            print("Please enter a valid number.")

    # If they choose to download immediately
    if str(dl_now) == '1':
        # Check for/create directory where the file will be saved
        if not os.path.exists("./SteamUL Downloads"):
            os.makedirs("./SteamUL Downloads")

        # Remove special characters from filename
        name = query.results[choice]['name']
        name = f"{name.replace(':', '-').replace('?', '-')}.zip"

        file_path = os.path.join("./SteamUL Downloads", name)

        # Save the file
        save_file(ddl, file_path)

        # Ask to unzip
        unzip_dl(query, choice, file_path)

        restart()

    # If not
    elif str(dl_now) == '2':
        restart()


def unzip_dl(query: SteamUL, choice: int, zip_path: Any) -> None:
    """Ask the user whether they'd like to unzip the download or not."""
    # Ask the user to unzip or not
    print(f"Would you like to unzip the download now?")
    print("\t[1]\tY\n\t[2]\tN")
    unzip_now = input("Selection:\t")

    # If they choose to unzip
    if str(unzip_now) == '1':
        # Check for/create directory where the zip contents will be saved
        if not os.path.exists("./SteamUL Games"):
            os.makedirs("./SteamUL Games")

        # Remove special characters from folder name
        name = query.results[choice]['name']
        name = f"{name.replace(':', '-').replace('?', '-')}"
        folder_path = os.path.join("./SteamUL Games", name)

        # Unzip the contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in tqdm(zip_ref.infolist(), desc='Extracting'):
                try:
                    zip_ref.extract(member, folder_path)
                except zipfile.error:
                    pass

        # Ask whether the zip archive should be deleted or not
        print(f"Would you like to delete the archive (.zip)?")
        print("\t[1]\tY\n\t[2]\tN")
        delete_now = input("Selection:\t")
        if str(delete_now) == '1':
            os.remove(zip_path)
            print('Deleted the archive')

    elif str(unzip_now) == '2':
        pass


def restart() -> None:
    """Ask the user whether they'd like to quit or return to the main menu."""
    choice = input("Press [1] to quit or [2] to return to the main menu...\t")
    if choice == '1':
        pass
    elif choice == '2':
        menu()


if __name__ == '__main__':
    pass
