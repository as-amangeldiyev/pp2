"""Extended PostgreSQL phonebook."""
import csv
import json
from datetime import date
from pathlib import Path

from connect import get_connection, initialize_database


def install() -> None:
    base = Path(__file__).resolve().parent
    with get_connection() as conn, conn.cursor() as cur:
        for name in ("procedures.sql",):
            cur.execute((base / name).read_text(encoding="utf-8"))


def contacts(group=None, email=None, sort="name", limit=20, offset=0):
    order = {"name": "c.first_name,c.surname,c.id", "birthday": "c.birthday NULLS LAST,c.first_name", "date": "c.created_at,c.id"}[sort]
    sql = f"""SELECT c.id,c.first_name,c.surname,c.email,c.birthday,g.name,c.created_at,
      COALESCE(jsonb_agg(jsonb_build_object('phone',p.phone,'type',p.type)) FILTER(WHERE p.id IS NOT NULL),'[]'::jsonb)
      FROM contacts c LEFT JOIN contact_groups g ON g.id=c.group_id LEFT JOIN phones p ON p.contact_id=c.id
      WHERE (%s IS NULL OR g.name=%s) AND (%s IS NULL OR c.email ILIKE %s)
      GROUP BY c.id,g.name ORDER BY {order} LIMIT %s OFFSET %s"""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (group, group, email, f"%{email}%" if email else None, limit, offset))
        return cur.fetchall()


def show(rows):
    for row in rows:
        print(row)


def browse():
    group = input("Group (blank for all): ").strip() or None
    email = input("Email contains (blank for all): ").strip() or None
    sort = input("Sort name/birthday/date [name]: ").strip() or "name"
    page, size = 0, 10
    while True:
        rows = contacts(group, email, sort, size, page * size)
        show(rows)
        action = input("next / prev / quit: ").strip().lower()
        if action == "next" and len(rows) == size: page += 1
        elif action == "prev": page = max(0, page - 1)
        elif action == "quit": break


def export_json(path):
    rows = contacts(limit=100000)
    data = [dict(id=r[0], name=r[1], surname=r[2], email=r[3], birthday=r[4].isoformat() if r[4] else None,
                 group=r[5], created_at=r[6].isoformat(), phones=r[7]) for r in rows]
    Path(path).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def import_json(path):
    for item in json.loads(Path(path).read_text(encoding="utf-8")):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE LOWER(first_name)=LOWER(%s)", (item['name'],))
            old = cur.fetchone()
            if old and input(f"{item['name']} exists: skip or overwrite? ").strip().lower() != 'overwrite': continue
            if old: cur.execute("DELETE FROM contacts WHERE id=%s", (old[0],))
            cur.execute("INSERT INTO contacts(first_name,surname,email,birthday,group_id) VALUES(%s,%s,%s,%s,(SELECT id FROM contact_groups WHERE name=%s)) RETURNING id",
                        (item['name'],item.get('surname'),item.get('email'),item.get('birthday'),item.get('group')))
            cid=cur.fetchone()[0]
            for phone in item.get('phones',[]): cur.execute("INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",(cid,phone['phone'],phone['type']))


def import_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("INSERT INTO contact_groups(name) VALUES(%s) ON CONFLICT(name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (row.get('group') or 'Other',))
                gid=cur.fetchone()[0]
                cur.execute("INSERT INTO contacts(first_name,surname,email,birthday,group_id) VALUES(%s,%s,%s,%s,%s) RETURNING id",(row['first_name'],row.get('surname'),row.get('email') or None,row.get('birthday') or None,gid))
                cur.execute("INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",(cur.fetchone()[0],row['phone'],row.get('phone_type') or 'mobile'))


def interactive_menu():
    while True:
        print("\nPhoneBook")
        print("1. Install database routines")
        print("2. Search contacts")
        print("3. Browse and filter contacts")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Import contacts from CSV")
        print("7. Import contacts from JSON")
        print("8. Export contacts to JSON")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "0":
                break
            if choice == "1":
                install()
                print("Database routines installed.")
            elif choice == "2":
                query = input("Search name, email, or phone: ")
                with get_connection() as conn, conn.cursor() as cur:
                    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                    show(cur.fetchall())
            elif choice == "3":
                browse()
            elif choice == "4":
                with get_connection() as conn, conn.cursor() as cur:
                    cur.execute("CALL add_phone(%s,%s,%s)",
                                (input("Contact name: "), input("Phone: "), input("Type (home/work/mobile): ")))
                print("Phone added.")
            elif choice == "5":
                with get_connection() as conn, conn.cursor() as cur:
                    cur.execute("CALL move_to_group(%s,%s)", (input("Contact name: "), input("Group: ")))
                print("Contact moved.")
            elif choice == "6":
                import_csv(input("CSV file path: ").strip())
                print("CSV imported.")
            elif choice == "7":
                import_json(input("JSON file path: ").strip())
                print("JSON imported.")
            elif choice == "8":
                export_json(input("Output JSON file: ").strip())
                print("JSON exported.")
            else:
                print("Choose one of the listed options.")
        except (ValueError, KeyError, FileNotFoundError) as error:
            print(f"Input or file error: {error}")


def main():
    initialize_database()
    interactive_menu()

if __name__=='__main__': main()
