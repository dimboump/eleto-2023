import csv
import os
import random
import sys
from string import ascii_lowercase
from string import digits
from typing import Dict
from typing import List

Row = Dict[str, str]


def generate_unique_id(id: int, zfill: int = 0) -> str:
    random_str = ''.join(random.choices(ascii_lowercase + digits, k=6))
    id_leading_zeros = str(id).zfill(zfill)
    unique_id = f"{id_leading_zeros}-{random_str}"
    return unique_id


def read_csv(file: str, delim: str) -> List[Row]:
    with open(file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in, delimiter=delim)
        rows = [row for row in reader]
    return rows


def count_unique_ids(rows: List[Row]) -> int:
    n_unique_ids = len(set([row['id'] for row in rows]))
    return n_unique_ids


def get_zfill(n: int) -> int:
    zfill = len(str(n)) if len(str(n)) > 2 else 2
    return zfill


def add_unique_ids(rows: List[Row], zfill: int) -> List[Row]:
    for row in rows:
        row['uid'] = generate_unique_id(int(row['id']), zfill)
        print(row['uid'])
    return rows


def write_csv(rows: List[Row], out_file: str, delim: str) -> None:
    with open(out_file, 'w', encoding='utf-8', newline='') as f_out:
        fields = ['id', 'uid'] + [k for k in rows[0].keys()
                                  if k not in {'id', 'uid'}]
        writer = csv.DictWriter(f_out, fieldnames=fields, delimiter=delim)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    retv = 0
    file = sys.argv[1]
    file_no_ext, file_ext = file.rsplit('.', 1)

    if file_ext not in {'csv', 'tsv'}:
        raise ValueError(f"File extension must be csv or tsv, not {file_ext}.")

    delim = '\t' if file_ext == 'tsv' else ','
    out_file = f"{file_no_ext}_unique.{file_ext}"

    rows = read_csv(file, delim)
    n_unique_ids = count_unique_ids(rows)
    zfill = get_zfill(n_unique_ids)
    rows = add_unique_ids(rows, zfill)

    if os.path.exists(out_file):
        os.remove(out_file)

    try:
        write_csv(rows, out_file, delim)
    except IOError as e:
        print(f"Error writing to file: {e}")
        retv |= 1

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
