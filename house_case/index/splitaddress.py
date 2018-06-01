# encoding=utf-8
# to finish that local source to find the address for text

import json

start_w = ["坐落于","位于","名下的","所有的"]
find_w   = ["的房产","的房屋","房产","房屋","的房地产","的抵押房产","的土地","房地产","商位","商铺","抵押房产","土地。"]
find_sg = ["。","；"]
#load_dict = []
#source_cases = "../data/dw.document.json"
#addr_cases_json = "../data/index_01.json"

"""
#with open(source_cases,"r",encoding='gbk') as f:
def read_source(source_cases):
	with open(source_cases,"r") as f:
		load_dict = json.load(f)

	print("json loaded!")
	return load_dict
"""

def find_addrkey(newaddr):
	if(len(newaddr) > 0):
		for ad_key in find_w:
			if(newaddr.find(ad_key) > -1):
				return True
	return False

def local_index(load_dict):
	case_num = 0
#	length = len(load_dict)
	#print(str(length)+","+load_dict[0]['_id'])
#	for case_id in range(length):
	new_dict = {}
	judge_res = load_dict["judgement_result"]

	for i in start_w:
		if(judge_res.find(i) > -1):
#			print(i+" "+judge_res),
			head_s = (judge_res.split(i,1))[0]
			head_addr = head_s

			if(head_s.find(find_sg[0]) > -1):
				head_addr= (head_s.rsplit(find_sg[0],1))[1]
			if(head_addr.find(find_sg[1]) > -1):
				head_addr = (head_addr.rsplit(find_sg[1],1))[1]
			first_s = (judge_res.split(i,1))[1] #关键词后半段

			#print(str(case_id)+":"+ head_addr + i + first_s)
			find_house = False
			temp_addr = first_s
			for j in find_sg:
				if(j == find_sg[1]):
					break
				if(temp_addr.find(j) > -1):#发现后半段结尾符号
					find_house = True
					if(i == start_w[2] or i == start_w[3]):
						if(find_addrkey(temp_addr) == False):
							find_house = False
#							break
				#	new_dict.append(first_s)
					address = (temp_addr.split(j))[0]	#判断是否含有句号，有则取句号
					temp_addr = address

			if(find_house):
				address = head_addr + i + address
				#addr_dict.append(address)
				#addr_dict = {}
				new_dict["_id"] = load_dict["_id"]
				new_dict["judgement_result"] = address
				break
	
	#print("get address!")
	return new_dict

#print(new_dict)
#print(new_dict)
"""
def write_text(new_dict):

	with open(addr_cases_json,"w",encoding='gbk') as f:
		json.dump(new_dict,f,ensure_ascii=False)
"""
