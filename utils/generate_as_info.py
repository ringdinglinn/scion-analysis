from utils import io

def build_as_to_country(input_path, output_path):
    org_to_country = {}
    as_records = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            fields = line.split("|")

            # Organization records: org_id|changed|org_name|country|source
            if len(fields) == 5:
                org_id = fields[0]
                country = fields[3]
                org_to_country[org_id] = country

            # AUT records: aut|changed|aut_name|org_id|opaque_id|source
            elif len(fields) == 6:
                aut = fields[0]
                org_id = fields[3]
                as_records.append((aut, org_id))

    # Write AS → country mapping
    with open(output_path, "w", encoding="utf-8") as out:
        for aut, org_id in as_records:
            country = org_to_country.get(org_id)
            if country:
                out.write(f"{aut}|{country}\n")
            # Optional: else write UNKNOWN or skip (currently skips)

if __name__ == "__main__":
    inp = io.user_input_path()
    outp = io.user_input()
    build_as_to_country(inp, outp)
