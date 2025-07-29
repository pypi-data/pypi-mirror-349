import FreeSimpleGUI as sg
import json
from jsonpath_ng.ext import parse # jsonpath_ng.jsonpath was unused

# Helper function to get all item IDs from the Treeview widget
def get_all_tree_item_ids(tree_widget, parent=''):
    ids = []
    if not tree_widget: # Check if the widget exists
        return ids
    try:
        for child_id in tree_widget.get_children(parent):
            ids.append(child_id)
            ids.extend(get_all_tree_item_ids(tree_widget, child_id))
    except Exception: # Catch any potential errors if widget is not fully initialized or empty
        pass
    return ids

def create_main_window():
    """Creates the main window layout."""

    left_column = [
        # Removed JSON Input/File Path and Browse button
        [sg.Text("JSON Input:")], # Changed label
        [sg.Multiline(key="-LEFT_PANE-", size=(60, 20), expand_x=True, expand_y=True, enable_events=True)],
        [sg.Button("Pretty JSON", key="-PRETTY_JSON-", expand_x=True)], # Added Pretty JSON button
        [sg.Text("Status:", key="-STATUS_LEFT-")]
    ]

    right_column = [
        [sg.Text("JSON Tree View:")],
        [sg.Tree(data=sg.TreeData(), headings=['Value'], key='-TREE-', show_expanded=False, col0_width=30, auto_size_columns=False, num_rows=20, expand_x=True, expand_y=True)],
        [sg.Text("JSONPath Filter:"), sg.InputText(key="-JSONPATH_FILTER-", enable_events=True, expand_x=True), sg.Button("?", key="-JSONPATH_HELP-", size=(2,1)), sg.Button("Apply Filter", key="-APPLY_FILTER-")], # Added Help button
        [sg.Button("Expand All", key="-EXPAND_ALL-"), sg.Button("Collapse All", key="-COLLAPSE_ALL-")], # Added Expand/Collapse buttons
        [sg.Text("Status:", key="-STATUS_RIGHT-")]
    ]

    layout = [
        [
            sg.Column(left_column, element_justification='left', expand_x=True, expand_y=True),
            sg.VSeperator(),
            sg.Column(right_column, element_justification='left', expand_x=True, expand_y=True),
        ]
    ]
    return sg.Window("PySimpleJSONViewer", layout, resizable=True, finalize=True, size=(1200, 800), element_justification='left', margins=(10, 10), keep_on_top=False)

# Removed load_json_or_jsonl function as it's no longer used

