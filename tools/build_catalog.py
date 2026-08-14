#!/usr/bin/env python3
"""Generate browsable catalog views from an OCRDb bundle.

    python3 tools/build_catalog.py --bundle build/ocrdb-<ver>.json [--out .] [--html-out build]

Emits two deterministic, self-contained views (no external deps, byte-stable):
    CATALOG.md                      GitHub-rendered tree (browse in-repo now)
    build/ocrdb-<ver>.html          searchable/filterable single page (local + Pages later)

Both are generated from the built bundle, so they never drift from domains/.
"""
import argparse
import html
import json
import os


def _sorted_entries(dom):
    return sorted(dom["entries"].items())


def build_markdown(bundle):
    ver = bundle["version"]
    domains = bundle["domains"]
    total = sum(len(d["entries"]) for d in domains.values())
    L = []
    L.append(f"# OCRDb Catalog — v{ver}")
    L.append("")
    L.append(f"{total} finding types across {len(domains)} domains. "
             "Generated from `domains/` by `tools/build_catalog.py` — do not edit by hand. "
             "For a searchable view, open `build/ocrdb-%s.html`." % ver)
    L.append("")
    L.append("**Severity** INFO · LOW · MEDIUM · HIGH · CRITICAL — the *typical* grade "
             "for the defect type, not a per-instance verdict. **character**: `defect` "
             "(absent) or `opportunity`.")
    L.append("")
    L.append("## Domains")
    L.append("")
    L.append("| Domain | Name | Entries |")
    L.append("|---|---|---:|")
    for code, dom in domains.items():
        anchor = f"{code.lower()}--{dom['name']}"
        L.append(f"| [`{code}`](#{anchor}) | {dom['name']} | {len(dom['entries'])} |")
    L.append("")
    for code, dom in domains.items():
        L.append(f"## {code} — {dom['name']}")
        L.append("")
        areas = dom["areas"]
        for ak in sorted(areas):
            area = areas[ak]
            L.append(f"### {code}-{ak} · {area['name']}")
            L.append("")
            for ck in sorted(area.get("categories") or {}):
                cname = area["categories"][ck]
                rows = [(c, e) for c, e in _sorted_entries(dom)
                        if c.startswith(f"{code}-{ak}{ck}")]
                if not rows:
                    continue
                L.append(f"**{code}-{ak}{ck} · {cname}**")
                L.append("")
                L.append("| Code | Issue | Severity | CWE | Notes |")
                L.append("|---|---|---|---|---|")
                for c, e in rows:
                    cwe = ", ".join(e.get("cwe") or []) or "—"
                    tags = []
                    if e.get("character") == "opportunity":
                        tags.append("opportunity")
                    if e.get("automated_by"):
                        tags.append("auto: " + ", ".join(e["automated_by"]))
                    if e.get("status") == "deprecated":
                        tags.append("deprecated→" + str(e.get("superseded_by", "")))
                    note = "; ".join(tags) or "—"
                    L.append(f"| `{c}` | {e['name']} | {e['default_severity']} | {cwe} | {note} |")
                L.append("")
    return "\n".join(L) + "\n"


