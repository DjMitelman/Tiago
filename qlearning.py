import numpy as np


environment_rows = 10
environment_columns = 10
q_values = np.zeros((environment_rows, environment_columns, 4))


actions = ['up', 'right', 'down', 'left']


rewards = np.full((environment_rows, environment_columns), -1.)

rewards[9, 7] = 100.
rewards[9, 8] = 200.
rewards[9, 9] = 300.

rewards[5, 3] = -1000.
rewards[5, 4] = -1000.
rewards[5, 5] = -1000.
rewards[5, 6] = -1000.
  
for row in rewards:
  print(row)


def isTerminalState(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

def getStartingLocation():
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  while isTerminalState(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index

def getNextAction(current_row_index, current_column_index, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else:
    return np.random.randint(4)

def getNextLocation(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index

def getShortestPath(start_row_index, start_column_index):
  if isTerminalState(start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    while not isTerminalState(current_row_index, current_column_index):
      action_index = getNextAction(current_row_index, current_column_index, 1.)
      current_row_index, current_column_index = getNextLocation(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index])
    return shortest_path

###

epsilon = 0.4
discount = 0.9
learning_rate = 0.9

for episode in range(1000):
  row_index, column_index = getStartingLocation()

  while not isTerminalState(row_index, column_index):
    action_index = getNextAction(row_index, column_index, epsilon)

    old_row_index, old_column_index = row_index, column_index
    row_index, column_index = getNextLocation(row_index, column_index, action_index)
    
    reward = rewards[row_index, column_index]
    old_q_value = q_values[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount * np.max(q_values[row_index, column_index])) - old_q_value

    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')

###

x = getShortestPath(0, 0)
print(getShortestPath(0, 0))

