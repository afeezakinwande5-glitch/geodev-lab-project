import csv


def inspect_column(filename, column):

    with open(filename, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    values = []

    for row in rows:

        raw = row[column].strip()

        if raw in ("", "NA", "N/A", "-"):
            continue

        raw = raw.replace(",", "")

        try:
            values.append(float(raw))
        except ValueError:
            continue

    if len(values) == 0:
        return {
            "smallest": None,
            "largest": None,
            "count": 0
        }

    return {
        "smallest": min(values),
        "largest": max(values),
        "count": len(values)
    }


# Inspect two columns

area_result = inspect_column("mydata.csv", "area_km2")

pop_result = inspect_column("mydata.csv", "population")


print("Area:", area_result)

print("Population:", pop_result)