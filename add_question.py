import argparse, csv, json

from sqlalchemy import Column, create_engine, Integer, MetaData, String, Table
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session, mapper
import os


#python3 add_question.py playground abbrev "what state has iso usa"


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

if __name__ == '__main__':
    split="playground"
    table_id="abbrev"
    question="what state has iso usa"
    din="data_and_model"
    json_file_name = os.path.join(din, split)+'.jsonl'
    
    
    question_to_json(table_id,question, json_file_name)
    print("Added question (with dummy label) to {}".format(json_file_name))
