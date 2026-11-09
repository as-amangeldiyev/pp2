"""Small command-line examples for the Practice 8 PostgreSQL routines."""
import argparse
import csv
import json
from pathlib import Path

from connect import get_connection, initialize_database


def install_routines() -> None:
    base = Path(__file__).resolve().parent
    with get_connection() as conn, conn.cursor() as cursor:
        for filename in ("functions.sql", "procedures.sql"):
            cursor.execute((base / filename).read_text(encoding="utf-8"))


def search(pattern: str) -> list[tuple]:
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM find_contacts(%s)", (pattern,))
        return cursor.fetchall()


def page(limit: int, offset: int) -> list[tuple]:
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        return cursor.fetchall()


def upsert(name: str, phone: str, surname: str | None = None) -> None:
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("CALL upsert_contact(%s, %s, %s)", (name, phone, surname))


def import_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {"name", "phone"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain 'name' and 'phone' columns.")
        names, phones = [], []
        for row in reader:
            names.append(row.get("name") or "")
            phones.append(row.get("phone") or "")
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            "CALL upsert_contacts_batch(%s, %s, %s)",
            (names, phones, "[]"),
        )
        invalid_json = cursor.fetchone()[0]
    return invalid_json if isinstance(invalid_json, list) else json.loads(invalid_json)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("install", help="install the functions and procedures")
    add = commands.add_parser("add", help="insert or update one contact")
    add.add_argument("name")
    add.add_argument("phone")
    add.add_argument("--surname")
    find = commands.add_parser("search", help="search name, surname, or phone")
    find.add_argument("pattern")
    listing = commands.add_parser("page", help="list one page of contacts")
    listing.add_argument("--limit", type=int, default=20)
    listing.add_argument("--offset", type=int, default=0)
    batch = commands.add_parser("import-csv", help="bulk upsert name,phone rows")
    batch.add_argument("file", type=Path)
    delete = commands.add_parser("delete", help="delete by username or phone")
    delete.add_argument("--username")
    delete.add_argument("--phone")
    args = parser.parse_args()

    initialize_database()
    if args.command == "install":
        install_routines()
    elif args.command == "add":
        upsert(args.name, args.phone, args.surname)
    elif args.command == "search":
        print(*search(args.pattern), sep="\n")
    elif args.command == "page":
        print(*page(args.limit, args.offset), sep="\n")
    elif args.command == "import-csv":
        print(json.dumps(import_csv(args.file), ensure_ascii=False, indent=2))
    elif args.command == "delete":
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute("CALL delete_contacts(%s, %s)", (args.username, args.phone))


if __name__ == "__main__":
    main()
