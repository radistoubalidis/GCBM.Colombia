import os
import json
import pandas as pd

def calc_metrics(period,ind_type,data):
    lifezones = data['LifeZone'].unique()
    for zone in lifezones:
        zone_data = data[data['LifeZone'] == zone]
        metrics = {
            'pool_tc_sum_mean' : float(zone_data['pool_tc_sum'].mean()),
            'area_sum_mean' : float(zone_data['area_sum'].mean()),
            'pool_tc_per_ha_mean': float(zone_data['pool_tc_per_ha'].mean())            
        }
        formatted_zone = zone.replace(' ','_')
        formatted_name = f"{period}_{ind_type}_{formatted_zone}.json"
        with open(os.path.join('metrics',formatted_name),'w') as out:
            json.dump(metrics,out)

if __name__ == "__main__":
    pools = pd.read_csv(os.path.join('Tables','Pools_DOM_Sensitivity_full.csv'))

    pools_divided = [
        {'period':'1900-1950','data':pools[pools['year']<=1950]},
        {'period':'1951-2000','data':pools[(pools['year']>1950) & (pools['year']<=2000)]},
        {'period':'2001-2050','data':pools[pools['year']>2000]}
        ]

    indicators = pools['indicator'].unique()
    for pool in pools_divided:
        for ind_type in indicators:
            pool_data = pool.get('data')
            ind_data = pool_data[pool_data['indicator'] == ind_type]
            calc_metrics(pool['period'],ind_type,ind_data)