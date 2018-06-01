# encoding: utf-8

import re
import json
import sys

case_normal_json = "../data/case_norm_01.json"
keys_house_addr_h = "../keys_dict/house_addr_head.txt"
keys_house_addr_e = "../keys_dict/house_addr_endw.txt"


def read_json2dict(json_file):
	try:
		with open(json_file,"r") as case_f:#,encoding='gbk'
			load_dict = json.load(case_f)
			return load_dict
	except IOError as ioerr:
		print(sys._getframe().f_code.co_name,"() File %s is not found!" % json_file )
		return 
	

def read_list2key(list_file):
	_list = []
	try:
		with open(list_file, "r") as list_file:
			for line in list_file:
				ad_key = line.strip().split('\n')
				_list.append(ad_key[0])
			return _list
	except IOError as ioerr:
		print("File %s is not found!")
	

def replace_key(str_inf,oldkey, newkey):
	case_info = str_inf
	if(isinstance(str_inf,str) and isinstance(oldkey,str) and isinstance(newkey,str)):
		case_info = str_inf.replace(oldkey,newkey)	
	return case_info

def blurry_replace(str_inf):#处理地址后置信息，使其归一
	if((str_inf.find("的房产") != -1) or (str_inf.find("的经营使用权") != -1) or (str_inf.find("的土地使用权") != -1) or (str_inf.find("的商铺") != -1)):
		return str_inf

	pattern1 = re.compile(r'(室|号|间|村|层|户)(的?)(房产|房屋|房地产|小区房地产|房产的房产)')
	if(re.search(pattern1,str_inf) != None):
		res_str = pattern1.sub(r'\1的房产',str_inf) #保留前面的部分，后面的用“的房产”替换
		return res_str
		
	pattern2 = re.compile(r'(室|号|间|村|层)(（|【|\[|，)(房产|房屋|商位|商铺|房产证号|房产权证)')
	if(re.search(pattern2,str_inf) != None):
		res_str = pattern2.sub(r'\1的房产\2\3',str_inf)
		return res_str

	pattern3 = re.compile(r'(室|号|间|村|层)(）)(房产|房屋|商位|商铺)')
	if(re.search(pattern3,str_inf) != None):
		res_str = pattern3.sub(r'\1\2的房产',str_inf)
		return res_str
		

	pattern5 = re.compile(r'(商位)(的?)(使用权|经营使用权)')
	if(re.search(pattern5,str_inf) != None):
		res_str = pattern5.sub(r'\1的经营使用权',str_inf)
		return res_str

	pattern6 = re.compile(r'(号)(的?)(商铺|商位)')
	if(re.search(pattern6,str_inf) != None):
		res_str = pattern6.sub(r'\1的商铺',str_inf)
		return res_str

	pattern7 = re.compile(r'(套|处)(房产|房屋|房地产|小区房地产)')
	if(re.search(pattern7,str_inf) != None):
		res_str = pattern7.sub(r'\1的房产',str_inf) #保留前面的部分，后面的用“的房产”替换
		return res_str
	

	pattern4 = re.compile(r'(土地|地块|处)(的?)(使用权|国有土地使用权|土地使用权)')
	if(re.search(pattern4,str_inf) != None):
		res_str = pattern4.sub(r'\1的土地使用权',str_inf)
		return res_str
	else:
		return str_inf

"""
将地址完成标准化转换
"""
house_addr_head = read_list2key(keys_house_addr_h)
house_addr_endw = read_list2key(keys_house_addr_e)
	
def addr2norm(case_json):
	load_dict = []
	new_dict = []
#	house_addr_head = []
#	house_addr_endw = []
#	load_dict = read_json2dict(case_source_json)
#	if(not load_dict):
#		print("No found data!")
#		return
	
#	num = 0 #######################
#	for case_id in range(len(load_dict)):
#	if(num_find != -1)
#		num = num + 1
#		if(num > num_find):###########################################################
#			break
	case_dict = {}
	judge_res = case_json["judgement_result"] #load_dict[case_id]["judgement_result"]
	temp_case = judge_res
	
	if(house_addr_head and len(house_addr_head) > 1):
		ker_key_h = house_addr_head[0]
		len_h = len(house_addr_head)
		for i in range(len_h):
			if(i == 0 ):
				continue
			if(temp_case.find(house_addr_head[i]) > -1):#发现前置词
				temp_case = replace_key(temp_case, house_addr_head[i], ker_key_h)	
	else:
		print("没有获取到前置词的字典数据！")

	if(house_addr_endw and len(house_addr_endw) > 1):
		ker_key_e = house_addr_endw[0]
		len_e = len(house_addr_endw)
		for i in range(len(house_addr_endw)):
			if(i == 0):
				continue
			if(temp_case.find(house_addr_endw[i]) > -1):#发现后置词
				temp_case = replace_key(temp_case, house_addr_endw[i], ker_key_e)	
				break
	else:
		print("没有获取到后置词的字典数据！")

	temp_case = blurry_replace(temp_case)

	case_dict["_id"] = case_json["_id"]
	case_dict["judgement_result"] = temp_case

	return case_dict
#	new_dict.append(case_dict)
#		print(num,temp_case)

#	return new_dict

def write_addr_json(source_dict, _new_dict):
	if not _new_dict:
		print("new dict is null!" )
	try:	
		with open(source_dict, "w",encoding='gbk') as w_f:
			json.dump(_new_dict,w_f,ensure_ascii=False)
	except IOError as ioerr:
		print("write Error!")
	print("%s Writed data in %s !" % (sys._getframe().f_code.co_name ,source_dict))
"""
if __name__ == '__main__':
	_new_dict = addr2norm()		
	write_addr_json(_new_dict)
"""
