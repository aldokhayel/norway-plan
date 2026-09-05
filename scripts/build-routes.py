"""Snapshot public OSRM car routing; ferry/boat/train remain explicitly schematic."""
import json,subprocess,concurrent.futures
from pathlib import Path
D=json.loads(Path('trip-data.json').read_text());P=D['points']
def route(item):
 key,seg=item
 coords=';'.join(str(P[p]['xy'][1])+','+str(P[p]['xy'][0]) for p in seg['points'])
 url='https://router.project-osrm.org/route/v1/driving/'+coords+'?overview=simplified&geometries=geojson&steps=false'
 try:
  s=subprocess.run(['curl','-fsS','--max-time','30',url],capture_output=True,text=True,check=True).stdout
  r=json.loads(s)['routes'][0]
  return key,dict(coords=[[y,x] for x,y in r['geometry']['coordinates']],km=round(r['distance']/1000),carHours=round(r['duration']/3600,2),source=url,checked='2026-09-05')
 except Exception as e:return key,dict(error='routing unavailable')
items=[(f"{d['n']}-{i}",s) for d in D['days'] for i,s in enumerate(d['segments']) if s['mode'] in ['road','bus']]
r=dict(concurrent.futures.ThreadPoolExecutor(4).map(route,items))
Path('routes.js').write_text('window.ROUTES = '+json.dumps(r)+';\n')
for k,v in r.items():print(k,v.get('km'),v.get('carHours'),v.get('error',''))
