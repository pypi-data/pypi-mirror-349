import re
from IPython.display import display, HTML

def display_highlighted_words(df, keywords):
    """\
    Display a DataFrame with highlighted keywords.

    Parameters
    ----------
    df
        The DataFrame to be displayed.
    keywords
        The list of keywords to be highlighted.

    Returns
    -------
        The displayed DataFrame with highlighted keywords.
    """
    # Build the table header
    head = """
    <table>
        <thead>
            <tr>""" + "".join([f"<th>{c}</th>" for c in df.columns]) + """
            </tr>
        </thead>
    <tbody>"""
    
    # Iterate over the rows of the DataFrame
    for i, r in df.iterrows():
        row = "<tr>"
        for c in df.columns:
            # Find all keyword matches in the current cell value
            matches = []
            for k in keywords:
                for match in re.finditer(k, str(r[c])):
                    matches.append(match)
            
            # Reverse sort matches by their starting position
            matches = sorted(matches, key=lambda x: x.start(), reverse=True)
            
            # Build HTML for the current cell
            cell = str(r[c])
            for match in matches:
                cell = cell[:match.start()] + \
                    f"<span style='color:red;'>{cell[match.start():match.end()]}</span>" + \
                    cell[match.end():]
            
            row += f"<td>{cell}</td>"
        
        row += "</tr>"
        head += row
    
    # Close table and display the result
    head += "</tbody></table>"
    display(HTML(head))

def highlight_nodes(obj, node):
    """\
    Highlight the nodes in the obj.paths DataFrame.

    Parameters
    ----------
    obj
        The VerkkoFillet object.
    node
        The node to be highlighted.

    Returns
    -------
        The all paths containing the node.
    """
    # df = obj.paths.loc[obj.paths['path'].str.contains(node), ['name','path']]
    df = obj.paths.loc[obj.paths['path'].str.contains(node, na=False , regex=False), ['name', 'path']]


    return display_highlighted_words(df, [node])