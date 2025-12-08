def check_adjacent(paper_roll_map, i, j):
    adjacent_found = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(paper_roll_map) and 0 <= nj < len(paper_roll_map[0]):
            if paper_roll_map[ni][nj] == '@':
                adjacent_found += 1
    if  adjacent_found >= 4:
        return False
    return True

def main():
    paper_roll_map = []
    with open("H:/AdventOfCode_25/day4/input.txt", "r", encoding="utf-8") as f:
      for line in f:
        paper_roll_map.append([x for x in line.strip()])
        
    #part1    
    movable_count = 0
    for i, row in enumerate(paper_roll_map):
        for j, roll in enumerate(row):
            if roll == '@':
                if check_adjacent(paper_roll_map, i,j):
                    movable_count += 1
    
    print(movable_count)
    
    #part2
    movable_count = 0
    removable_positions = []
    
    while True:
        for i, row in enumerate(paper_roll_map):
            for j, roll in enumerate(row):
                if roll == '@':
                    if check_adjacent(paper_roll_map, i,j):
                        movable_count += 1
                        removable_positions.append((i,j))
        if not removable_positions:
            break
        for i,j in removable_positions:
            paper_roll_map[i][j] = '.'
        removable_positions = []
        
    print(movable_count)

main()
