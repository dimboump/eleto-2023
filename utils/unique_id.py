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
    ret = 0
    file = sys.argv[1]
    file_no_ext, file_ext = file.rsplit('.', 1)

    if file_ext not in {'csv', 'tsv'}:
        raise ValueError(f"File extension must be csv or tsv, not {file_ext}.")

    out_file = f"{file_no_ext}_unique.{file_ext}"

    with open(file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in,
                                delimiter='\t' if file_ext == 'tsv' else ',')
        rows = [row for row in reader]
        n_unique_ids = len(set([row['id'] for row in rows]))
        zfill = len(str(n_unique_ids)) if len(str(n_unique_ids)) > 2 else 2
        for row in rows:
            row['uid'] = generate_unique_id(int(row['id']), zfill)
            print(row['uid'])

    try:
        with open(out_file, 'w', encoding='utf-8', newline='') as f_out:
            fields = ['id', 'uid'] + [k for k in rows[0].keys() if k != 'id']
            writer = csv.DictWriter(f_out, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    except IOError as e:
        print(f"Error writing to file: {e}")
        ret |= 1

    return ret

if __name__ == '__main__':
    raise SystemExit(main())
