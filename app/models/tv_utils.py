#  -*- coding: utf-8 -*-
from .item_utils import ItemUtils
from . import graph

class TvUtils(ItemUtils):

    @staticmethod
    def search_item(query):
        print "TvUtils search_item called with: query_text={0}".format(query)
        item_ids_str = ItemUtils.search_item_in_sql(query, 'TV')
        query = """MATCH (i:Item)
                WHERE i.item_id IN [{0}]
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.first_air_date, '-')[0] as year
                      ,filter(x in labels(i) WHERE x <> 'Item')[0] AS label
		ORDER BY i.popularity DESC
                LIMIT 25""".format(item_ids_str)
        print query
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr
