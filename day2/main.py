import re

def part1(id_ranges):
    invalid_count = 0
    
    for start, end in id_ranges:
        if len(str(start)) %2 != 0 and len(str(end)) %2 != 0 and len(str(start)) == len(str(end)):
            continue
        else:
            for number in range(start, end+1):
                if len(str(number)) %2 == 0:
                    number_str = str(number)
                    number_first_half = number_str[:len(number_str)//2]
                    number_second_half = number_str[len(number_str)//2:]
                    if number_first_half == number_second_half:
                        invalid_count += number

    print("Invalid IDs:", invalid_count)
    
def find_sequence(number_str):
    for i in range(2, len(number_str)//2+1):
        regex = rf"{number_str[:i]}"
        match = re.findall(rf"({regex})", number_str)
        if match:
            if len(match) * len(regex) == len(number_str):
                return int(number_str)
    return 0

def part2(id_ranges):
    invalid_count = 0
    
    for start, end in id_ranges:
       for number in range(start, end+1):
           if len(str(number)) > 1:
            number_str = str(number)
            set_digits = set(number_str)
            if 1 == len(set_digits):
                invalid_count += number
            else:
                invalid_count += find_sequence(number_str)

    print("Invalid IDs:", invalid_count)

def main():
    id_ranges = []
    with open("H:/AdventOfCode_25/day2/input.txt", "r", encoding="utf-8") as file:
        line = file.readline().strip()
        ranges = line.split(",")
        for r in ranges:
            start, end = map(int, r.split("-"))
            id_ranges.append((start, end))

    part1(id_ranges)
    part2(id_ranges)
    
main()
