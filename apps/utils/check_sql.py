#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import prettytable as pt
import json
tb = pt.PrettyTable()
def check_mysql_sql(user_name, passwords, host_address, port_port,sql_data):
    sql = '''/*--user={};--password={};--host={};--check=1;--port={};*/
    inception_magic_start;
    {}
    inception_magic_commit;'''.format(user_name, passwords, host_address, port_port, sql_data)
    return_data={}
    jsonData=[]
    conn = pymysql.connect(host='127.0.0.1', user='', passwd='',
                           db='', port=4000, charset="utf8mb4")
    cur = conn.cursor()
    ret = cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        return_data=dict()
        return_data['order_id']=row[0]
        return_data['stage']=row[1]
        return_data['error_level']=row[2]
        return_data['stage_status']=row[3]
        return_data['error_message']=row[4]
        if return_data['error_message'] != None:
            return {'Mysql_Sql_Error':return_data['error_message'],'status':'-1','check':'sql语法错误，请检查后重新提交审核'}
        return_data['sql']=row[5]
        jsonData.append(return_data)
    cur.close()
    conn.close()
    # tb.field_names = [i[0] for i in cur.description]
    # jsondatar = json.dumps(jsonData, ensure_ascii=False)
    # json_Ultimate=jsondatar[1:len(jsondatar) - 1]
    return {'Mysql_Sql_Error':None,'status':'-1','check':'sql检查成功，等待审核执行'}