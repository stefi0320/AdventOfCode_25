from math import sqrt
from sys import maxsize

def main():  
    junction_boxes = []
    with open("H:/AdventOfCode_25/day8/input.txt", "r", encoding="utf-8") as f:
        for line in f:
            junction_boxes.append([int(x) for x in line.split(",")])

    edges = []
    for i, box in enumerate(junction_boxes):
        for j in range(i+1, len(junction_boxes)):
            a, b = box, junction_boxes[j]
            dist = sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
            edges.append([dist, box, b])

    circuits = []
    #part1
    #for i in range(1000):
    last_connected = []
    while junction_boxes:
        min_range = maxsize
        to_connect = 0
        for idx, e in enumerate(edges):
            if min_range > e[0]:
                min_range = e[0]
                to_connect = idx

        a, b = edges[to_connect][1], edges[to_connect][2]

        found = 0
        appened_to = []
        for i,circuit in enumerate(circuits):
            if a in circuit or b in circuit:
                if a not in circuit:
                    appened_to.append([i,a])
                if b not in circuit:
                    appened_to.append([i,b])
                found = 1
            
        if found == 0:
            circuits.append([a, b])
        else:
            if appened_to:
                if len(appened_to) > 1:
                    for c in circuits[appened_to[0][0]]:
                        if c not in circuits[appened_to[1][0]]:
                            circuits[appened_to[1][0]].append(c)
                    if appened_to[0][1] not in circuits[appened_to[1][0]]:
                        circuits[appened_to[1][0]].append(appened_to[0][1])
                    circuits.pop(appened_to[0][0])
                else:
                    circuits[appened_to[0][0]].append(appened_to[0][1])

        if a in junction_boxes:
            junction_boxes.remove(a)
        if b in junction_boxes:
            junction_boxes.remove(b)
            
        last_connected = [a,b]

        edges.pop(to_connect)


    #part1
    #circuits_sorted = sorted(circuits, key=len, reverse=True)
    #top3 = circuits_sorted[:3]
    #mult = 1
    #for t in top3:
    #    mult *= len(t)

    #print(mult)
    
    #part2
    print(last_connected[0][0]*last_connected[1][0])

main()