def _catalog_data(bundle):
    """Flat, render-ready records for the HTML view."""
    recs = []
    for dcode, dom in bundle["domains"].items():
        areas = dom["areas"]
        for code, e in _sorted_entries(dom):
            area = code.split("-")[1][0]
            recs.append({
                "code": code, "domain": dcode, "domainName": dom["name"],
                "area": f"{dcode}-{area}", "areaName": areas.get(area, {}).get("name", ""),
                "name": e["name"], "sev": e["default_severity"],
                "cwe": e.get("cwe") or [], "character": e.get("character", "defect"),
                "automated_by": e.get("automated_by") or [],
                "status": e.get("status", "active"),
                "provenance": e.get("provenance") or [],
                "examples": e.get("examples") or [],
            })
    return recs


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OCRDb Catalog — v__VER__</title>
<style>
:root{
  --paper:#f4f6f8;--surface:#fff;--sunk:#eef1f4;--ink:#1b2027;--muted:#586472;
  --faint:#8b939d;--line:#e1e5ea;--brass:#94701f;--brass-soft:#f1e8d0;
  --crit:#8a2f2a;--high:#b04f4a;--med:#94701f;--low:#566a88;--info:#7a8390;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --serif:ui-serif,Georgia,"Times New Roman",serif;
  --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#111419;--surface:#191d25;--sunk:#14181f;--ink:#e8ebef;--muted:#9aa3af;
  --faint:#69727f;--line:#282e37;--brass:#cea54e;--brass-soft:#2c2717;
  --crit:#e0847c;--high:#d8817a;--med:#cea54e;--low:#8a9bbd;--info:#8b95a3;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.55;-webkit-text-size-adjust:100%}
.wrap{max-width:1000px;margin:0 auto;padding:24px 18px 80px}
header{border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:6px}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brass);font-weight:600}
h1{font-family:var(--serif);font-size:1.8rem;margin:.2em 0 .1em}
.sub{color:var(--muted);font-size:.95rem;margin:0}
.controls{position:sticky;top:0;background:var(--paper);padding:14px 0 10px;z-index:5;border-bottom:1px solid var(--line);margin-bottom:8px}
#q{width:100%;font-family:var(--sans);font-size:1rem;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
#q:focus{outline:2px solid var(--brass);outline-offset:1px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font-family:var(--mono);font-size:.72rem;letter-spacing:.04em;padding:.34em .66em;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer;user-select:none}
.chip[aria-pressed="true"]{background:var(--brass-soft);color:var(--brass);border-color:var(--brass)}
.chip:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.count{font-family:var(--mono);font-size:.78rem;color:var(--faint);margin-top:9px}
details.dom{margin-top:18px;border:1px solid var(--line);border-radius:12px;background:var(--surface);overflow:hidden}
details.dom>summary{cursor:pointer;padding:13px 16px;font-family:var(--serif);font-size:1.15rem;font-weight:600;list-style:none;display:flex;align-items:baseline;gap:.6em}
details.dom>summary::-webkit-details-marker{display:none}
details.dom>summary .dcode{font-family:var(--mono);font-size:.85rem;color:var(--brass)}
details.dom>summary .dn{color:var(--muted);font-weight:400;font-size:.9rem}
.area{padding:2px 16px 8px}
.area h3{font-family:var(--sans);font-size:.82rem;text-transform:uppercase;letter-spacing:.06em;color:var(--faint);margin:16px 0 6px;font-weight:600}
.area h3 .ac{font-family:var(--mono);color:var(--brass);text-transform:none;letter-spacing:0}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:10px 12px;align-items:baseline;padding:9px 0;border-top:1px solid var(--line)}
.row .code{font-family:var(--mono);font-size:.82rem;color:var(--ink);white-space:nowrap}
.row .nm{font-size:.95rem}
.row .nm .meta{display:block;color:var(--faint);font-family:var(--mono);font-size:.72rem;margin-top:2px}
.sev{font-family:var(--mono);font-size:.66rem;font-weight:700;letter-spacing:.05em;padding:.28em .5em;border-radius:6px;white-space:nowrap;color:#fff}
.sev.CRITICAL{background:var(--crit)}.sev.HIGH{background:var(--high)}.sev.MEDIUM{background:var(--med)}
.sev.LOW{background:var(--low)}.sev.INFO{background:var(--info)}
.tag{font-family:var(--mono);font-size:.66rem;color:var(--brass);background:var(--brass-soft);padding:.2em .45em;border-radius:5px;margin-left:.4em}
.empty{color:var(--faint);padding:30px 0;text-align:center;font-family:var(--mono);font-size:.85rem}
mark{background:var(--brass-soft);color:var(--brass);border-radius:3px}
@media(max-width:560px){.row{grid-template-columns:1fr auto}.row .code{grid-column:1;color:var(--brass)}}
</style></head>
<body><div class="wrap">
<header>
  <div class="eyebrow">Open Code Review Database</div>
  <h1>Catalog · v__VER__</h1>
  <p class="sub">__TOTAL__ finding types · __NDOM__ domains · __LICENSE__ · generated from <code>domains/</code></p>
</header>
<div class="controls">
  <input id="q" type="search" placeholder="Search code, name, CWE… (e.g. injection, CWE-89, AGT)" autocomplete="off">
  <div class="chips" id="domChips"></div>
  <div class="chips" id="sevChips"></div>
  <div class="count" id="count"></div>
</div>
<div id="results"></div>
</div>
<script>
const DATA=__DATA__;
const DOMAINS=__DOMAINS__;
const SEVS=["CRITICAL","HIGH","MEDIUM","LOW","INFO"];
const state={q:"",doms:new Set(),sevs:new Set()};
const el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;};
function chip(label,set,val,box){const c=el("button","chip",label);c.setAttribute("aria-pressed","false");
  c.onclick=()=>{if(set.has(val)){set.delete(val);c.setAttribute("aria-pressed","false");}else{set.add(val);c.setAttribute("aria-pressed","true");}render();};box.appendChild(c);}
