import numpy as np
import json
import math

def compute_pass_at_k(n, c, k):
    """
    n: total number of completions per task
    c: number of completions that pass all tests
    k: k in pass_at_k
    这里n可能与k不一致 
    若n < k, 则只要c > 0, pass@k = 1 
    若n > k, 则需要计算组合数
    """
    if n - c < k:
        return 1
    else:
        # 计算从n中选k的组合数
        all_condidate = math.factorial(n) / (math.factorial(k) * math.factorial(n-k))
        # 计算从n-c中选k的组合数
        error_condidate = math.factorial(n-c) / (math.factorial(k) * math.factorial(n-c-k))
        return 1 - error_condidate / all_condidate
    
    
def pass_k(dataset, k=3):
    all_result = []
    for namespace in dataset:
        pass_num = 0
        for result in dataset[namespace]["completion"]:
            if result["run"] == "Pass":
                pass_num += 1
        data_num = len(dataset[namespace]["completion"])
        if data_num == 0:
            continue
        pass_rate = pass_num / data_num
        if data_num == 3:
            data_num *= 2
            pass_num *= 2
        all_result.append(compute_pass_at_k(data_num, pass_num, k))
        
    pass_k = np.mean(all_result)
    print("pass@{}: {}".format(k, pass_k))
    return pass_k
 
def compute_recall_at_k(num_list, k=3):
    """
    从num_list随机取k个数 计算其最大值；
    通过组合数 考虑所有情况的平均
    num_list: list of recall numbers
    k: k in recall@k
    """
    # 先排序
    num_list = sorted(num_list)
    # 计算从num_list中取k个数的组合数
    all_condidate_num = math.factorial(len(num_list)) / (math.factorial(k) * math.factorial(len(num_list)-k)) if len(num_list) >= k else 1
    all_condidate_value = 0
    for idx in range(len(num_list)):
        if idx+1 < k:
            continue
        condidate_num = math.factorial(idx) / (math.factorial(k-1) * math.factorial(idx-k+1)) if idx >= k-1 else 1
        all_condidate_value += num_list[idx] * condidate_num
    all_condidate_value = all_condidate_value / all_condidate_num
    return all_condidate_value
    
    
def recall_k(dataset, reference_dataset, dependency_type_list,  k=3):
    all_result = []
    for namespace in dataset:
        refer_dependency = reference_dataset[namespace]
        refer_list = []
        recall_num = []
        for depen_type in dependency_type_list:
            if depen_type in refer_dependency:
                refer_list += refer_dependency[depen_type]
        # 去重
        refer_list = list(set(refer_list))
        if len(refer_list) == 0:
            continue
        
        for result in dataset[namespace]:
            result_dependency = result["dependency"] if "dependency" in result else None
            if not result_dependency:
                recall_num.append(0)
                continue
            result_recall = 0
            result_list = []
            for depen_type in dependency_type_list:
                if depen_type in result_dependency:
                    # 如果result_dependency[depen_type]被json.dumps() 则需要反序列化
                    if isinstance(result_dependency[depen_type], str):
                        result_list += json.loads(result_dependency[depen_type])
                    else:
                        result_list += result_dependency[depen_type]
            # 去重
            result_list = list(set(result_list))
            for depen in result_list:
                if depen in refer_list:
                    result_recall += 1
            recall_num.append(result_recall / len(refer_list))
        all_result.append(compute_recall_at_k(recall_num, k))

    recall_k = np.mean(all_result)
    print("recall@{}: {}".format(k, recall_k))
    return recall_k



if __name__ == "__main__":
    data_type = "BaF"
    dataset_path = "/home/qikahh/projects/DynamicStructredContext/Datasets/DevEval/Result/Qwen2.5-Coder-3B-Instruct/{}/result_with_passk.json".format(data_type)
    raw_dataset_path = "/home/qikahh/projects/DynamicStructredContext/Datasets/DevEval/data.jsonl"
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
    
    raw_dataset = {}
    for line in open(raw_dataset_path, "r"):
        data = json.loads(line)
        raw_dataset[data["namespace"]] = data
        
    new_dataset = {}
    for key in dataset:
        raw_data = raw_dataset[key]
        if len(raw_data["dependency"]["cross_file"]) > 0 or True:
            new_dataset[key] = dataset[key]
    dataset = new_dataset
    dataset = dict(list(dataset.items())[:])
    pass_k(dataset, k=3)
    pass_k(dataset, k=1)
    
    reference_dataset_path = "/home/qikahh/projects/DynamicStructredContext/Datasets/DevEval/data.jsonl"
    reference_dataset = {}
    for line in open(reference_dataset_path, "r"):
        data = json.loads(line)
        reference_dataset[data["namespace"]] = data["dependency"]
    
    dependency_type_list = ["intra_class", "intra_file", "cross_file"]
    dependency_type_list = ["cross_file"]
    recall_k(dataset, reference_dataset, dependency_type_list, k=3)
    recall_k(dataset, reference_dataset, dependency_type_list, k=1)