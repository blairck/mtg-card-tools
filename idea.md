# Overview

I would like to make a CLI tool which will provide a local space for managing tickets and searching the local codebase docstrings for related code. At a high level, a user would create a ticket describing some work, and then when they go to work on the ticket, the CLI shows relevant functions based on search of docstrings in the codebase.

## Components

There are 2 major components to this: the ticket management and the code search functionality. Both come together seemlessly to streamline work and make it simple for the user to find relevant code and pick up where they left off.

### Ticket Management

This component handles the creation, viewing, updating, and searching of tickets. Users can manage their work items efficiently, keeping track of the status, tags, comments, and recent activity associated with each ticket.

### Search

Users can search tickets by text and tags, and view tickets most recently updated. Creating a ticket, updating its status, and adding a comment all count as ticket updates.

### Code Search

This component allows users to search the local codebase for functions and methods related to the work described in their tickets. The search is based on docstrings (specifically `__doc__` attributes) on Python entities, providing a relevance score to help users quickly find the most pertinent code.

### Algorithm

The algorithm for searching the codebase involves the following steps:
1. Extract all Python entities with a `__doc__` attribute from the configured code directories.
2. Retrieve the `__doc__` attribute for each function or method.
3. Compute a relevance score by counting occurrences of each word from the ticket title and description in the entity name and docstring.
4. Rank the functions and methods by their relevance score.
5. Display the top results to the user, with VS Code links to the source code.

## Technical Details
The CLI tool will be implemented in Python and will use a local SQLite database stored as a `*.db` file at the repository root. Ticket IDs will be SQLite's simple incrementing integer IDs. A repository may have zero or one active ticket; attempts to activate a ticket must preserve this invariant. Tickets support `open`, `closed`, `cancelled`, and `active` statuses, and any status may be updated to any other status.

The code search functionality will leverage Python's `ast` module to parse the codebase and extract Python entities along with their docstrings. It will index lazily each time the user runs a search. The relevance scoring will use simple word-occurrence counts from the ticket title and description against entity names and docstrings.

This tool should be configurable in a configuration file, including specifying `src/` and `tests/` directories by default. Only these configured directories are searched.

The tool is designed to simplify the workflow for developers by providing an integrated environment for managing tickets and quickly finding relevant code in the local codebase. It aims to reduce context switching and improve productivity by keeping all necessary information and tools within the CLI. The tool should work offline for all functionality. The tool should have a small footprint and minimal dependencies to ensure ease of installation and use, as it will be part of a template repository for other projects to build on.

## User Stories

### View Active Ticket

Mockup 1:
```bash
Welcome to SimpleProjects
1) View active ticket
2) Create ticket
3) Update ticket status
4) Search tickets... # can search by "test & tags" or just "tags"
5) Search code
$ 1
```

Mockup 2:
```bash
Active ticket
Title: Add Foo Write API
Description: Add API; Update DB client with new Foo table; Add tests
Status: Active
Tags: foo, api
Comments:
- User, 9/3: Initial comment on the ticket
- User, 9/10: Follow-up comment on the ticket

Choose an option, or return to the main menu:
1) Find related code
2) Find related tickets
3) Update ticket status
4) Add comment
5) Return to main menu
$ 1
```

Mockup 3:
```bash
- Function: src.api.ReadFoo() # Clickable link
  score: 7 # = 2 (name) + 5 (docstring)
- Function: src.db.ReadFoo() # Clickable link
  score: 5 # = 2 (name) + 3 (docstring)
- Function: src.db.ReadFizz() # Clickable link
  score: 1 # = 0 (name) + 1 (docstring)

1) Back to ticket
2) Back to main menu
$ 2
```

### Create Ticket

Mockup 1:
```bash
Welcome to SimpleProjects
1) View active ticket
2) Create ticket
3) Update ticket status
4) Search tickets... # can search by "test & tags" or just "tags"
5) Search code
$ 2
```

Mockup 2:
```bash
Create a new ticket
Please enter the ticket title:
$ Test ticket
```

Mockup 3:
```bash
Please enter ticket description:
$ Test description
```

Mockup 4:
```bash
Please enter ticket status (open, closed, cancelled, or active):
$ open
```

Mockup 5:
```bash
Please enter ticket tags (comma-separated):
$ foo, bar
```

```bash
Choose an option, or return to save:
1) Save ticket
2) Cancel
$ 1
```

### Ticket Search and Recent Activity

The main menu provides ticket search by text and tags, plus a view of recently updated tickets. Search results and recent-activity entries display each ticket's integer ID so it can be selected for viewing or status updates.

## Text Color Guidance

General guidance for text color usage in the TUI:

- Blue: TUI text
- Green: Dates
- White: User authored text
- Yellow: Warnings or alert messages

## Open Questions

1. What information should the ticket-search results and recently updated ticket list display, beyond ID, title, status, tags, and last-updated time?
- This is fine.
2. Should tags be normalized (for example, trimmed and case-insensitive), and can a ticket have duplicate tags?
- Tags should be normalized to avoid duplicates and camel case formatting.
3. What author name should be recorded for comments in a fully offline, local-only tool?
- Just put "Me" as the author name.
4. How many code-search and recently updated ticket results should the CLI show by default, and should those views support pagination?
- The CLI should show 5 results by default, with no pagination currently (later results are omitted).
