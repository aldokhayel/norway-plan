"""Regenerate browser data and the text itinerary from the canonical JSON."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
t=json.loads((root/'trip-data.json').read_text())
(root/'trip-data.js').write_text('window.TRIP = '+json.dumps(t,ensure_ascii=False)+';\n')
camps={c['id']:c for c in t['camps']}
lines=['# رحلة البحيرات والفيوردات · 19–29 سبتمبر 2026','',
'3 بالغين · 10 ليالٍ · 11 تاريخًا تقويميًا · تحديث 5 سبتمبر 2026','',
'الوصول إلى ستوكهولم 19 سبتمبر الساعة 08:00؛ الاستلام المخطط 11:00. إعادة الكرفان في Touring Cars، Bristagatan 12، قبل 12:00 يوم 29 سبتمبر؛ الإقلاع 16:00. انتقال المطار يفترض Arlanda ARN.','',
'بعد تفويض زيادة الساعات: أغلب الأيام 09:00–19:00، والانتقالات 08:00–20:00 عند الحاجة. زيارة أوسلو 27 سبتمبر 09:00–13:00، وستوكهولم 28 سبتمبر 14:00–18:00.','',
'رابط بحث الكرفان يذكر شخصين وإعادة 15:00؛ المطلوب تأكيد حجز لـ3 بالغين وإعادة 12:00. لم تنفذ أي حجوزات.','',
'## مراجعة المسار','',
'الخطة السابقة كانت تعتمد على قواعد مكررة وتترك 7–8 ساعات قيادة من Lillehammer ليوم التسليم. الخطة الحالية حلقة شمالية ثم جنوبية بعشرة مخيمات مختلفة، وتنتهي بليلة في ستوكهولم. استُخدم الرسم المرفق للاتجاه العام؛ تعذر الوصول إلى محتوى فيديو YouTube. لا ننسب له تفاصيل غير متحققة.','',
'20–23 سبتمبر: الشمال الغربي، مع يوم 20 للعبور الطويل ويوم 23 لبريكسدال والانتقال جنوبًا. 24–26: فلام وهاردانغر ثم أوسلو. 27–29: المدينتان والتسليم.','',
'الأسعار مخصصات تقديرية ما لم توصف بأنها منشورة. تقييمات Google من صفحات Google أو مصادر ناقلة مسماة، وليست أرقامًا حية. الإطلالة والموقف وخدمات آخر سبتمبر تحتاج تأكيدًا.','']
for d in t['days']:
 lines += [f"## {d['n']} · {d['date']} · {d['title']}",'',f"{d['hours']} · حوالي {d['km']} كم · قيادة {d['drive']}",'',d['desc'],'']
 lines += [f"- **{s['time']}**: {s['text']}" for s in d['schedule']]
 lines+=['','### الأنشطة والتكلفة','']+['- '+c for c in d['costs']]
 if d['camp']:
  c=camps[d['camp']];price='–'.join(map(str,c['price']))
  rate=('%.1f/5 Google'%c['rating']) if c.get('rating') is not None else 'التقييم على خرائط Google'
  lines += ['','### مخيم الليلة','',f"[{c['name']}]({c['web']}) · [{rate}]({c['ratingSource']}) · {price} {c['currency']} للكرفان والثلاثة.",'',c['view']+'. '+c['services'], '',c['season'], '',f"[مصدر الموسم والخدمات]({c['seasonSource']})",'',c['tradeoff']]
 if d.get('grocery'):
  g=d['grocery'];lines+=['','### تسوّق قبل الحدود','',f"[{g['name']}]({g['map']}) — {g['town']}. {g['note']}"]
 if d.get('food'):
  lines+=['','### توقف طعام مميز','']+[f"- [{f['name']}]({f['map']}) · {f['type']}"+(f" · ★{f['rating']}" if f.get('rating') is not None else '') for f in d['food']]
 lines+=['','### ملاحظات','']+['- '+n for n in d['notes']]+['']
lines+=['## ميزانية ومصادر','',
'إيجار الكرفان والتأمين والوديعة والطيران خارج التقديرات. ثمن الوقود يحسب عند التعبئة؛ افتراض الاستهلاك 11–14 لتر/100 كم. الطعام 600–900 كرونة يوميًا للمجموعة بعملة البلد مع الطبخ، وزيادة للمطاعم. لا تجمع NOK مع SEK دون سعر صرف.','',
'القطار + قارب Nærøyfjord + حافلة العودة: 4,800–6,300 NOK للثلاثة. العبّارات الثلاث: 1,800–3,200 NOK للمركبة والمجموعة. تلفريك واحد اختياري 1,800–2,550 NOK للمجموعة. احتياط الطرق والمواقف والنقل 2,000–3,500 NOK و500–1,000 SEK.','']
for currency in ['NOK','SEK']:
 cs=[c for c in t['camps'] if c['currency']==currency];sums=[sum(c['price'][i] for c in cs) for i in [0,1]]
 lines += [f"- المخيمات: {sums[0]}–{sums[1]} {currency}."]
lines+=['']+[f'- [{n}]({u})' for n,u in t['sources']]
(root/'PLAN.md').write_text('\n'.join(lines)+'\n')
print('Generated trip-data.js and PLAN.md from trip-data.json.')
