import os
import pandas as pd
import csv
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gptfuzzer.fuzzer.corecode import GPTFuzzer
import argparse

# 增加文件名和行号到日志格式
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# 获取一个日志记录器
logger = logging.getLogger(__name__)

# 创建一个 ArgumentParser 对象
parser = argparse.ArgumentParser(description='处理API调用和文件路径的参数脚本。')
# 添加参数
parser.add_argument('-a', '--oneApi_address', type=str, required=True, help='oneApi的访问地址')
parser.add_argument('-k', '--apikey', type=str, required=True, help='API的key')
parser.add_argument('-m', '--model_name', type=str, required=True, help='模型的名称')
parser.add_argument('-n', '--channelId', type=int, required=True, help='channelId')
parser.add_argument('-p', '--question_path', type=str, required=True, help='问题表的路径')
parser.add_argument('-t', '--seed_path', type=str, required=True, help='模板的路径')
parser.add_argument('-s', '--type', type=str, required=True, help='模板的类型')
parser.add_argument('-o', '--result_file_path', type=str, required=True, help='输出文件的路径')
parser.add_argument('-l', '--encode', type=str, required=True, help='要加密的编码')
parser.add_argument('-f', '--max_jailbreak', type=int, required=True, help='Fuzz的轮数')
parser.add_argument('-s1', '--state', type=str, required=False, help='状态')
parser.add_argument('-a1', '--oneApi_address_judge', type=str, required=False, help='判断模型的访问地址')
parser.add_argument('-k1', '--apikey_judge', type=str, required=False, help='判断模型的key')
parser.add_argument('-m1', '--model_name_judge', type=int, required=False, help='判断模型地址')
parser.add_argument('-n1', '--channelId_judge', type=int, required=False, help='判断channelId')
# 如果命令行中提供了 --reset 或 -r 选项，则将 reset 设置为 True；如果没有提供，则默认为 False
parser.add_argument('-r', '--reset', action='store_true', help='重排问题')
# 解析参数
args = parser.parse_args()

oneApi_address = args.oneApi_address
apikey = args.apikey
model_name = args.model_name
channelId = args.channelId
max_jailbreak = args.max_jailbreak
result_file_path = args.result_file_path                      
seed_path = args.seed_path 
encode_string = args.encode
state = args.state
oneApi_address_judge = args.oneApi_address_judge
apikey_judge = args.apikey_judge
model_name_judge = args.model_name_judge
channelId_judge = args.channelId_judge
reset = args.reset
# 使用split()方法按照"-"拆分字符串，得到一个列表
encode_list = encode_string.split("-")   

# 获取模板类型
type_string = args.type
seed_type = type_string.split("-")


# initial_seed = pd.read_csv(seed_path)['content'].tolist()
initial_seed = []

# 打开CSV文件  
with open(seed_path, mode='r', newline='', encoding='utf-8') as file:  
    csv_reader = csv.reader(file)  
    # 跳过表头（假设第一行是表头）  
    next(csv_reader)  
    # 遍历CSV文件的每一行  
    for row in csv_reader:  
        # row是一个列表，row[0]是'content'的值，row[1]是'type'的值  
        if row[2] in seed_type:  # 注意：CSV文件中的数字可能是字符串形式  
            all = (row[0],row[1],row[2])
            initial_seed.append(all)

question_path = args.question_path
questions_set = pd.read_csv(question_path)['content'].tolist()
logging.info(f"questions_set:{questions_set}")

if not os.path.exists(result_file_path):
    parent_dir = os.path.dirname(result_file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    new_file = open(result_file_path,"w")
    new_file.close()

#通过参数的名称来指定值，这样可以不按照定义的顺序传递。例如，max_jailbreak=3是将数字3传递给max_jailbreak参数。
fuzzer = GPTFuzzer(
    questions=questions_set,
    initial_seed=initial_seed,
    encode_list=encode_list,
    max_jailbreak=max_jailbreak,
    max_query=500,
    result_file=result_file_path,
    oneApi_address = oneApi_address,
    apikey = apikey,
    model_name = model_name,
    channelId = channelId,
    state=state,
    oneApi_address_judge=oneApi_address_judge,
    apikey_judge=apikey_judge,
    model_name_judge=model_name_judge,
    channelId_judge=channelId_judge,
    reset=reset,
)

fuzzer.run()