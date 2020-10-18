from pathlib import Path 

file = 'people.csv'

path = Path.cwd().joinpath(f'{file}')

print('hello', path)

