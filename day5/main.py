def merge_ranges(ranges):
    ranges.sort(key=lambda x: x[0])  
    merged = [ranges[0]]
      
    for current in ranges[1:]:
        last_merged = merged[-1]
        if current[0] <= last_merged[1]:
            merged[-1] = (last_merged[0], max(last_merged[1], current[1]))
        else:
            merged.append(current)
    
    ranges.clear()
    ranges.extend(merged)


def main():
    ingredients = []
    ranges = []
    with open("H:/AdventOfCode_25/day5/input.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if '-' in line:
                range_parts = line.split("-")
                ranges.append((int(range_parts[0]), int(range_parts[1])))
            elif line:
                ingredients.append(int(line.strip()))    
    merge_ranges(ranges)
    
    #part1
    fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                fresh += 1
                break

    print(fresh)
    
    #part2
    total = 0
    for r in ranges:
        total += r[1] - r[0] + 1
        
    print(total)

main()