DOMAINS.forEach(d=>chip(d.code,state.doms,d.code,domChips));
SEVS.forEach(s=>chip(s,state.sevs,s,sevChips));
document.getElementById("q").addEventListener("input",e=>{state.q=e.target.value.trim().toLowerCase();render();});
function esc(s){return s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function hl(s){if(!state.q)return esc(s);const i=s.toLowerCase().indexOf(state.q);if(i<0)return esc(s);
  return esc(s.slice(0,i))+"<mark>"+esc(s.slice(i,i+state.q.length))+"</mark>"+esc(s.slice(i+state.q.length));}
function match(r){
  if(state.doms.size&&!state.doms.has(r.domain))return false;
  if(state.sevs.size&&!state.sevs.has(r.sev))return false;
  if(state.q){const hay=(r.code+" "+r.name+" "+r.cwe.join(" ")+" "+r.areaName+" "+r.domainName).toLowerCase();
    if(!hay.includes(state.q))return false;}
  return true;
}
function render(){
  const res=document.getElementById("results");res.textContent="";
  const rows=DATA.filter(match);
  document.getElementById("count").textContent=rows.length+" of "+DATA.length+" entries";
  if(!rows.length){res.appendChild(el("div","empty","No entries match."));return;}
  const byDom={};rows.forEach(r=>{(byDom[r.domain]=byDom[r.domain]||[]).push(r);});
  DOMAINS.forEach(d=>{
    const rs=byDom[d.code];if(!rs)return;
    const det=el("details","dom");det.open=(!!state.q||state.doms.size>0);
    const sum=el("summary",null,'<span class="dcode">'+d.code+'</span><span>'+esc(d.name)+'</span><span class="dn">'+rs.length+'</span>');
    det.appendChild(sum);
    const byArea={};rs.forEach(r=>{(byArea[r.area]=byArea[r.area]||[]).push(r);});
    Object.keys(byArea).sort().forEach(area=>{
      const wrap=el("div","area");
      const a=byArea[area][0];
      wrap.appendChild(el("h3",null,'<span class="ac">'+area+'</span> · '+esc(a.areaName)));
      byArea[area].forEach(r=>{
        let meta=r.cwe.join(" · ");
        if(r.character==="opportunity")meta+=(meta?' · ':'')+'opportunity';
        if(r.automated_by.length)meta+=(meta?' · ':'')+'auto:'+r.automated_by.join(",");
        const row=el("div","row");
        row.appendChild(el("span","code",hl(r.code)));
        row.appendChild(el("span","nm",'<span>'+hl(r.name)+'</span>'+(meta?'<span class="meta">'+esc(meta)+'</span>':'')));
        row.appendChild(el("span","sev "+r.sev,r.sev));
        wrap.appendChild(row);
      });
      det.appendChild(wrap);
    });
    res.appendChild(det);
  });
}
render();
</script>
</body></html>
"""


def _json_for_script(obj, **dumps_kw):
    """json.dumps output safe to embed inside an inline <script> element.

    Escapes the characters that can terminate the <script> element or break
    JS parsing -- `<`, `>`, `&`, and the U+2028/U+2029 line separators -- as
    `\\uXXXX`. These are valid JSON and parse back to the identical values, so
    the embedded data is unchanged, but no catalog field (name, examples,
    definition, area names) can close the tag or inject markup (CWE-79/116).
    """
    s = json.dumps(obj, **dumps_kw)
    return (s.replace("<", "\\u003c").replace(">", "\\u003e")
             .replace("&", "\\u0026")
             .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def build_html(bundle):
    recs = _catalog_data(bundle)
    domains = [{"code": c, "name": d["name"]} for c, d in bundle["domains"].items()]
    total = len(recs)
    out = HTML_TEMPLATE
    out = out.replace("__VER__", html.escape(bundle["version"]))
    out = out.replace("__TOTAL__", str(total))
    out = out.replace("__NDOM__", str(len(domains)))
    out = out.replace("__LICENSE__", html.escape(bundle.get("license", "")))
    out = out.replace("__DATA__", _json_for_script(recs, sort_keys=True, separators=(",", ":")))
    out = out.replace("__DOMAINS__", _json_for_script(domains, separators=(",", ":")))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", default=".", help="dir for CATALOG.md")
    ap.add_argument("--html-out", default="build", help="dir for the HTML view")
    args = ap.parse_args(argv)
    with open(args.bundle, encoding="utf-8") as fh:
        bundle = json.load(fh)
    md_path = os.path.join(args.out, "CATALOG.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(build_markdown(bundle))
    os.makedirs(args.html_out, exist_ok=True)
    html_path = os.path.join(args.html_out, f"ocrdb-{bundle['version']}.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(build_html(bundle))
    total = sum(len(d["entries"]) for d in bundle["domains"].values())
    print(f"catalog: {total} entries -> {md_path}, {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
