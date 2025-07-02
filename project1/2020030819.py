import sys
from itertools import combinations

min_support = int(sys.argv[1])
input_name = sys.argv[2]
output_name = sys.argv[3]

input_file = open(input_name, 'r')
output_file = open(output_name, 'w')

input_lines =input_file.readlines()


# Transaction DB
DB = []

# count dict 에는 Count 를 저장해서 나중에 사용할 때 get_support 사용 (frequent itemSet 만 저장)
count_dict = dict()

# transaction 내에 itemSet 존재하는 지 확인
def contain(transaction, itemSet):
    for item in itemSet:
        if not item in transaction:
            return False
    return True

# count to support
def get_support(count):
    return count / len(DB) * 100

# itemSet 내부에서 진행하는 것으로 변경할 것
def write_associative(itemSet):

    itemSet_count = count_dict[itemSet]
    itemSet_list = []
    
    # 각 조합의 경우의 수 추가 1 에서 item Set 크기 미만
    # itemSet 길이가 1인 경우 자동으로 걸러짐
    for i in range(1, len(itemSet)):
        itemSet_list.append(list(combinations(itemSet, i)))

    # item_set 별로 진행
    for cur_set_list in itemSet_list:
        for cur_set in cur_set_list:
            itemSet1 = frozenset(cur_set)
            itemSet2 = itemSet.difference(itemSet1)

            itemSet1_count = 0
            for transaction in DB:
                if contain(transaction, itemSet1):
                    itemSet1_count += 1

            # above support, then, find confidence
            # unionSet's support / itemSet1's support
            if(get_support(itemSet_count) >= min_support):
                support = get_support(itemSet_count) # 원본 itemSet 것으로
                confidence = itemSet_count / itemSet1_count * 100 # 원본 / 조합 itemSet * 100

                output_text = ""

                # ItemSet
                output_text += "{"
                for item in itemSet1:
                    output_text += f"{item},"
                output_text = output_text.strip(',')

                output_text += "}"
                output_text += "\t"

                #Associatvie ItemSet
                output_text += "{"

                for item in itemSet2:
                    output_text += f"{item},"

                output_text = output_text.strip(",")
                output_text += "}"

                output_text += "\t"

                #Support
                output_text += f"{support : .2f}"

                output_text += "\t"

                #Confidence
                output_text += f"{confidence : .2f}"

                output_text += "\n"
                output_file.write(output_text)
        
for line in input_lines:
    DB.append(list(map(int, line.split())))

# Size 별 itemSet의 집합
C_set_list = []
L_set_list = []

# 각 size set 에는 frozenset 을 집어넣음
# set 내부 set 불가, tuple은 내부 중복 및 순서 => frozenset 이 가장 적절함
C_set_1 = set()
L_set_1 = set()




# Initial, Add All size 1 item to C_set_1
for transaction in DB:
    for item in transaction:
        C_set_1.add(frozenset({item}))
        
C_set_list.append(C_set_1)

# L_set_1 Initial
# 이 코드에선 DB도 Memory 에서 올려놔서 연산 속도 큰 차이 없을 듯
for itemSet in C_set_1:
    
    count = 0
    for transaction in DB:
        if contain(transaction, itemSet):
            count += 1
        
    if(get_support(count) >= min_support):
        L_set_1.add(itemSet)
        count_dict[itemSet] = count

        

L_set_list.append(L_set_1)

# Apply Apriori Algorithm, K =1 is already complete
k = 2

# final L_set is not empty
while len(L_set_list[-1]) != 0:
    
    C_set_new = set()
    
    # Candidate Generate Algorithm
    # L_set 에서 합치고 길이가 k 인 것만 보냄
    # Pruning?
    for temp_1 in L_set_list[-1]:
        for temp_2 in L_set_list[-1]:
            new_candidate_itemSet = frozenset.union(temp_1, temp_2)
            if len(new_candidate_itemSet) == k:
                C_set_new.add(new_candidate_itemSet)
            
    # Generate L
    L_set_new = set()
    for itemSet in C_set_new:
        count = 0

        for transaction in DB:
            if contain(transaction, itemSet):
                count += 1
        
        if(get_support(count) >= min_support):
            L_set_new.add(itemSet)
            count_dict[itemSet] = count
    
    # Add L_set_new to L_set_list
    L_set_list.append(L_set_new)
    k += 1
    

frequent_set = set()

for L_set in L_set_list:
    for itemSet in L_set:
        frequent_set.add(itemSet)

# Find Associative Set
for itemSet in frequent_set:
    write_associative(itemSet)
             
output_file.close()
input_file.close()