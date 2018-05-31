# encoding: utf-8

import re
import json
import sys
sys.path.append('../norm')
import normalized
sys.path.append('../index')
import splitaddress


case_source_json = "../data/dw.document.json" # "../data/index_01.json"
case_extracted_json = "../data/case_extracted_01.json"
#case_info_json = "./house_info_extract.json"
#case_norm_json = "../norm/case_norm_01.json"
house_info_json = []

def get_addr(judge_res):
	pattern = re.compile(r'.*坐落于(.*?)的房产.*')
	match_addr = re.match(pattern, judge_res)
	if(match_addr):
		return match_addr.group(1)
#		print("(",match_addr.group(1),")")

def get_name(judge_res):
	pattern = re.compile(r'(被告|被执行人|被申请人|担保人|被上诉人|被申诉人|被告人|二审被上诉人|抵押人|罪犯)(.*)(共有|共同所有|将其所有|名下|所有|所有用于抵押|抵押|抵押担保|质押|最高额抵押担保|用于抵押|坐落于|享有|位于)')
	match_addr = re.match(pattern, judge_res)
	if(match_addr):
		return match_addr.group(2)
#		print("(",match_addr.group(1),")")

def get_number(judge_res):
	"""结尾符号等存在优先顺序，应将优先权大的排在前面，以免丢失信息;"""
	res_num = []
	res_hos = {}

	pattern1 = re.compile(r'(【|\[|（|；)(房产证|房产证号|房屋所有权证号|权证号码|房权证号|产权证号|房地产权证号|登记证明号)(：)(.*)号(】|\]|）|；|，|、)')
	pattern2 = re.compile(r'(土地证号|国有土地使用权证号|土地使用证号)(：)(.*?)号(】|\]|）|；|，|、)')

	match_house = re.search(pattern1, judge_res)
	if(match_house != None):
		res_hos["h_number"] = match_house.group(4)

	match_land = re.search(pattern2, judge_res)	
	if(match_land != None):
		res_hos["g_number"] = match_land.group(3)

	res_num.append(res_hos)
	
	return res_num

#		print("(",match_addr.group(1),")")

def get_value(judge_res):
	res_value = []
	index_value = 3
	flag_p = 1

	pattern1 = re.compile(r'(最高限额|最高额|最高抵押金额|最高债权数额|最高本金限额|最高抵押担保金额)(为|人民币|：?)(.*?)(万元)')
	pattern2 = re.compile(r'(在人民币|在)(.*?)(万元)[(的)(最高金额)(范围)]')#((的?)(最高金额?))(范围)')
	pattern3 = re.compile(r'(在)(.*?)万元和(.*?)(万元)')

	match_addr = re.search(pattern1, judge_res)
	if(match_addr == None):
		match_addr = re.search(pattern2,judge_res)
		index_value = 2
		flag_p = 2
	if(match_addr == None):
		match_addr = re.search(pattern3,judge_res)
		flag_p = 3
	if(match_addr == None):
		return 

	res_num_str = match_addr.group(index_value)
	if(res_num_str):
		res_num_int = int(res_num_str)
	else:
		return
	res_value.append(res_num_int)
	if(flag_p == 3):
		res_num_str_2 = match_addr.group(index_value+1)
		res_num_int_2 = int(res_num_str_2)
		res_value.append(res_num_int_2)

	return res_value
#		print("(",match_addr.group(1),")")

def extract(source_case):
	
	case_normal_dict = []
	num_case = 0
	#read
	index_addr_dict = splitaddress.local_index(source_case)
	if not index_addr_dict:
		return
	norm_addr_dict = normalized.addr2norm(index_addr_dict)

	case_normal = {}
	house_info = []
	house_addr_info = {}
	judge_res = norm_addr_dict["judgement_result"]

	#house_info["h_number"] = get_number(judge_res)["h_number"]
	house_info.append(get_number(judge_res))

	house_addr_info["address"] = get_addr(judge_res)
	house_addr_info["value"] = get_value(judge_res)
	house_info.append(house_addr_info)

	case_normal["house"] = house_info
	case_normal["_id"] = norm_addr_dict["_id"]
	case_normal["name"] = get_name(judge_res)
	return case_normal

def batch_extract(source_json,batch_num):
	
	case_extr_info_dict = []

	case_info_dict = normalized.read_json2dict(source_json)
	num_case = len(case_info_dict)
	if( num_case < 1):
		print("没有读到有效案件数据！")
		return 
	
	num_b = 0
	for case_i in range(num_case):
		if(num_b > batch_num):
			break
		num_b = num_b + 1

		str_case = case_info_dict[case_i]
		ext_house_info = extract(str_case)
		if case_extr_info_dict:
			case_extr_info_dict.append(ext_house_info)

	normalized.write_addr_json(case_extracted_json,case_extr_info_dict)	


if __name__ == '__main__':
	batch_num = 100
	batch_extract(case_source_json,batch_num)
