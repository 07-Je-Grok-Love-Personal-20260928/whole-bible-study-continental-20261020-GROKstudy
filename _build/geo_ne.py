"""v9: vendored Natural Earth (public domain, naturalearthdata.com) offline base.
Source GeoJSON: github.com/nvkelso/natural-earth-vector (10m land / lakes / rivers_lake_centerlines), clipped to the
biblical world (lon 0–72, lat 12–50) and simplified. Output: assets/data/ne.js (window.NE) + helpers for SVG concept maps."""
import json,os
from shapely.geometry import shape,box,mapping,Polygon,MultiPolygon,LineString,MultiLineString
SRC=os.environ.get('NE_SRC','/workspace/ne')
BB=(0,12,72,50)
RIV={'Nile':'尼罗河','Rosetta Branch':'尼罗河（罗塞塔支）','Damietta Branch':'尼罗河（杜姆亚特支）','Tigris':'底格里斯河','Dicle':'底格里斯河','Euphrates':'幼发拉底河','Firat':'幼发拉底河','Al Furat':'幼发拉底河','Jordan':'约旦河','Kiz?lirmak':'哈吕斯河','Tevere':'台伯河','Danube':'多瑙河','Karkheh':'乌莱河（卡尔黑河）','Shatt al Arab':'阿拉伯河','Byk Menderes':'迈安德河','Haliacmon':'哈利阿克蒙河','Evros':'赫布鲁斯河','Ceyhan':'皮拉摩斯河','Aras':'阿拉斯河','Kura':'库拉河','Sakarya':'桑加里乌斯河','Murat':'幼发拉底河（东源）','Po':'波河','Strymnas':'斯特里蒙河','Kelkit':'吕科斯河','Simav':'','Talkeh':'','Morava':'','Drina':'','Sava':''}
CORE=box(24,27,50,40)
SKIPR=('Canal','Channel','Hindiyah','Gharraf')
LAK={'Dead Sea':'死海（盐海）','Sea of Galilee':'加利利海','Lake Van':'凡湖','Lake Urmia':'乌鲁米耶湖','Lake Tuz':'图兹湖','Lake Sevan':'塞凡湖','Great Bitter Lake':'大苦湖','Lake Hammar':'哈马尔沼','Beyşehir':'','Eğirdir':'','Lake Skadar':'','Syvash':''}
def r(x):return round(x,3)
def ring(c):return [[r(a),r(b)] for a,b in c]
def load(n):return json.load(open(os.path.join(SRC,n+'.geojson')))['features']
def land(tol=.025):
    B=box(*BB);ps=[]
    for f in load('ne_10m_land'):
        g=shape(f['geometry']).intersection(B)
        if g.is_empty:continue
        g=g.simplify(tol,preserve_topology=True)
        for p in (g.geoms if hasattr(g,'geoms') else [g]):
            if isinstance(p,Polygon) and p.area>.004:ps.append(p)
    return ps
def lakes():
    B=box(*BB);out=[]
    for f in load('ne_10m_lakes'):
        n=f['properties'].get('name');
        if n not in LAK:continue
        g=shape(f['geometry']).intersection(B).simplify(.004,preserve_topology=True)
        for p in (g.geoms if hasattr(g,'geoms') else [g]):
            if isinstance(p,Polygon):out.append((LAK[n],p))
    return out
def rivers():
    B=box(*BB);out=[]
    for f in load('ne_10m_rivers_lake_centerlines'):
        n=f['properties'].get('name') or ''
        if any(s in n for s in SKIPR) or (f['properties'].get('scalerank') or 9)>9:continue
        g=shape(f['geometry']).intersection(B)
        if g.is_empty:continue
        g=g.simplify(.01)
        for l in (g.geoms if hasattr(g,'geoms') else [g]):
            if isinstance(l,LineString) and l.length>.15 and (RIV.get(n) or l.intersects(CORE)):out.append((RIV.get(n,''),l))
    return out
def write(path):
    L=land();K=lakes();R=rivers()
    d={'land':[[ring(p.exterior.coords)] for p in L],'lakes':[{'n':n,'c':[ring(p.exterior.coords)]} for n,p in K],'rivers':[{'n':n,'c':ring(l.coords)} for n,l in R]}
    s='window.NE='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';'
    open(path,'w').write(s);return len(s),len(L),len(K),len(R)
_cache={}
def geoms():
    if not _cache:_cache.update(land=land(),lakes=lakes(),rivers=rivers())
    return _cache
if __name__=='__main__':print(write(os.path.join(os.path.dirname(__file__),'..','assets','data','ne.js')))
