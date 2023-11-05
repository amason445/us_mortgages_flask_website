import csv
from io import StringIO

def generate_dummy_csv():

    x = list(range(0, 100))
    y = list(range(0, 200, 2))

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['X', 'Y'])

    for i, j in zip(x, y):
        writer.writerow([i, j])

    output.seek(0)

    return output.getvalue()