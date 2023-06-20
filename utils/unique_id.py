import csv
import random
import sys
from string import ascii_lowercase, digits


def generate_unique_id(id: int, zfill: int = 0) -> str:
    random_str = ''.join(random.choices(ascii_lowercase + digits, k=6))
    id_leading_zeros = str(id).zfill(zfill)
    unique_id = f"{id_leading_zeros}-{random_str}"
    return unique_id


def main() -> int:

    with open(sys.argv[1], 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        rows = [row for row in reader]
        n_unique_ids = len(set([row['id'] for row in rows]))
        zfill = len(str(n_unique_ids)) if len(str(n_unique_ids)) > 2 else 2
        for row in rows:
            row['uid'] = generate_unique_id(int(row['id']), zfill)
            print(row['uid'])

    with open('new.csv', 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=['id', 'uid'] + \
                                [key for key in rows[0].keys() if key != 'id'])
        writer.writeheader()
        writer.writerows(rows)

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
