# Builds plan.json: for each dua, the full clip and one clip per line.
import json
H = lambda f, a, b, x=False: {"file": f"h{f}.mp3", "from": a, "to": b, "exact_from": x}
Q = lambda k, w0, w1: {"quran": k, "words": [w0, w1]}
END = -0.05
duas = {
 "travel":    [[H(16,5.18,9.94)], [H(16,9.94,END)]],
 "ride":      [[H(206,6.58,11.2,True)], [H(206,11.2,17.76)], [H(206,17.76,22.62)], [H(206,22.62,29.82)], [H(206,29.82,36.14)], [H(206,36.14,41.04)], [H(206,41.04,END)]],
 "talbiyah":  [[H(233,7.74,11.02)], [H(233,11.02,14.28)], [H(233,14.28,18.32)], [H(233,18.32,END)]],
 "enter":     [[H(20,3.98,10.38)], [H(20,10.38,16.54)], [H(20,16.58,22.04)], [H(20,22.04,END)]],
 "exit":      [[H(21,4.34,10.36)], [H(21,10.36,14.34)], [H(21,14.34,END)]],
 "kaaba":     [[H(206,29.82,36.14)], [H(236,31.44,35.14)]],
 "tawafStart":[[H(16,5.18,7.24), H(206,29.82,32.02)]],
 "rabbana":   [[H(235,5.56,10.5,True)], [H(235,10.5,13.48)], [H(235,13.48,END)]],
 "maqam":     [[Q("2:125",7,11)]],
 "zamzam":    [[H(73,0.0,4.12)], [H(73,4.52,7.16)], [H(73,7.16,9.2)]],
 "safaVerse": [[Q("2:158",1,6)], [H(236,15.56,18.22)]],
 "safaDhikr": [[H(206,29.82,36.14)], [H(236,31.44,36.16)], [H(236,36.16,41.16)], [H(236,41.16,47.3)], [H(236,47.3,51.84)]],
 "durood":    [[H(53,7.38,13.24)], [H(53,13.24,19.32)], [H(53,19.32,22.0)], [H(53,22.0,28.02)], [H(53,28.02,33.78)], [H(53,33.78,END)]],
 "istighfar": [[H(250,4.18,6.46,True)], [H(250,6.46,10.46)], [H(250,10.46,11.7)]],
 "forgive":   [[H(48,5.34,END)]],
 "parents":   [[Q("17:24",7,12)]],
 "family":    [[Q("25:74",3,13)]],
 "ease":      [[Q("20:25",2,5)], [Q("20:26",1,3)]],
 "knowledge": [[Q("20:114",-4,-1)]],
 "hasbun":    [[Q("3:173",-4,-1)]],
 "baqi":      [[H(165,3.74,9.72,True)], [H(165,9.72,14.58)], [H(165,14.58,20.58)], [H(165,20.58,END)]],
}
plan = {}
for id, lines in duas.items():
    plan[id] = [p for line in lines for p in line]
    for i, line in enumerate(lines, 1):
        plan[f"{id}-{i}"] = line
json.dump(plan, open("plan.json", "w"), indent=1)
json.dump({k: len(v) for k, v in duas.items()}, open("counts.json", "w"))
print(len(plan), "clips")
