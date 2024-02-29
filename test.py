file = open('zip_codes.txt')

zip_codes = [f.strip() for f in file.readlines()]

for zip_code in zip_codes:
    state,zip_code = zip_code.split(',')
    print(state,zip_code)