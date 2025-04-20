# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Nick Riazi
# ncriazi@uci.edu
# 14622762
import shlex
from pathlib import Path
from notebook import Notebook, Diary
from typing import List, Dict, Union

def parse_command(command_list: List[str], state: Dict[str, Union[str, Notebook]]) -> None:
    """Parses and dispatches commands based on user input."""
    command = command_list[0]

    if command == "C":
        handle_create(command_list)
    elif command == "D":
        handle_delete(command_list)
    elif command == "O":
        handle_open(command_list, state)
    elif command == "E":
        handle_edit(command_list, state)
    elif command == "P":
        handle_print(command_list, state)
    else:
        print("ERROR")

def handle_create(command_list: List[str]) -> None:
    """Handles the 'C' command: create a new notebook."""
    try:
        path = command_list[1]

        if "-n" not in command_list:
            print("ERROR")
            return

        name_index = command_list.index("-n") + 1
        notebook_name = command_list[name_index]

        dir_path = Path(path)
        file_path = dir_path / f"{notebook_name}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.exists():
            print("ERROR")
            return

        username = input()
        password = input()
        bio = input()
        nb = Notebook(username, password, bio)

        nb.save(file_path)
        print(f'{file_path.resolve()} CREATED')

    except Exception:
        print("ERROR")

def handle_delete(command_list: List[str]) -> None:
    """Handles the 'D' command: delete a notebook file."""
    try:
        file_path = Path(command_list[1])
        if file_path.suffix != ".json" or not file_path.exists():
            print("ERROR")
            return

        file_path.unlink()
        print(f'{file_path.resolve()} DELETED')
    except Exception:
        print("ERROR")

def handle_open(command_list: List[str], state: Dict[str, Union[str, Notebook]]) -> None:
    """Handles the 'O' command: open a notebook."""
    try:
        file_path = Path(command_list[1])
        if file_path.suffix != ".json" or not file_path.exists():
            print("ERROR")
            return

        nb = Notebook("x", "x", "x")
        nb.load(file_path)

        user = input()
        password = input()

        if nb.username != user or nb.password != password:
            print("ERROR")
            return

        state["notebook"] = nb
        state["path"] = file_path
        print("Notebook loaded.")
        print(nb.username)
        print(nb.bio)
    except Exception:
        print("ERROR")

def handle_edit(command_list: List[str], state: Dict[str, Union[str, Notebook]]) -> None:
    """Handles the 'E' command: edit notebook contents."""
    notebook = state.get("notebook")
    path = state.get("path")

    if notebook is None or path is None:
        print("ERROR")
        return

    i = 1
    while i < len(command_list):
        try:
            if command_list[i] == "-usr":
                notebook.username = command_list[i + 1]
                i += 2
            elif command_list[i] == "-pwd":
                notebook.password = command_list[i + 1]
                i += 2
            elif command_list[i] == "-bio":
                notebook.bio = command_list[i + 1]
                i += 2
            elif command_list[i] == "-add":
                diary = Diary(command_list[i + 1])
                notebook.add_diary(diary)
                i += 2
            elif command_list[i] == "-del":
                index = int(command_list[i + 1])
                if not notebook.del_diary(index):
                    print("ERROR")
                    return
                i += 2
            else:
                print("ERROR")
                return
        except Exception:
            print("ERROR")
            return

    notebook.save(path)

def handle_print(command_list: List[str], state: Dict[str, Union[str, Notebook]]) -> None:
    """Handles the 'P' command: print notebook contents."""
    notebook = state.get("notebook")
    if notebook is None:
        print("ERROR")
        return

    i = 1
    while i < len(command_list):
        option = command_list[i]

        if option == "-usr":
            print(notebook.username)
        elif option == "-pwd":
            print(notebook.password)
        elif option == "-bio":
            print(notebook.bio)
        elif option == "-diaries":
            for idx, diary in enumerate(notebook._diaries):
                print(f"{idx}: {diary.entry}")
        elif option == "-diary":
            i += 1
            if i >= len(command_list):
                print("ERROR")
                return
            try:
                diary_id = int(command_list[i])
                if 0 <= diary_id < len(notebook._diaries):
                    print(notebook._diaries[diary_id].entry)
                else:
                    print("ERROR")
                    return
            except ValueError:
                print("ERROR")
                return
        elif option == "-all":
            print(notebook.username)
            print(notebook.password)
            print(notebook.bio)
            for idx, diary in enumerate(notebook._diaries):
                print(f"{idx}: {diary.entry}")
        else:
            print("ERROR")
            return

        i += 1
            