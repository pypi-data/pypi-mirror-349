import csv

def modifini(filename): 
    assert "." not in filename
    return "data/" + filename + ".csv"

def save_shield_to_file(shield,filename):
    fp = modifini(filename)

    with open(fp, 'w') as fi:
        wtr = csv.writer(fi,delimiter=',',lineterminator='\n')
        for s in shield:
            wtr.writerow(s)
    return

def load_shield_from_file(f):
    fp = modifini(f)
    q = []
    with open(fp, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            q.append([int(r) for r in row])
    return q