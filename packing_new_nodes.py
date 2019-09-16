#!/usr/bin/python3
import sys,pprint
import psycopg2

class Db_operations:
    def __init__(self, db='my_db', usr='user', hst='localhost',pswd='qwerty',db_scheme='topology',db_table_nodes='nodes',db_table_edges='edges'):
       	self.connect = psycopg2.connect(database=db, user=usr, host=hst, password=pswd)
        self.cursor = self.connect.cursor()
        self.db_scheme=db_scheme
        self.db_table_nodes=db_table_nodes
        self.db_table_edges=db_table_edges
        self.column_nodes='id,label,x,y'
        self.column_edges='source,target'
        self.column_nodes_arr = self.column_nodes.split(',')
        self.column_edges_arr = self.column_edges.split(',')
        self.nodes_arr_of_dict = []
        self.edges_arr_of_dict = []
    def get_nodes(self):
        self.cursor.execute("select "+ self.column_nodes +" from " + self.db_scheme +"."+self.db_table_nodes+";")
        for row in self.cursor:
            i=0
            row_dict={}
            for field in self.column_nodes_arr:
                row_dict.update({field: str(row[i])})
                i+=1
            self.nodes_arr_of_dict.append(row_dict)
        return self.nodes_arr_of_dict
    def get_edges(self):
        self.cursor.execute("select "+ self.column_edges +" from " + self.db_scheme +"."+self.db_table_edges+";")
        for row in self.cursor:
            i=0
            row_dict={}
            for field in self.column_edges_arr:
                row_dict.update({field: str(row[i])})
                i+=1
            self.edges_arr_of_dict.append(row_dict)
        return self.edges_arr_of_dict

    def guess_empty_position(self):
        #выбрать точки с пустыми данными 'A' (в последствии переделать на особое поле(где отсутствуют соседи))
        #отделить от всех остальных 'B'
        #выбрать каждую точку, вычислять для неё координаты по соседям из 'B'
        #поместить все вновь найденные координаты в пул 'C'
        # по циклу искать наличие связей с координатами
        #для к
        return 0
    def update_position_new_nodes(self):
        return 0
session=Db_operations(db='first_db', usr='superuser',pswd='123qwe',db_scheme='topology',db_table_nodes='nodes',db_table_edges='edges')
print(session.get_nodes())
print('######')
print(session.get_edges())
