#!/usr/bin/python3
import sys,pprint
import psycopg2
from gexf import Gexf, GexfImport
class Positions:
    def __init__(self,fle_name,path=""):
        self.f = open(fle_name)
        self.gexf_import = Gexf.importXML(self.f)
        self.f.close()
        self.graph=self.gexf_import.graphs[0]
    def get_positions(self):
        self.arr_of_dict=[]
        for node in self.graph.nodes:
            row = self.graph.nodes[node].get_position()
            row.update({'id':node})
            self.arr_of_dict.append(row)
        return self.arr_of_dict
class Db:
    def __init__(self, db='my_db', usr='user', hst='localhost',pswd='qwerty',db_scheme='topology',db_table_nodes='nodes'):
       	self.connect = psycopg2.connect(database=db, user=usr, host=hst, password=pswd)
        self.cursor = self.connect.cursor()
        self.db_scheme=db_scheme
        self.db_table_nodes=db_table_nodes
    def upload_positions(self,positions_data=[]):
        self.positions_data=positions_data
        for row in positions_data:
            sql="UPDATE " + self.db_scheme + "." + self.db_table_nodes + " SET (x,y) = ('" + row['x'] +"'::numeric,'"+ row['y'] +"""'::numeric)
                where id='"""+ row['id'] +"'::bigint;"
            self.cursor.execute(sql)
        self.connect.commit()

curr_file=Positions('hand_edit.gexf')
positions_to_db=curr_file.get_positions()
my_db=Db(db='first_db', usr='superuser',pswd='123qwe',db_scheme='topology',db_table_nodes='nodes')
my_db.upload_positions(positions_to_db)
