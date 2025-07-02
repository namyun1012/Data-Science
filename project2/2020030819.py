import sys
import math
## DECISION TREE CLASS


# feature : attribute 포함된 list
# database : 가지고 있는 data 값
# 해당하는 DB 를 못 찾을 시 leaf 가 이니어도 해당 Node 에서 끝내게 해야함
# Leaf 가 아니더라도 classify 를 갖고 있어야 할 듯
# Classify 는 각자 가지고 있긴 해야 할 듯?

class DecisionTree:
    
    # Init 진행할 때, 자기 자신이 leaf 인지 확인
    def __init__(self, feature : list[str], database : list, domain = None):
        self.feature = feature
        self.children : list[DecisionTree] = []
        self.database = database
        self.selected_feature = None
        self.domain = domain

        # Leaf 에서 Testing 할 때 사용하는 용도
        self.is_leaf = True
        self.classify = None

        # 데이터 베이스 Class 전원 일치시 Leaf
        testing = database[0][-1]
        for data in database:
            if data[-1] != testing:
                self.is_leaf = False
                break

        # 나눌 Feature 없으면 Leaf
        if not feature:
            self.is_leaf = True

        # Vote 과정 진행
        # if self.is_leaf:
        count_dict = dict()

        for data in database:
            class_data = data[-1]
            if class_data in count_dict:
                count_dict[class_data] = count_dict.get(class_data) + 1
            else:
                count_dict[class_data] = 1

        max_votes = 0
        for classify, votes in count_dict.items():
            if votes > max_votes:
                max_votes =votes
                self.classify = classify


    # Training 과정에서 나누는 과정
    def divide(self):
        ## 먼저 leaf 인지 확인하는 검증 필요
        if self.is_leaf :
            return False

        selected_feature = select_feature(database=self.database, features=self.feature)
        self.selected_feature = selected_feature
        
        ## Selected Feature 선정 완료, DB를 이에 따라 나눔
        data_dict = dict()
        index = attributes_dict[selected_feature]

        for data in self.database:
            if data[index] in data_dict:
                data_dict[data[index]].append(data)
            else :
                data_dict[data[index]] = [data]

        child_features = self.feature[:]
        child_features.remove(selected_feature)

        for domain, split_db in data_dict.items():
            child_database = split_db
            self.children.append(DecisionTree(feature=child_features, database=child_database, domain = domain))

        return True



#FUNCTIONS
def entropy(p : float):
    return -p * math.log2(p)


def info(database : list):
    count_dict = dict()
    database_size = len(database)

    ## First Classify Class
    for data_set in database:
        class_data = data_set[-1]

        if class_data in count_dict:
            count_dict[class_data] = count_dict.get(class_data) + 1
        else:
            count_dict[class_data] = 1

    info = 0.0
    for class_name, count in count_dict.items():
        p = count / database_size
        info += entropy(p)

    return info


# In features, There are features you can use
# feature is list

def select_feature(database, features):
    # First, Get Info(D)
    
    # 분리 전의 Info, feature  사용 안함
    info_before = info(database)

    selected_feature = None
    gain_ratio = 0.0

    # 각 Feature 별 구하기
    for feature in features:
        # attribute 의 index
        index = attributes_dict[feature]

        info_after = 0.0
        split_info = 0.0

        # Database 를 나누어서 작은 database 를 나눈 후 거기서 Info 함수 실행 필요
        distributed_database = dict()

        for data in database:
            if data[index] in distributed_database:
                distributed_database[data[index]].append(data)
            else :
                distributed_database[data[index]] = [data]

        for temp, split_db in distributed_database.items():
            split_data_ratio = len(split_db) / len(database) # 기존 database 에서 나눠진 database 의 비율
            info_after += info(split_db) * split_data_ratio
            split_info += entropy(split_data_ratio)

        cur_gain_ratio = (info_before - info_after) / split_info

        if cur_gain_ratio > gain_ratio:
            gain_ratio = cur_gain_ratio
            selected_feature = feature

    # 선정 완료
    # DB 분할은 받는 쪽에서 진행하는 걸로?
    return selected_feature

def recursive_decison_tree(tree : DecisionTree):

    tree.divide()

    if not tree.children:
        return

    for child in tree.children:
        recursive_decison_tree(child)

def testing(tree : DecisionTree, data : list[str]):

    ## Tree 가 LEAF 인 경우
    if tree.is_leaf:
        return tree.classify

    # Tree 가 LEAF 가 아닌 경우, Child 들을 확인해서 재귀 형태로 testing
    feature = tree.selected_feature
    index = attributes_dict[feature]

    testing_domain = data[index]

    for child in tree.children:
        if child.domain == testing_domain:
            return testing(child, data)


    # 없을 시 자신의 classify return
    return tree.classify

# FILES
training_dataset_file = sys.argv[1]
test_data_file = sys.argv[2]
classification_result_file = sys.argv[3]

training_file = open(training_dataset_file, 'r')
test_file = open(test_data_file, 'r')
result_file = open(classification_result_file, 'w')

# INPUT
attributes_list = []
attributes_dict = dict()

## attribute 별 index 맞추어 놓기
index = 0
for attribute in training_file.readline().split():
    attributes_list.append(attribute)
    attributes_dict[attribute] = index
    index += 1

class_label = attributes_list[-1]

DB = []

for line in training_file.readlines():
    DB.append(list(line.split()))

## TRAINING

"""
 MAKING A DECISION TREE
"""

root = DecisionTree(feature=attributes_list[0 : len(attributes_list) - 1], database=DB)

## Decision Tree 를 끝까지 만들어 내기

recursive_decison_tree(root)

## TESTING DB 준비
testing_attribute_list = test_file.readline().split()
testing_DB = []

for line in test_file.readlines():
    testing_DB.append(list(line.split()))

# Resulting Attribute 먼저 작성
result_text = ""
for attribute in attributes_list:
    result_text += attribute
    result_text += "\t"

result_text = result_text.strip()
result_text += "\n"
result_file.write(result_text)

# Testing 진행하기
for data in testing_DB:
    test_label = testing(root, data)
    result_text = ""

    for data_domain in data:
        result_text += data_domain
        result_text += "\t"

    result_text += test_label

    result_text += "\n"
    result_file.write(result_text)







## FILE CLOSED

training_file.close()
test_file.close()
result_file.close()