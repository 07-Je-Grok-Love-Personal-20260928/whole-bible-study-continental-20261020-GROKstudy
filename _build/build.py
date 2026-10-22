import sys
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p_timeline,p_geo,p_creeds,p_forms,p_cov,p_story,p_books,p_misc,p_gospels,p_life,p_kc,p_compare,p_stats
from books import QUOTES
from lib import SITE as S
out={'timeline.html':p_timeline.build(),'geography.html':p_geo.build(),'creeds.html':p_creeds.build(),'forms.html':p_forms.build(),'covenant.html':p_cov.build(),'story.html':p_story.build(),'ot.html':p_books.ot(),'nt.html':p_books.nt(),'index.html':p_misc.index(),'memory.html':p_misc.memory()}
out.update({'gospels.html':p_gospels.build(),'life-of-christ.html':p_life.build(),'kings-chronicles.html':p_kc.build(),'compare.html':p_compare.build(),'stats.html':p_stats.build()})
out['sources.html']=p_misc.sources()
for k,v in out.items(): open(S+k,'w').write(v); print(k,len(v))
print('verified short quotes:',len(QUOTES))
import merpre
merpre.run(list(out.keys()))
