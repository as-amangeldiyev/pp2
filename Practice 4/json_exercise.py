import json

with open("sample-data.json", encoding="utf-8") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 88)
print(f"{'DN':<50} {'Description':<20} {'Speed':>6} {'MTU':>6}")
print(f"{'-' * 50} {'-' * 20} {'-' * 6} {'-' * 6}")

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    print(
        f"{attributes['dn']:<50} {attributes['descr']:<20} "
        f"{attributes['speed']:>6} {attributes['mtu']:>6}"
    )
