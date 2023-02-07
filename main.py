""" This is the main file of the project. It contains the main function and the switcharray. """
import os

from functions import (
    boardfunctions,
    cardChecklistFunctions,
    cardfunctions,
    clienttoken,
    listfunctions,
    voiceassistant,
)

# vaname = greetUser.VANAME


def using_switcharray():
    """
    This function is the main function of the project. It contains the switcharray.
    """
    # A dictionary.
    switcharray = {
        "add board": boardfunctions.add_board,
        "update board name": boardfunctions.update_board_name,
        "delete board": boardfunctions.close_and_archive_board,
        "add list": listfunctions.add_list,
        "update list name": listfunctions.update_list_name,
        "archive list": listfunctions.archive_list,
        "add card": cardfunctions.add_card,
        "open card": cardfunctions.open_card,
        "update card name": cardfunctions.update_card_name,
        "delete card": cardfunctions.delete_card,
        "add check list": cardChecklistFunctions.add_checklist_item,
        "open trello": boardfunctions.open_trello,
        "exit": exit,
    }

    query = voiceassistant.takecommand().lower()

    if query in switcharray:
        switcharray[query](clienttoken.CLIENT)
    else:
        voiceassistant.speak("Sorry, I didn't understand that")


# A way to run the main function only when you want to run the script directly.
if __name__ == "__main__":

    def clear():
        """This function clears the terminal."""
        return os.system("cls")

    clear()
    # greetUser.wishMe()
    # greetUser.username()

    while True:
        using_switcharray()
