def part1(tachyon_manifold, pos):
    count = 0
    
    while pos:
        p = pos.pop(0)
        if p[0]+1 < len(tachyon_manifold):
            if tachyon_manifold[p[0]+1][p[1]] == '.':
                tachyon_manifold[p[0]+1][p[1]] = '|'
                pos.append((p[0]+1, p[1]))
            elif tachyon_manifold[p[0]+1][p[1]] == '^':
                count += 1
                if p[1]-1 >= 0 and tachyon_manifold[p[0]+1][p[1]-1] == '.':
                    tachyon_manifold[p[0]+1][p[1]-1] = '|'
                    pos.append((p[0]+1, p[1]-1))
                if p[1]+1 < len(tachyon_manifold[0]) and tachyon_manifold[p[0]+1][p[1]+1] == '.':
                    tachyon_manifold[p[0]+1][p[1]+1] = '|'
                    pos.append((p[0]+1, p[1]+1))
    print(count)
    
def part2(tachyon_manifold, pos, cache=None):
    if cache is None:
        cache = {}
    if pos in cache:
        return cache[pos]
    count = 0
    if pos[0] == len(tachyon_manifold)-1:
        return 1

    if pos[0]+1 < len(tachyon_manifold):
        if tachyon_manifold[pos[0]+1][pos[1]] == '.':
            count += part2(tachyon_manifold, (pos[0]+1, pos[1]), cache)
        elif tachyon_manifold[pos[0]+1][pos[1]] == '^':
            if pos[1]-1 >= 0 and tachyon_manifold[pos[0]+1][pos[1]-1] == '.':
                count += part2(tachyon_manifold, (pos[0]+1, pos[1]-1), cache)
            if pos[1]+1 < len(tachyon_manifold[0]) and tachyon_manifold[pos[0]+1][pos[1]+1] == '.':
                count += part2(tachyon_manifold, (pos[0]+1, pos[1]+1), cache)
    cache[pos] = count
    return count

def main():  
    tachyon_manifold = []
    pos = []
    with open("H:/AdventOfCode_25/day7/input.txt", "r", encoding="utf-8") as f:
        i = 0
        for line in f:
            if 'S' in line:
                start_pos = (i, line.index('S'))
                pos.append(start_pos)
            tachyon_manifold.append([x for x in line.strip()])
            i+=1

    p1_pos = pos.copy()
    p1_tachyon_manifold = [row.copy() for row in tachyon_manifold]
    part1(p1_tachyon_manifold, p1_pos)

    print(part2(tachyon_manifold, pos[0]))

main()
