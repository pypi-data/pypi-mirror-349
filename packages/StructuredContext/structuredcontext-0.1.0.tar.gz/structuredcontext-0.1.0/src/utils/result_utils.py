import os
import json
from tqdm import tqdm

def concat_result(root_path, config):
    """
    将所有结果合并到all_result.json中
    """
    result_path = os.path.join(root_path, "Result", config["path"], config["context"])
    dataset_path = os.path.join(result_path,  "all_result.json")
    
    # 载入全部子数据
    data_list = []
    all_dataset = {}
    for file in os.listdir(result_path):
        if file.endswith(".json") and file not in ["all_result.json", "result_-1.json"]:
            with open(os.path.join(result_path, file), "r") as f:
                data_list.append(json.load(f))
                    
    # 合并数据并保存在子文件夹下
    for subset in data_list:
        for key in subset:
            if key not in all_dataset:
                all_dataset[key] = []
            for result in subset[key]:
                all_dataset[key].append(result)
    # 排序
    all_dataset = sorted(all_dataset.items(), key=lambda x: int(x[0]))
    all_dataset = {key: value for key, value in all_dataset}
    
    for key in all_dataset:
        assert len(all_dataset[key]) >= 3
    
    all_result = {}
    
    ex_dataset = []
    dataset_path = os.path.join(root_path,  "data_ex.jsonl")
    for line in tqdm(open(dataset_path, "r")):
        data = json.loads(line)
        ex_dataset.append(data)
    
    raw_dataset = []
    dataset_path = os.path.join(root_path,  "data.jsonl")
    for line in tqdm(open(dataset_path, "r")):
        data = json.loads(line)
        raw_dataset.append(data)
        
    for key in all_dataset:
        assert ex_dataset[int(key)]["namespace"] == all_dataset[key][0]["namespace"]
        ex_namespace = ex_dataset[int(key)]["namespace"]
        data = ex_dataset[int(key)]
        namespace = None
        for idx, raw_data in enumerate(raw_dataset):
            if raw_data["completion_path"] == data["completion_path"] and raw_data["requirement"]["Functionality"] == data["requirement"]["Functionality"]:
                namespace = raw_data["namespace"]
                break
        assert namespace is not None
        if namespace not in all_result:
            all_result[namespace] = {
                "ex_namespace": ex_namespace,
                "completion_path": data["completion_path"],
                "completion": []
            }
        all_result[namespace]["completion"] += [{"result": result["result"]} for result in all_dataset[key]]
        pass
    
    # 将all_dataset中的数据写入文件    
    with open(os.path.join(result_path, "all_result.json"), "w") as f:
        json.dump(all_result, f, indent=4)

def make_completion(root_path, config):
    """
    将all_result.json中的数据写入completion.jsonl中用于评估
    """
    result_path = os.path.join(root_path, "Result", config["path"], config["context"])
    try:
        all_result = json.load(open(os.path.join(result_path, "all_result.json"), "r"))
    except:
        print(f"all_result.json not found in {result_path}")
        return

    with open(os.path.join(result_path, f"completion.jsonl"), "w") as f:
        for key in all_result:
            namespace = key
            completion = all_result[key]["completion"]
            for result in completion:
                f.write(json.dumps({
                    "namespace": namespace,
                    "completion": result["result"]
                }) + "\n")

def make_result_with_passk(root_path, config):
    """
    基于all_result.json的数据和test_output.jsonl中的pass结果，合成数据
    """
    result_path = os.path.join(root_path, "Result", config["path"], config["context"])
    all_result = json.load(open(os.path.join(result_path, "all_result.json"), "r"))
    test_output = []
    for line in tqdm(open(os.path.join(result_path, "test_output.jsonl"), "r")):
        data = json.loads(line)
        test_output.append(data)
    
    all_result_with_passk = {}
    for key in all_result:
        namespace = key
        completion = all_result[key]["completion"]
        all_result_with_passk[namespace] = {
            "ex_namespace": all_result[key]["ex_namespace"],
            "completion_path": all_result[key]["completion_path"],
            "completion": []
        }
        for idx, result in enumerate(completion):
            completion_with_passk = {
                "result": result["result"],
                "run": None
            }
            for test_data in test_output:
                if test_data["namespace"] == namespace and test_data["completion"] == result["result"]:
                    completion_with_passk["run"] = test_data["Result"]
                    break
            assert completion_with_passk["run"] is not None
            all_result_with_passk[namespace]["completion"].append(completion_with_passk)
    
    with open(os.path.join(result_path, "result_with_passk.json"), "w") as f:
        json.dump(all_result_with_passk, f, indent=4)
    
    

if __name__ == "__main__":
    root_path = "/home/qikahh/projects/DynamicStructredContext/Datasets/DevEval"
    config = {
        "path": "Qwen2.5-Coder-3B-Instruct",
        "context": "HiC", # None or Structure or File or Oracle
    }
    concat_result(root_path, config)
    make_completion(root_path, config)
    # make_result_with_passk(root_path, config)