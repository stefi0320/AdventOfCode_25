def main():
    moveset = []
    with open("H:/AdventOfCode_25/day1/input.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            direction = line[0]
            distance = int(line[1:].strip())
            moveset.append([direction, distance])
    
    dial = 50
    password = 0
    
    # Part 1 exactly 0
    for m in moveset:
        if m[0] == "L":
            if dial < m[1]: 
                dial = 100 - ((m[1] - dial)) % 100
            else:
                dial -= m[1]
            if dial == 100:
                dial = 0
        elif m[0] == "R":
            dial = (dial + m[1]) % 100
        if dial == 0:
            password += 1
    print(password)
        
    # Part 2 during a turn reach 0
    dial = 50
    password = 0
    for m in moveset:
        if m[0] == "L":
            for _ in range(m[1]):
                dial -= 1
                if dial < 0:
                    dial = 99
                if dial == 0:
                    password += 1
        elif m[0] == "R":
            for _ in range(m[1]):
                dial += 1
                if dial > 99:
                    dial = 0
                if dial == 0:
                    password += 1
    
    print(password)
    
main()