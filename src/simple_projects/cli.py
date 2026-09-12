"""Interactive command-line interface for Simple Projects."""

from __future__ import annotations

import argparse
from pathlib import Path

from .code_search import CodeResult, search_code
from .tickets import STATUSES, Ticket, TicketStore


def main() -> None:
    """Run the interactive Simple Projects command-line interface."""
    parser = argparse.ArgumentParser(description="Offline tickets and Python code search.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository to manage (default: current directory).")
    arguments = parser.parse_args()
    store = TicketStore(arguments.root.resolve())
    store.initialize()
    _menu(store, arguments.root.resolve())


def _menu(store: TicketStore, repository_root: Path) -> None:
    while True:
        print("\nSimple Projects\n1) View active ticket\n2) Create ticket\n3) Update ticket status\n4) Search tickets\n5) Search code\n6) Recently updated tickets\n0) Exit")
        choice = input("$ ").strip()
        try:
            if choice == "1":
                _view_active_ticket(store, repository_root)
            elif choice == "2":
                _create_ticket(store)
            elif choice == "3":
                _update_status(store)
            elif choice == "4":
                _show_tickets(store.search_tickets(input("Search text or tag: ")))
            elif choice == "5":
                _show_code_results(search_code(repository_root, input("Search code: ")))
            elif choice == "6":
                _show_tickets(store.recent_tickets())
            elif choice == "0":
                return
            else:
                print("Choose a listed option.")
        except ValueError as error:
            print(f"Warning: {error}")


def _create_ticket(store: TicketStore) -> None:
    title = input("Title: ")
    description = input("Description: ")
    status = input(f"Status ({', '.join(sorted(STATUSES))}): ").strip().lower()
    tags = input("Tags (comma-separated): ")
    ticket = store.create_ticket(title, description, status, tags)
    print(f"Created ticket #{ticket.id}.")


def _update_status(store: TicketStore) -> None:
    ticket_id = int(input("Ticket ID: "))
    status = input(f"Status ({', '.join(sorted(STATUSES))}): ").strip().lower()
    print(f"Updated ticket #{store.update_status(ticket_id, status).id}.")


def _view_active_ticket(store: TicketStore, repository_root: Path) -> None:
    ticket = store.active_ticket()
    if ticket is None:
        print("No active ticket.")
        return
    print(f"\n#{ticket.id}: {ticket.title}\n{ticket.description}\nStatus: {ticket.status}\nTags: {', '.join(ticket.tags)}")
    print("1) Find related code\n2) Update ticket status\n3) Add comment\n0) Back")
    choice = input("$ ").strip()
    if choice == "1":
        _show_code_results(search_code(repository_root, f"{ticket.title} {ticket.description}"))
    elif choice == "2":
        status = input(f"Status ({', '.join(sorted(STATUSES))}): ").strip().lower()
        store.update_status(ticket.id, status)
    elif choice == "3":
        store.add_comment(ticket.id, input("Comment: "))


def _show_tickets(tickets: list[Ticket]) -> None:
    if not tickets:
        print("No tickets found.")
    for ticket in tickets:
        print(f"#{ticket.id} [{ticket.status}] {ticket.title} ({', '.join(ticket.tags)})")


def _show_code_results(results: list[CodeResult]) -> None:
    if not results:
        print("No code results found.")
    for result in results:
        print(f"{result.name} - score: {result.score}\n  {result.vscode_link}")


if __name__ == "__main__":
    main()