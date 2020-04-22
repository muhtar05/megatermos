import xlrd
book = xlrd.open_workbook("termos.xls")
sh = book.sheet_by_index(0)
print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=5)))

categories = set()
for rx in range(sh.nrows):
    if rx == 0:
        continue
    curr_cat = sh.cell_value(rowx=rx, colx=5)
    categories.add(curr_cat)

for category in categories:
    print(category)
