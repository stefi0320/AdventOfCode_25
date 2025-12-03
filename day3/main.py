def part1(batteries):
    max_joltage = 0
    
    for battery in batteries:
        max_first = max(battery[:-1])
        second_set = battery[battery.index(max_first)+1:]
        max_num = max(second_set)
        max_joltage += int(max_first+max_num)
    
    print(max_joltage)
    
def part2(batteries):
    max_joltage = 0
    for battery in batteries:
        temp_joltage = ""
        idx = 0
        for i in range(-11, 1):
            if i == 0:
                num_set = battery[idx:]
            else:
                num_set = battery[idx:i]
            max_num = max(num_set)
            idx += num_set.index(max_num)+1
            temp_joltage += max_num
        max_joltage += int(temp_joltage)
    print(int(max_joltage))
    
def main():
    batteries = []
    with open("H:/AdventOfCode_25/day3/input.txt", "r", encoding="utf-8") as f:
        for line in f:
            batteries.append(line.strip())
    part1(batteries)
    part2(batteries)
main()
