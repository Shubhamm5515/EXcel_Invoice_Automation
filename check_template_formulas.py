"""
Check which cells in the template have formulas
"""
import openpyxl

template_path = 'inn sample.xlsx'
wb = openpyxl.load_workbook(template_path)
ws = wb.active

print("=" * 80)
print("CELLS WITH FORMULAS IN TEMPLATE")
print("=" * 80)

formula_cells = []

# Check all cells in the used range
for row in ws.iter_rows(min_row=1, max_row=50, min_col=1, max_col=10):
    for cell in row:
        if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
            formula_cells.append({
                'cell': cell.coordinate,
                'formula': cell.value
            })
            print(f"{cell.coordinate}: {cell.value}")

print("\n" + "=" * 80)
print(f"TOTAL FORMULA CELLS: {len(formula_cells)}")
print("=" * 80)

print("\n" + "=" * 80)
print("CELLS WE SHOULD NOT OVERWRITE:")
print("=" * 80)
for fc in formula_cells:
    print(f"  {fc['cell']}: {fc['formula']}")

wb.close()
