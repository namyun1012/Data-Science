import sys
import math

UNDEFINED = -2
NOISE = -1

input_name = sys.argv[1]
n = int(sys.argv[2])
eps = int(sys.argv[3])
min_pts = int(sys.argv[4])

input_file = open(input_name, 'r')
input_lines =input_file.readlines()

DB : list[list[int]] = []

# DB 에 전체 데이터 넣어 놓기
# [object_id, x_coordinate, y_coordinate]
for line in input_lines:
    line = line.split()
    id = int(line[0])
    x = float(line[1])
    y = float(line[2])
    DB.append([id, x, y])

# label 용도
# undefined : -2, Noise : -1
label = dict()

# label init
for line in DB:
    label[line[0]] = UNDEFINED # undefined

# 결과 cluster
# set 을 담는 list
clusters : list[list[int]] = []

def distance(x1 : float , y1 : float, x2 : float, y2 : float) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def range_query(px : float, py : float) -> list[int]:
    neighbors = []

    for line in DB:
        id = line[0]
        x = line[1]
        y = line[2]

        if distance(px, py, x, y) <= eps:
            neighbors.append(id)

    return neighbors

# DBSCAN 적용
for line in DB:
    point_id = line[0]
    cur_x = line[1]
    cur_y = line[2]

    if label[point_id] != UNDEFINED:
        continue

    cur_neighbors = range_query(cur_x, cur_y)

    if len(cur_neighbors) < min_pts:
        label[point_id] = NOISE # noise
        continue

    # cluster 번호는 기존 클러스터의 길이 (처음 0 부터 ~~~ )
    c = len(clusters)
    label[point_id] = c
    
    # cluster 그냥 list 사용, set 사용시 문제 많은 듯
    cur_cluster = cur_neighbors[:]
    # 자기 자신 제외는 배제
    
    idx = 0

    while idx < len(cur_cluster):
        q = cur_cluster[idx]
        idx += 1

        # Noise
        if label[q] == NOISE:
            label[q] = c
        # check undefined
        if label[q] != UNDEFINED:
            continue

        qx = DB[q][1]
        qy = DB[q][2]

        neighbors : list[int] = range_query(qx, qy)
        label[q] = c

        if len(neighbors) < min_pts:
            continue
        
        # 중복 방지 해야 함
        for data in neighbors:
            if not data in cur_cluster:
                cur_cluster.append(data)

    clusters.append(cur_cluster)

# len 이 제일 긴 것 n 개 선정

result_clusters = []

for i in range(n):
    max_number = -1
    cur_idx = -1

    for j in range(len(clusters)):
        cluster = clusters[j]
        if len(cluster) > max_number:
            max_number = len(cluster)
            cur_idx = j

    if cur_idx != -1:
        result_clusters.append(clusters[cur_idx])
        clusters[cur_idx] = [] # clusters[j] 는 비움

# Input file name split 시켜서 찾음
extracted_input_name = input_name.split(".")[0]

for i in range(n):
    cluster : list[int] = result_clusters[i]
    cluster.sort()

    output_file_name = extracted_input_name + f"_cluster_{i}.txt"
    output_file = open(output_file_name, 'w')

    output_text = ""
    for data in cluster:
        output_text += str(data)
        output_text += "\n"

    output_file.write(output_text)
    output_file.close()

input_file.close()







