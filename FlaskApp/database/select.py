
def select(filter_dict, count=False):
    condition_dict={}
    for k,v in filter_dict.items():
        if v!="":
            condition_dict.update({k:v})
    
    if count:
        query="""
            SELECT {columns}, COUNT(*) FROM BigTable GROUP BY {columns} {where}
        """.format(columns=", ".join(filter_dict.keys()), where="" if condition_dict=={} else "WHERE " + " AND ".join([k+"="+v for k,v in condition_dict.items()]))
        return query
    
    query="""
        SELECT * FROM BigTable {where}
    """.format(where="" if condition_dict=={} else ("WHERE " + " AND ".join([k+"="+v for k,v in condition_dict.items()])))
    
    return query