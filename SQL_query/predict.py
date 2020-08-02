import argparse, os
from sqlnet.dbengine import DBEngine
from sqlova.utils.utils_wikisql import *
from train import construct_hyper_param, get_models


import argparse, csv, json

from sqlalchemy import Column, create_engine, Integer, MetaData, String, Table
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, mapper

import subprocess



import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_filewh
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn,sqlquery):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
  
    cur = conn.cursor()
    try:
    	cur.execute(sqlquery)
    except Error as e:
    	print(e)	
    rows = cur.fetchall()

    for row in rows:
        print(row)
        
        
        
        
        
def question_to_json(table_id, question, json_file_name):
    record = {
        'phase': 1,
        'table_id': table_id,
        'question': question,
        'sql': {'sel': 0, 'conds': [], 'agg': 0}
    }
    print(record)
    with open(json_file_name, 'wt') as fout:
        json.dump(record, fout)
        fout.write('\n')





def predict(data_loader, data_table, model, model_bert, bert_config, tokenizer,
            max_seq_length,
            num_target_layers, detail=False, st_pos=0, cnt_tot=1, EG=False, beam_size=4,
            path_db=None, dset_name='test'):

    model.eval()
    model_bert.eval()

    engine = DBEngine(os.path.join(path_db, f"{dset_name}.db"))
    results = []
    for iB, t in enumerate(data_loader):
        #print(t)
        nlu, nlu_t, sql_i, sql_q, sql_t, tb, hs_t, hds = get_fields(t, data_table, no_hs_t=True, no_sql_t=True)
        
        
        g_sc, g_sa, g_wn, g_wc, g_wo, g_wv = get_g(sql_i)
        
        g_wvi_corenlp = get_g_wvi_corenlp(t)
        wemb_n, wemb_h, l_n, l_hpu, l_hs, \
        nlu_tt, t_to_tt_idx, tt_to_t_idx \
            = get_wemb_bert(bert_config, model_bert, tokenizer, nlu_t, hds, max_seq_length,
                            num_out_layers_n=num_target_layers, num_out_layers_h=num_target_layers)
        if not EG:
            # No Execution guided decoding
            s_sc, s_sa, s_wn, s_wc, s_wo, s_wv = model(wemb_n, l_n, wemb_h, l_hpu, l_hs)
            pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wvi = pred_sw_se(s_sc, s_sa, s_wn, s_wc, s_wo, s_wv, )
            pr_wv_str, pr_wv_str_wp = convert_pr_wvi_to_string(pr_wvi, nlu_t, nlu_tt, tt_to_t_idx, nlu)
            pr_sql_i = generate_sql_i(pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wv_str, nlu)
        else:
            # Execution guided decoding
            prob_sca, prob_w, prob_wn_w, pr_sc, pr_sa, pr_wn, pr_sql_i = model.beam_forward(wemb_n, l_n, wemb_h, l_hpu,
                                                                                            l_hs, engine, tb,
                                                                                            nlu_t, nlu_tt,
                                                                                            tt_to_t_idx, nlu,
                                                                                            beam_size=beam_size)
            # sort and generate
            pr_wc, pr_wo, pr_wv, pr_sql_i = sort_and_generate_pr_w(pr_sql_i)
            # Following variables are just for consistency with no-EG case.
            pr_wvi = None # not used
            pr_wv_str=None
            pr_wv_str_wp=None

        pr_sql_q = generate_sql_q(pr_sql_i, tb)
        #print(pr_sql_i)

        for b, (pr_sql_i1, pr_sql_q1) in enumerate(zip(pr_sql_i, pr_sql_q)):
            results1 = {}
            results1["query"] = pr_sql_i1
            
            results1["table_id"] = tb[b]["id"]
            results1["nlu"] = nlu[b]
            results1["sql"] = pr_sql_q1
            results.append(results1)
            #print(b)

    return results

## Set up hyper parameters and paths
parser = argparse.ArgumentParser()

args = construct_hyper_param(parser)

BERT_PT_PATH = "annotated_wikisql_and_PyTorch_bert_param"


path_save_for_evaluation = "result"
split="playground"
data_path = "data_and_model"




# Load pre-trained models
path_model_bert = "model_bert_best.pt"
path_model = "model_best.pt" 
args.no_pretraining = True  # counterintuitive, but avoids loading unused models
model, model_bert, tokenizer, bert_config = get_models(args, BERT_PT_PATH, trained=True, path_model_bert=path_model_bert, path_model=path_model)



#connection to db

db_file=r"data_and_model/playground.db"
conn=create_connection(db_file)





while 1:
	
	
	question=input("Enter your question : ")
	din="data_and_model"
	table_id="company"
	#"what state has iso us"
	json_file_name = os.path.join(din, split)+'.jsonl'

	question_to_json(table_id,question, json_file_name)
	print("Added question (with dummy label) to {}".format(json_file_name))

	command = 'python3 annotate_ws.py '

	subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)




	# Load data
	dev_data, dev_table = load_wikisql_data(data_path, mode=split, toy_model=args.toy_model, toy_size=args.toy_size, no_hs_tok=True)
	dev_loader = torch.utils.data.DataLoader(
	    batch_size=args.bS,
	    dataset=dev_data,
	    shuffle=False,
	    num_workers=1,
	    collate_fn=lambda x: x  # now dictionary values are not merged!
	)







	#print("dev_loader",dev_loader)
	# Run prediction
	with torch.no_grad():
	    results = predict(dev_loader,
		              dev_table,
		              model,
		              model_bert,
		              bert_config,
		              tokenizer,
		              args.max_seq_length,
		              args.num_target_layers,
		              detail=False,
		              path_db=data_path,
		              st_pos=0,
		              dset_name=split, EG=args.EG)

	# Save results
	
	sqlquery=str(results[0]['sql'])
	
	a=sqlquery.split(' ')
	for i in range(len(a)):
		if a[i] == "=" :
			a[i+1] = '"'+a[i+1]+'"'
	sqlquery=" ".join(a)
	print(sqlquery)
	select_all_tasks(conn,sqlquery)  
	save_for_evaluation(path_save_for_evaluation, results, split)
