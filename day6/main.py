def main():
    problems = []
    problems_part2 = []
    with open("H:/AdventOfCode_25/day6/input.txt", "r", encoding="utf-8") as f:
        for line in f:
            elements = [x for x in line.strip().split(" ") if x != '']
            problems.append(elements)

            line = line.replace(' ', '.')
            problems_part2.append(str(line.strip()))
                        
    #part1
    sum = 0
    for i in range(len(problems[0])):
        operator = problems[-1][i]
        temp = int(problems[0][i])
        for num in range(1, len(problems)-1):
            if operator == '+':
                temp += int(problems[num][i])
            elif operator == '*':
                temp *= int(problems[num][i])

        sum += temp
        
    print(sum)
    
    #part2
    sum2 = 0
    for i in range(len(problems_part2[0])):     
        if problems_part2[-1][i] == '+':
            tmp = 0
            expression = "+"
        elif problems_part2[-1][i] == '*':
            tmp = 1
            expression = "*"
        
        number = ''
        for problem in range(len(problems_part2)-1):
            number += problems_part2[problem][i]
            
        new_num = number.replace('.', '')

        if new_num == '':
            sum2 += tmp
        else:
            if expression == '+':
                tmp += int(new_num)
            else:
                tmp *= int(new_num)
    
    print(sum2+tmp)
                        
                
main()
