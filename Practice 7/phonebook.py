import argparse
import csv
import sys
from pathlib import Path

import psycopg2
from psycopg2 import errorcodes

from connect import get_connection, initialize_database


def add_contact(first_name: str, phone: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
                (first_name.strip(), phone.strip()),
            )


def import_csv(csv_path: Path) -> int:
    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {"first_name", "phone"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain 'first_name' and 'phone' columns.")

        rows = []
        for line_number, row in enumerate(reader, start=2):
            first_name = (row.get("first_name") or "").strip()
            phone = (row.get("phone") or "").strip()
            if not first_name or not phone:
                raise ValueError(f"CSV line {line_number} has a blank name or phone.")
            rows.append((first_name, phone))

    if not rows:
        return 0

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)", rows
            )
    return len(rows)


def update_contact(phone: str, first_name: str | None = None,
                   new_phone: str | None = None) -> int:
    if first_name is None and new_phone is None:
        raise ValueError("Provide a new first name, a new phone, or both.")

    assignments = []
    values = []
    if first_name is not None:
        assignments.append("first_name = %s")
        values.append(first_name.strip())
    if new_phone is not None:
        assignments.append("phone = %s")
        values.append(new_phone.strip())
    values.append(phone.strip())

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE contacts SET {', '.join(assignments)} WHERE phone = %s",
                values,
            )
            return cursor.rowcount


def search_contacts(name: str | None = None,
                    phone_prefix: str | None = None) -> list[tuple]:
    clauses = []
    values = []
    if name:
        clauses.append("first_name ILIKE %s")
        values.append(f"%{name.strip()}%")
    if phone_prefix:
        clauses.append("phone LIKE %s")
        values.append(f"{phone_prefix.strip()}%")

    query = "SELECT id, first_name, phone, created_at FROM contacts"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY first_name, id"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.fetchall()


def delete_contacts(name: str | None = None,
                    phone: str | None = None) -> int:
    if not name and not phone:
        raise ValueError("Provide a contact name or phone number to delete.")
    clauses = []
    values = []
    if name:
        clauses.append("first_name = %s")
        values.append(name.strip())
    if phone:
        clauses.append("phone = %s")
        values.append(phone.strip())

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM contacts WHERE " + " AND ".join(clauses), values
            )
            return cursor.rowcount


def _show_contacts(contacts: list[tuple]) -> None:
    if not contacts:
        print("No contacts found.")
        return
    for contact_id, first_name, phone, _created_at in contacts:
        print(f"{contact_id}: {first_name} — {phone}")


def interactive_menu() -> None:
    initialize_database()
    actions = {
        "1": "Add a contact",
        "2": "Import contacts from CSV",
        "3": "Update a contact",
        "4": "Search/list contacts",
        "5": "Delete contacts",
        "0": "Exit",
    }
    while True:
        print("\nPhoneBook")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_contact(input("First name: "), input("Phone: "))
                print("Contact added.")
            elif choice == "2":
                path = Path(input("CSV path: ").strip())
                print(f"Imported {import_csv(path)} contact(s).")
            elif choice == "3":
                phone = input("Current phone number: ")
                first_name = input("New first name (blank to keep): ").strip()
                new_phone = input("New phone number (blank to keep): ").strip()
                count = update_contact(phone, first_name or None, new_phone or None)
                print(f"Updated {count} contact(s).")
            elif choice == "4":
                name = input("Name contains (blank to skip): ").strip()
                prefix = input("Phone starts with (blank to skip): ").strip()
                _show_contacts(search_contacts(name or None, prefix or None))
            elif choice == "5":
                name = input("Exact name (blank to skip): ").strip()
                phone = input("Exact phone (blank to skip): ").strip()
                count = delete_contacts(name or None, phone or None)
                print(f"Deleted {count} contact(s).")
            elif choice == "0":
                break
            else:
                print("Choose one of the listed options.")
        except (ValueError, FileNotFoundError) as error:
            print(f"Input error: {error}")
        except psycopg2.Error as error:
            # The connection context rolls back the current transaction on errors.
            if error.pgcode == errorcodes.UNIQUE_VIOLATION:
                print("That phone number is already in the PhoneBook.")
            else:
                print(f"Database error; the transaction was rolled back: {error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PostgreSQL-backed PhoneBook")
    parser.add_argument(
        "--import-csv", type=Path, metavar="FILE",
        help="import a CSV file with first_name,phone columns and exit",
    )
    args = parser.parse_args()
    try:
        initialize_database()
        if args.import_csv:
            print(f"Imported {import_csv(args.import_csv)} contact(s).")
        else:
            interactive_menu()
    except (ValueError, FileNotFoundError, psycopg2.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
