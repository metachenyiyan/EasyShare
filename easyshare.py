import csv
import argparse

def get_sheet(file_path):
    rows = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        _ = next(reader)
        for row in reader:
            rows.append(row)
    return rows

def get_group2debt(sheet):
    nb_group = (len(sheet[0]) - 2) // 2
    group2paid = [0.]*nb_group
    group2received = [0.]*nb_group
    group2debt = [0.]* nb_group
    for row in sheet:
        price = float(row[1])
        ponderations = [0. if w=="" else float(w) for w in row[2:]]

        w_paid_ttl = sum(ponderations[:nb_group])
        for id_g in range(nb_group):
            group2paid[id_g] += price*ponderations[id_g]/w_paid_ttl

        w_rece_ttl = sum(ponderations[nb_group:2*nb_group])
        for id_g in range(nb_group):
            group2received[id_g] += price*ponderations[nb_group+id_g]/w_rece_ttl

    for id_g in range(nb_group):
        group2debt[id_g] = group2received[id_g] - group2paid[id_g]
    return group2debt


def get_transition_policy(group2paid, group2received):
    pass






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="csv file path",
        type=str
    )

    args = parser.parse_args()
    sheet = get_sheet(args.file)
    group2debt = get_group2debt(sheet)
    assert abs(sum(group2debt)) < 1e-6
    print(group2debt)
