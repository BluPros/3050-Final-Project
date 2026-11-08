from collections import deque

# IDK but I don't want BFS in the game_state.py
# and then I can use the deque import here instead

def reachable(territories, source, player_id):
    visited = {source}
    queue = deque([source])

    while queue:
        current_territory = queue.popleft()

        for neighbor in territories[current_territory].neighbors:
            if neighbor not in visited and territories[neighbor].owner_id == player_id:
                visited.add(neighbor)
                queue.append(neighbor)


    return visited

def connected(territories, source, destination, player_id):
    if source == destination:
        return True
    if destination in reachable(territories, source, player_id):
        return True