"""quick builder for v6 pages only: python3 _build/build6.py [module ...]"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import SITE as S
import importlib
MODS={'gospels.html':'p_gospels','life-of-christ.html':'p_life','kings-chronicles.html':'p_kc','compare.html':'p_compare','stats.html':'p_stats'}
want=sys.argv[1:] or list(MODS)
for fn in want:
    if fn not in MODS: fn=[k for k,v in MODS.items() if v==fn or k.startswith(fn)][0]
    m=importlib.import_module(MODS[fn]); html_=m.build(); open(S+fn,'w').write(html_); print(fn,len(html_))