def update_tree(tree_element, json_data):
    """Updates the Tree element with JSON data."""
    treedata = sg.TreeData()

    def add_nodes(parent_key, data):
        if isinstance(data, dict):
            for key, value in data.items():
                node_key = f"{parent_key}.{key}" if parent_key else key
                treedata.Insert(parent_key, node_key, key, values=[str(value) if not isinstance(value, (dict, list)) else ''])
                add_nodes(node_key, value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                node_key = f"{parent_key}[{i}]"
                treedata.Insert(parent_key, node_key, f"[{i}]", values=[str(item) if not isinstance(item, (dict, list)) else ''])
                add_nodes(node_key, item)

    if json_data:
        add_nodes('', json_data)
    tree_element.update(values=treedata)

def main():
    window = create_main_window()
    current_json_data = None
    # Removed full_jsonl_content, is_jsonl, total_jsonl_lines

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # Removed event == "-JSON_INPUT-" block

        elif event == "-LEFT_PANE-" and values["-LEFT_PANE-"]:
            left_pane_content = values["-LEFT_PANE-"]
            try:
                json_data = json.loads(left_pane_content)
                current_json_data = json_data
                update_tree(window['-TREE-'], current_json_data)
                window["-STATUS_RIGHT-"].update("Tree view updated from manual input.")
                window["-STATUS_LEFT-"].update("Interpreted as single JSON from input pane.")
            except json.JSONDecodeError:
                current_json_data = None
                update_tree(window['-TREE-'], None)
                window["-STATUS_RIGHT-"].update("Error: Invalid JSON in input pane.")
                window["-STATUS_LEFT-"].update("Error: Invalid JSON in input pane.")

        elif event == "-PRETTY_JSON-":
            left_pane_content = values["-LEFT_PANE-"]
            if not left_pane_content.strip():
                window["-STATUS_LEFT-"].update("Input is empty. Nothing to format.")
                sg.popup_quick_message("Input is empty.", auto_close_duration=2, background_color='yellow', text_color='black')
                continue
            try:
                json_data = json.loads(left_pane_content)
                pretty_json_str = json.dumps(json_data, indent=4)
                window["-LEFT_PANE-"].update(pretty_json_str)
                current_json_data = json_data # Keep current_json_data in sync
                update_tree(window['-TREE-'], current_json_data) # Update tree as well
                window["-STATUS_LEFT-"].update("JSON formatted.")
                window["-STATUS_RIGHT-"].update("Tree view updated.")
            except json.JSONDecodeError:
                window["-STATUS_LEFT-"].update("Error: Invalid JSON. Cannot format.")
                sg.popup_error("Invalid JSON. Cannot format.", title="Format Error")

        elif event == "-JSONPATH_HELP-":
            help_text = """JSONPath Extended Syntax Help (jsonpath-ng.ext)

Basic Selectors:
  $.store.book[*].author  - All authors of books in the store
  $..author               - All authors (recursive descent)
  $.store.book[0]         - First book
  $.store.book[-1]        - Last book (from the end)

Slices (for arrays):
  $.store.book[0:2]       - First two books (index 0 and 1)
  $.store.book[:2]        - First two books
  $.store.book[1:]        - All books from index 1 onwards
  $.store.book[-2:]       - Last two books

Filter Expressions (using '@' for the current object):
  $.store.book[?(@.price < 10)]     - Books cheaper than 10
  $.store.book[?(@.isbn)]           - Books that have an 'isbn' key
  $.store.book[?(@.category == 'fiction')] - Fiction books
  $.store.book[?(@.author == 'Nigel Rees' && @.price > 5)] 
                                  - Books by Nigel Rees costing > 5
  $.store.book[?(@.title =~ /lord/i)] - Books with 'lord' in title (case-insensitive regex)
                                     (Requires jsonpath-ng's RegexComparison extension if not default)

Union / Multiple Indices (for arrays):
  $.store.book[0,2]       - First and third book
  $.store.book[(@.length-1)] - Typically, use `[-1]` for the last element.
                                This form might be for specific cases.

Wildcard:
  $.store.book[*].title   - Titles of all books
  $.store.*                 - All direct children (values) of 'store' object
  $..*                      - All values recursively from root

Notes:
- The '@' symbol refers to the current node being processed within a filter expression.
- String literals in comparisons should be single or double-quoted (e.g., 'fiction').
- For more complex queries or specific operator details (like regex support), refer to the jsonpath-ng library documentation.
"""
            sg.popup_scrolled(help_text, title="JSONPath Help", size=(80, 25), font=("Courier New", 10))

        elif event == "-EXPAND_ALL-":
            if window['-TREE-'].Widget:
                all_ids = get_all_tree_item_ids(window['-TREE-'].Widget)
                for item_id in all_ids:
                    try:
                        window['-TREE-'].Widget.item(item_id, open=True)
                    except Exception: # In case an ID is stale or invalid
                        pass
                window["-STATUS_RIGHT-"].update("Tree expanded.")
            else:
                window["-STATUS_RIGHT-"].update("Tree widget not available.")

        elif event == "-COLLAPSE_ALL-":
            if window['-TREE-'].Widget:
                all_ids = get_all_tree_item_ids(window['-TREE-'].Widget)
                # Iterate reversed or just all; for collapsing, order might not be critical
                # but often parents are collapsed first in UIs.
                # Collapsing children first then parent, or all at once.
                # Let's try collapsing all directly.
                for item_id in reversed(all_ids): # Reversed to collapse deepest first
                    try:
                        window['-TREE-'].Widget.item(item_id, open=False)
                    except Exception:
                        pass
                window["-STATUS_RIGHT-"].update("Tree collapsed.")
            else:
                window["-STATUS_RIGHT-"].update("Tree widget not available.")


        elif event == "-APPLY_FILTER-" and current_json_data:
            jsonpath_expr_str = values["-JSONPATH_FILTER-"]
            if jsonpath_expr_str:
                try:
                    jsonpath_expr = parse(jsonpath_expr_str)
                    matches = [match.value for match in jsonpath_expr.find(current_json_data)]
                    if matches:
                        # Displaying filtered results: for simplicity, show the first match or list of matches
                        # A more complex UI might be needed for multiple matches.
                        filtered_data_to_display = matches[0] if len(matches) == 1 else matches
                        # We need a way to show this. For now, let's try to update the tree with it.
                        # This might not always be a dict/list, so tree update might fail.
                        update_tree(window['-TREE-'], filtered_data_to_display)
                        window["-STATUS_RIGHT-"].update(f"Filter applied. Showing {len(matches)} match(es).")
                    else:
                        update_tree(window['-TREE-'], {"message": "No matches found for filter."})
                        window["-STATUS_RIGHT-"].update("Filter applied. No matches found.")
                except Exception as e:
                    sg.popup_error(f"Invalid JSONPath expression: {e}", title="Filter Error")
                    window["-STATUS_RIGHT-"].update("Error: Invalid JSONPath expression.")
            else: # No filter, show original tree
                update_tree(window['-TREE-'], current_json_data)
                window["-STATUS_RIGHT-"].update("Filter cleared. Showing full tree.")

    window.close()

# if __name__ == "__main__":
#     main()
