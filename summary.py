
import csv


# 1. Read data from CSV
def read_rows(filename):
    with open(filename, encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


# 2. Clean numeric values
def clean_values(rows, column):
    values = []

    for row in rows:
        raw = row.get(column, "")

        if raw is None:
            continue

        raw = raw.strip()

        if raw in ("", "NA", "N/A", "-"):
            continue

        raw = raw.replace(",", "")

        try:
            values.append(float(raw))
        except ValueError:
            continue

    return values


# 3. Calculate summary statistics
def summarise(values):
    if len(values) == 0:
        return {
            "count": 0,
            "smallest": None,
            "largest": None,
            "average": None
        }

    return {
        "count": len(values),
        "smallest": min(values),
        "largest": max(values),
        "average": sum(values) / len(values)
    }


# 4. Summarise multiple columns
def summarise_all(filename, columns):
    rows = read_rows(filename)

    report = {}

    for column in columns:
        values = clean_values(rows, column)
        report[column] = summarise(values)

    return report


# 5. Run the analysis
if __name__ == "__main__":

    filename = "ALFA_PROJ.csv"

    columns = [
        "E",
        "N"
    ]

    report = summarise_all(filename, columns)

    for column, stats in report.items():
        print(f"\n{column}")
        print("-------------------")
        print("Count:", stats["count"])
        print("Smallest:", stats["smallest"])
        print("Largest:", stats["largest"])
        print("Average:", stats["average"])
