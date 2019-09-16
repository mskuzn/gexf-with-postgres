#!/usr/bin/python3
import sys,pprint
import psycopg2
from gexf import Gexf, GexfImport

class Db_operations:
    def __init__(self, db='my_db', usr='user', hst='localhost',pswd='qwerty',db_scheme='topology',db_table_nodes='nodes',db_table_edges='edges'):
       	self.connect = psycopg2.connect(database=db, user=usr, host=hst, password=pswd)
        self.cursor = self.connect.cursor()
        self.db_scheme=db_scheme
        self.db_table_nodes=db_table_nodes
        self.db_table_edges=db_table_edges
        self.nodes_arr_of_dict = []
        self.edges_arr_of_dict = []
 
    def create_gexf_from_db(self):
        #получаем имена колонок из таблиц с узлами и рёбрами для того, чтобы знать имена необязательных атрибутов графа
        self.cursor.execute("select string_agg(column_name,',') as str from INFORMATION_SCHEMA.COLUMNS where table_name = '"+self.db_table_nodes+"' and table_schema = '"+ self.db_scheme +"';")
        self.column_nodes=next(self.cursor)[0]
        self.column_nodes_arr=self.column_nodes.split(',')

        self.cursor.execute("select string_agg(column_name,',') as str from INFORMATION_SCHEMA.COLUMNS where table_name = '"+self.db_table_edges+"' and table_schema = '"+ self.db_scheme +"';")
        self.column_edges=next(self.cursor)[0]
        self.column_edges_arr=self.column_edges.split(',')

        self.cursor.execute("select "+self.column_nodes+" from " + self.db_scheme +"."+self.db_table_nodes+";")
        for row in self.cursor:
            i=0
            row_dict={}
            for field in self.column_nodes_arr:
                row_dict.update({field: str(row[i])})
                i+=1
            self.nodes_arr_of_dict.append(row_dict)

        self.cursor.execute("select "+self.column_nodes+" from " + self.db_scheme +"."+self.db_table_nodes+";")
        for row in self.cursor:
            i=0
            row_dict={}
            for field in self.column_nodes_arr:
                row_dict.update({field: str(row[i])})
                i+=1
            self.nodes_arr_of_dict.append(row_dict)

        self.cursor.execute("select "+self.column_edges+" from " + self.db_scheme +"."+self.db_table_edges+";")
        for row in self.cursor:
            i=0
            row_dict={}
            for field in self.column_edges_arr:
                row_dict.update({field: str(row[i])})
                i+=1
            self.edges_arr_of_dict.append(row_dict)

        #gexf операции
        gexf = Gexf("DAKOKS","topology_tn_region")
        graph=gexf.addGraph("undirected","static","topology_tn_region_graph")

        for attr in self.column_nodes_arr:
            if attr not in ['id','size','r','g','b','label','x','y']:
                graph.addNodeAttribute(title=attr, defaultValue=None, type="string")

        for attr in self.column_edges_arr:
            if attr not in ['id','source','target','label','weight','r','g','b']:
                graph.addEdgeAttribute(title=attr, defaultValue=None, type="string")

        for node_data in self.nodes_arr_of_dict:
            graph.addNode(node_data['id'],node_data['label'],r=node_data['r'],g=node_data['g'],b=node_data['b'],x=node_data['x'],y=node_data['y'])
            for attr in graph.attributes['node']:
                graph.nodes[node_data['id']].addAttribute(attr,node_data[graph.attributes['node'][attr]['title']])

        for edge_data in self.edges_arr_of_dict:
            graph.addEdge(edge_data['id'],edge_data['source'],edge_data['target'],weight=edge_data['weight'],label=edge_data['label'],r=edge_data['r'],g=edge_data['g'],b=edge_data['b'])
            for attr in graph.attributes['edge']:
                graph.edges[edge_data['id']].addAttribute(attr,edge_data[graph.attributes['edge'][attr]['title']])

        output_file=open("MY_GEXF.gexf","w")
        gexf.write(output_file)

#    def get_node_coords_from_gexf(self)

    def con_close(self):
        self.connect.close()

my_db=Db_operations(db='first_db', usr='superuser',pswd='123qwe',db_scheme='topology',db_table_nodes='nodes',db_table_edges='edges')
print(my_db.create_gexf_from_db())
