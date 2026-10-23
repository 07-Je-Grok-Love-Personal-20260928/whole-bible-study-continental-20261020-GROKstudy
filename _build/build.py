import sys
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p_timeline,p_geo,p_creeds,p_forms,p_cov,p_story,p_books,p_misc,p_gospels,p_life,p_kc,p_compare,p_stats,p_pent,p_hist,p_poet,p_proph,p_epis
from books import QUOTES
from lib import SITE as S
out={'timeline.html':p_timeline.build(),'geography.html':p_geo.build(),'creeds.html':p_creeds.build(),'forms.html':p_forms.build(),'covenant.html':p_cov.build(),'story.html':p_story.build(),'index.html':p_books.books(),'overview.html':p_misc.index(),'ot.html':p_books.stub('ot.html','ot','旧约39卷'),'nt.html':p_books.stub('nt.html','nt','新约27卷'),'memory.html':p_misc.memory()}
out.update({'gospels.html':p_gospels.build(),'life-of-christ.html':p_life.build(),'kings-chronicles.html':p_kc.build(),'compare.html':p_compare.build(),'stats.html':p_stats.build()})
out['pentateuch.html']=p_pent.build()
out['history.html']=p_hist.build()
out['poetry.html']=p_poet.build()
out['prophets.html']=p_proph.build()
out['epistles.html']=p_epis.build()
import p_harmony
out['harmony.html']=p_harmony.build()
import p_acts
out['acts.html']=p_acts.build()
import p_culture
out['culture.html']=p_culture.build()
out['sources.html']=p_misc.sources()  # last: counts every verified quote (harmony/acts add some)
import re as _re
def _fix(v):
    v=_re.sub(r'href="(?:ot|nt)\.html#','href="index.html#',v)
    return v.replace('href="ot.html"','href="index.html#ot"').replace('href="nt.html"','href="index.html#nt"')
for k,v in out.items():
    if k not in ('ot.html','nt.html'): v=_fix(v)
    open(S+k,'w').write(v); print(k,len(v))
print('verified short quotes:',len(QUOTES))
import merpre
merpre.run(list(out.keys()))
import subprocess,sys
r=subprocess.run([sys.executable,__import__('os').path.join(__import__('os').path.dirname(__file__),'links.py')],capture_output=True,text=True);print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode: print(r.stdout); sys.exit(1)
