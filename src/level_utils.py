from csv import reader


def import_level_data(level_number):
  if level_number > 5:
    print(f'No level {level_number}...setting to 0')
    level_number = 0


  level_BG  = []
  level_FG  = []
  level_WTR = []

  with open(f'./levels/level_layers/level_{level_number}_Background.csv', newline='') as file:
    for row in reader(file):
      level_BG.append(row)


  with open(f'./levels/level_layers/level_{level_number}_Foreground.csv', newline='') as file:
    for row in reader(file):
      level_FG.append(row)


  with open(f'./levels/level_layers/level_{level_number}_Water.csv', newline='') as file:
    for row in reader(file):
      level_WTR.append(row)      

  return [level_BG, level_FG, level_WTR]


if __name__ == '__main__':
  for row in import_level_data(0)[1]:
    print(row)