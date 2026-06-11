/* =========================================================================
 * SkillCODER 展示前端 · 纯原生 JS（无框架、无构建，便于阅读）
 *
 * 数据全部来自后端 :8000。本文件做四件事：
 *   0) 从 /api/ui/text 拉取「界面文案」并填充所有静态文字（文案的真源在后端）
 *   1) 探活后端，拉取案例列表与指标
 *   2) 选中案例后拉取「八步故事流」，按 visual.type 渲染每一步
 *   3) 提供上一步/下一步/自动播放交互，并渲染裁决卡与指标页
 *
 * 注意：本文件不再内嵌业务中文文案。所有界面文字都来自后端 UI_TEXT。
 *       唯一例外是下方 BOOTSTRAP —— 后端未连接时的提示，必须在没有后端的
 *       情况下也能显示，因此保留一份最小兜底（其同样的文案在后端 UI_TEXT 里）。
 * ========================================================================= */

const API = window.API_BASE;
const $ = (s) => document.querySelector(s);
const el = (html) => { const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; };
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const pct = (x) => (x == null ? "—" : (x * 100).toFixed(1) + "%");
const num = (x) => (x == null ? "—" : (+x).toFixed(4));

// 文案模板替换：把 "{key}" 换成 vars[key]（缺省替空串）。
// 模板里可含 HTML 标记；需要转义的值请在传入前先 esc()。
const fmt = (tpl, vars) =>
  String(tpl ?? "").replace(/\{(\w+)\}/g, (_, k) => (vars && k in vars ? String(vars[k]) : ""));

// 后端未连接时的最小兜底文案（无法从后端获取，因为后端正是不可达的那个）。
// 同样的文案在后端 UI_TEXT 里也有一份；后端连上后会用后端文案覆盖。
const BOOTSTRAP = {
  wait: "连接后端中…",
  bad: "● 后端未连接",
  offline: {
    title: "⚠️ 没有连接到后端",
    desc: "请先启动后端服务，再刷新本页面：",
    url_label: "当前尝试连接：",
    button: "重新连接",
  },
};

// 三大阶段 → 主题色（与后端 step.phase 对应）。label 来自后端 UI.phases。
const PHASE = {
  embedding: { color: "var(--embedding)" },
  deploy: { color: "var(--deploy)" },
  verification: { color: "var(--verification)" },
};
function phaseOf(p) {
  const color = (PHASE[p] || PHASE.embedding).color;
  const label = (UI && UI.phases && (UI.phases[p] || UI.phases.embedding)) || "";
  return { color, label };
}

async function getJSON(path) {
  const r = await fetch(API + path);
  if (!r.ok) throw new Error(path + " -> " + r.status);
  return r.json();
}

/* ---------------- 全局状态 ---------------- */
let UI = null;        // 后端下发的界面文案字典（/api/ui/text）
let CURRENT = null;   // 当前案例的完整 timeline 数据
let STEP = 0;         // 当前步骤索引 0..7
let PLAY = null;      // 自动播放定时器

/* ===================== 启动 ===================== */
applyBootstrap();
boot();

// 后端连接前先填好兜底文案（连接状态 + 离线提示卡），保证无后端也可读。
function applyBootstrap() {
  $("#conn").textContent = BOOTSTRAP.wait;
  $("#offline-title").textContent = BOOTSTRAP.offline.title;
  $("#offline-desc").textContent = BOOTSTRAP.offline.desc;
  $("#offline-url-label").textContent = BOOTSTRAP.offline.url_label;
  $("#offline-btn").textContent = BOOTSTRAP.offline.button;
}

async function boot() {
  $("#offline-url").textContent = API;
  try {
    await getJSON("/api/health");
    UI = await getJSON("/api/ui/text");
    applyStaticText();
    $("#conn").className = "conn conn-ok";
    $("#conn").textContent = UI.meta.conn.ok;
    $("#page").classList.remove("hidden");
    $("#offline").classList.add("hidden");
    const [cases, metrics] = await Promise.all([
      getJSON("/api/demo/cases"),
      getJSON("/api/metrics/overview"),
    ]);
    renderCases(cases);
    renderMetrics(metrics);
  } catch (e) {
    $("#conn").className = "conn conn-bad";
    $("#conn").textContent = (UI && UI.meta && UI.meta.conn.bad) || BOOTSTRAP.bad;
    $("#page").classList.add("hidden");
    $("#offline").classList.remove("hidden");
    console.error(e);
  }
}

/* ===================== 用后端文案填充静态界面 ===================== */
function applyStaticText() {
  // 顶部导航
  const m = UI.meta;
  document.title = m.title;
  $("#brand-title").textContent = m.brand_title;
  $("#brand-sub").textContent = m.brand_sub;
  $("#nav-links").innerHTML = m.nav.map((n) => `<a href="${n.href}">${esc(n.label)}</a>`).join("");

  // 离线提示卡（与 BOOTSTRAP 同文，连上后端后由后端文案驱动）
  const o = UI.offline;
  $("#offline-title").textContent = o.title;
  $("#offline-desc").textContent = o.desc;
  $("#offline-url-label").textContent = o.url_label;
  $("#offline-btn").textContent = o.button;

  // ① hero 背景区
  const h = UI.hero;
  $("#hero-h1").textContent = h.h1;
  $("#hero-lead").innerHTML = h.lead;
  $("#hero-grid").innerHTML = h.cards.map((c) =>
    `<div class="hero-card${c.highlight ? " hero-card-hi" : ""}">
      <div class="hc-icon">${c.icon}</div>
      <h3>${esc(c.title)}</h3>
      <p>${c.body}</p>
    </div>`).join("");
  $("#hero-flow").innerHTML = h.flow.map((s, i) =>
    `<span>${esc(s)}</span>` + (i < h.flow.length - 1 ? "<i>→</i>" : "")).join("");
  $("#hero-cta").textContent = h.cta;

  // ② / ③ / ④ / ⑤ 各区块标题
  const S = UI.sections;
  $("#cases-h2").textContent = S.cases.h2;
  $("#cases-desc").textContent = S.cases.desc;
  $("#attack-legend").innerHTML = S.cases.attack_legend.map((t) => `<span>${t}</span>`).join("");
  $("#story-h2").textContent = S.story.h2;
  $("#story-sub").textContent = S.story.sub_default;
  $("#verdict-h2").textContent = S.verdict.h2;
  $("#verdict-empty").textContent = S.verdict.empty;
  $("#metrics-h2").textContent = S.metrics.h2;
  $("#metrics-desc").textContent = S.metrics.desc;

  // 故事流控制条
  const C = UI.controls;
  $("#btn-prev").textContent = C.prev;
  $("#btn-next").textContent = C.next;
  $("#btn-play").textContent = C.play;
  $("#tech-summary").textContent = C.tech_summary;

  // 页脚
  $("#foot-text").textContent = UI.footer;
}

/* ===================== ② 案例卡 ===================== */
function attackTag(attack) {
  const a = UI.attack_tags;
  if (attack === "none") return `<span class="tag tag-clean">${esc(a.none)}</span>`;
  if (attack === "type1_rewrite") return `<span class="tag tag-atk1">${esc(a.type1)}</span>`;
  return `<span class="tag tag-atk2">${esc(a.type2)}</span>`;
}
function renderCases(cases) {
  const box = $("#cases");
  box.innerHTML = "";
  cases.forEach((c) => {
    const card = el(`
      <div class="case-card" data-id="${c.case_id}">
        <div class="case-tags">
          <span class="tag tag-buyer">${esc(c.buyer_id)}</span>
          ${attackTag(c.attack)}
        </div>
        <h3>${esc(c.title)}</h3>
        <p>${esc(c.goal)}</p>
        <div class="case-go">${esc(UI.case_card.go)}</div>
      </div>`);
    card.onclick = () => selectCase(c.case_id, card);
    box.appendChild(card);
  });
}

/* ===================== ③ 选中案例 → 故事流 ===================== */
async function selectCase(caseId, card) {
  document.querySelectorAll(".case-card").forEach((x) => x.classList.remove("active"));
  if (card) card.classList.add("active");
  stopPlay();
  $("#story-sub").innerHTML = `<span class="spin"></span>${esc(UI.story.loading)}`;
  $("#story").classList.add("hidden");
  try {
    CURRENT = await getJSON("/api/demo/cases/" + caseId);
    STEP = 0;
    const p = CURRENT.provenance;
    const srcTagText = p.data_source === "real"
      ? `<span class="src-tag src-real">${esc(UI.story.src_real)}</span>`
      : `<span class="src-tag src-sim">${esc(UI.story.src_sim)}</span>`;
    $("#story-sub").innerHTML = fmt(UI.story.cur_case, {
      title: esc(CURRENT.title), model: p.model || "—", agent: p.agent || "—", src_tag: srcTagText,
    });
    $("#foot-prov").textContent = p.note || "";
    buildStepper();
    renderStep();
    renderVerdict();
    $("#story").classList.remove("hidden");
    $("#sec-story").scrollIntoView({ behavior: "smooth" });
  } catch (e) {
    $("#story-sub").textContent = fmt(UI.story.load_failed, { msg: e.message });
    console.error(e);
  }
}

/* 阶段进度条 */
function buildStepper() {
  const s = $("#stepper");
  s.innerHTML = "";
  CURRENT.timeline.forEach((step, i) => {
    const c = phaseOf(step.phase).color;
    const pip = el(`
      <div class="pip" style="--accent:${c}" data-i="${i}">
        <div class="pip-no">${esc(UI.controls.pip_step)} ${step.index}</div>
        <div class="pip-tt">${esc(step.title)}</div>
        <div class="bar"></div>
      </div>`);
    pip.onclick = () => { stopPlay(); STEP = i; renderStep(); };
    s.appendChild(pip);
  });
}

/* 渲染当前步骤 */
function renderStep() {
  const step = CURRENT.timeline[STEP];
  const phase = phaseOf(step.phase);
  $("#step-stage").style.setProperty("--accent", phase.color);

  $("#step-no").textContent = step.index;
  $("#step-no").style.background = phase.color;
  $("#step-title").textContent = step.title;
  $("#step-phase").textContent = phase.label;
  $("#step-phase").style.color = phase.color;
  $("#step-story").textContent = step.story;
  $("#step-story").style.borderColor = phase.color;
  $("#step-tech").textContent = step.technical_hint;

  $("#step-visual").innerHTML = "";
  // 论点 + 要点（来自补全内容层）
  if (step.thesis) $("#step-visual").appendChild(el(`<div class="thesis">💡 ${esc(step.thesis)}</div>`));
  if (step.explanations && step.explanations.length) {
    const items = step.explanations.filter(Boolean).map((x) => `<li>${esc(x)}</li>`).join("");
    $("#step-visual").appendChild(el(`<ul class="explain-list">${items}</ul>`));
  }
  $("#step-visual").appendChild(renderVisual(step.visual));

  // 进度条状态
  document.querySelectorAll(".stepper .pip").forEach((p, i) => {
    p.classList.toggle("cur", i === STEP);
    p.classList.toggle("done", i < STEP);
  });
  // 圆点
  const dots = $("#dots"); dots.innerHTML = "";
  CURRENT.timeline.forEach((_, i) => {
    const d = el(`<div class="dot ${i === STEP ? "cur" : ""}" style="--accent:${phase.color}"></div>`);
    d.style.background = i === STEP ? phase.color : "";
    d.onclick = () => { stopPlay(); STEP = i; renderStep(); };
    dots.appendChild(d);
  });
  $("#btn-prev").disabled = STEP === 0;
  $("#btn-next").disabled = STEP === CURRENT.timeline.length - 1;
}

/* 控制条 */
$("#btn-prev").onclick = () => { stopPlay(); if (STEP > 0) { STEP--; renderStep(); } };
$("#btn-next").onclick = () => { stopPlay(); if (STEP < CURRENT.timeline.length - 1) { STEP++; renderStep(); } };
$("#btn-play").onclick = () => (PLAY ? stopPlay() : startPlay());
function startPlay() {
  $("#btn-play").textContent = UI.controls.pause;
  PLAY = setInterval(() => {
    if (STEP < CURRENT.timeline.length - 1) { STEP++; renderStep(); }
    else stopPlay();
  }, 2600);
}
function stopPlay() { if (PLAY) clearInterval(PLAY); PLAY = null; if (UI) $("#btn-play").textContent = UI.controls.play; }

/* ===================== 8 个 visual 渲染器 ===================== */
function renderVisual(v) {
  const fn = VISUAL[v.type];
  return fn ? fn(v) : el(`<pre>${esc(JSON.stringify(v, null, 2))}</pre>`);
}
function srcTag(s) {
  return s === "real" ? `<span class="src-tag src-real">${esc(UI.src_tag.real)}</span>`
       : s === "simulated" ? `<span class="src-tag src-sim">${esc(UI.src_tag.sim)}</span>` : "";
}

/* —— 通用展示小部件 —— */
function explainBox(title, text) {
  return `<div class="explain-box"><b>${esc(title)}</b><p>${esc(text)}</p></div>`;
}
function kvTable(obj) {
  const rows = Object.entries(obj || {}).map(([k, v]) =>
    `<tr><td><code>${esc(k)}</code></td><td>${esc(v)}</td></tr>`).join("");
  return `<table class="mtable"><tbody>${rows}</tbody></table>`;
}
// 两栏文件 diff（before 删除红 / after 新增绿）
function renderDiff(d) {
  if (!d) return "";
  const hl = new Set(d.highlights || []);
  const isHL = (t) => [...hl].some((h) => h && t.includes(h));
  const col = (side) =>
    side.lines.map((ln) => {
      const cls = "dl dl-" + ln.status + (isHL(ln.text) && ln.status !== "same" ? " dl-hl" : "");
      const no = ln.line == null ? "" : String(ln.line).padStart(3, "0");
      return `<div class="${cls}"><span class="dn">${no}</span><span class="dt">${esc(ln.text)}</span></div>`;
    }).join("");
  const st = d.stats || {};
  return `<div class="diff">
    <div class="diff-col"><div class="diff-head diff-before">${esc(d.before.label)} <span class="diff-stat">−${st.removed || 0}</span></div>
      <div class="diff-body scroll">${col(d.before)}</div></div>
    <div class="diff-col"><div class="diff-head diff-after">${esc(d.after.label)} <span class="diff-stat">+${st.added || 0}</span></div>
      <div class="diff-body scroll">${col(d.after)}</div></div>
  </div>`;
}

const VISUAL = {
  /* 1. 原始 Skill 文档（完整展示，可上下滚动） */
  skill_document(v) {
    const L = UI.visual.skill_document;
    const chips = v.sections.map((s) =>
      `<span class="chip nt-${s.type}">${esc(s.title)}</span>`).join("");
    const h = v.hero || {};
    const hero = `<div class="vbox" style="margin-bottom:14px">
      <h4>${fmt(L.hero_title, { name: esc(h.name || v.title) })}</h4>
      <div class="kv"><b>${L.what_it_does}</b>${esc(h.what_it_does || "")}</div>
      <div class="kv"><b>${L.why_this_skill}</b>${esc(h.why_this_skill || "")}</div></div>`;
    const comp = (v.composition || []).map((c) => `<li>${esc(c)}</li>`).join("");
    const others = (v.other_skills || []).map((c) => `<li>${esc(c)}</li>`).join("");
    return el(`<div>
      ${hero}
      <div class="cols2">
        <div class="vbox"><h4>${L.composition_title}</h4>
          <ul class="tight">${comp}</ul></div>
        <div class="vbox"><h4>${L.others_title}</h4>
          <ul class="tight">${others}</ul>
          <div class="bitlabel" style="margin-top:8px">${L.others_note}</div></div>
      </div>
      <div class="kv" style="margin-top:14px">${fmt(L.section_count, { count: v.section_count })}</div>
      <div class="chips" style="margin:10px 0">${chips}</div>
      <div class="bitlabel">${L.full_doc_label}</div>
      <pre class="scroll">${esc(v.markdown || "")}</pre>
    </div>`);
  },

  /* 2. SkillIR 结构节点图 */
  node_graph(v) {
    const L = UI.visual.node_graph;
    const nodes = v.nodes.map((n) =>
      `<span class="chip nt-${n.type}" title="${esc(n.text)}">${esc(n.label)}</span>`).join('<span style="color:var(--green);font-weight:800">→</span>');
    const anchors = (v.anchors || []).map((a) => `
      <div class="anchor-card">
        <div class="anchor-top"><span class="chip nt-${(a.type || "").replace(" ", "_")}">${esc(a.type)}</span>
          <span class="anchor-idx">${fmt(L.anchor_idx, { n: a.anchor })}</span></div>
        <div class="anchor-text">${esc(a.text)}</div>
        <div class="kv"><b>${L.meaning}</b>${esc(a.meaning)}</div>
        <div class="kv"><b>${L.reason}</b>${esc(a.reason)}</div>
      </div>`).join("");
    return el(`<div>
      <div class="kv">${L.intro}</div>
      <div class="chips" style="margin-top:12px;align-items:center">${nodes}</div>
      <div class="bitlabel" style="margin-top:12px">${L.node_types}</div>
      <div class="bitlabel" style="margin-top:16px">${L.anchors_label}</div>
      <div class="anchor-grid">${anchors}</div>
      ${v.explain ? explainBox(L.explain_title, v.explain) : ""}
    </div>`);
  },

  /* 3. 所有者水印（胶囊 schema） */
  capsule_schema(v) {
    const L = UI.visual.capsule_schema;
    const gate = (v.gate_rules || v.auxiliary_clauses || []).map((c, i) =>
      `<li><span class="rule-no">${i + 1}</span>${esc(c)}</li>`).join("");
    const fields = v.capsule_fields.map((f) =>
      `<tr><td><code>${esc(f.field)}</code></td><td>${esc(f.meaning)}</td></tr>`).join("");
    return el(`<div>
      <div class="cols2">
        <div class="vbox">
          <h4>${L.gate_title}</h4>
          <ul class="rule-list scroll" style="max-height:300px;overflow:auto">${gate}</ul>
        </div>
        <div class="vbox">
          <h4>${L.capsule_title}</h4>
          <table class="mtable"><tbody>${fields}</tbody></table>
          <div class="bitlabel" style="margin-top:8px">${esc(v.owner_labels_note)}</div>
          <details style="margin-top:10px" open><summary class="muted" style="cursor:pointer;font-size:12px">${L.example_summary}</summary>
            <pre class="scroll" style="margin-top:8px">${esc(v.example_capsule || "")}</pre></details>
        </div>
      </div>
      ${v.field_meanings ? `<div class="vbox" style="margin-top:14px"><h4>${L.field_meanings_title}</h4>${kvTable(v.field_meanings)}</div>` : ""}
      ${v.explain ? explainBox(L.explain_title, v.explain) : ""}
      <div class="bitlabel" style="margin-top:16px">${L.diff_label}</div>
      ${renderDiff(v.owner_diff)}
    </div>`);
  },

  /* 4. 买家指纹 bit 网格 */
  bit_grid(v) {
    const L = UI.visual.bit_grid;
    const cmp = v.compare_with;
    const diff = new Set(cmp.diff_positions);
    const grid = bitsGrid(v.fingerprint_bits, { diff });
    const gridB = bitsGrid(cmp.bits_b, { diff });
    const tt = (v.token_table || []).map((r) => `
      <tr><td>${r.anchor_idx}</td>
        <td><code>${esc(r.buyer_1_token)}</code></td><td class="ours">${r.buyer_1_bit}</td>
        <td><code>${esc(r.buyer_2_token)}</code></td><td class="ours">${r.buyer_2_bit}</td></tr>`).join("");
    return el(`<div>
      <div class="kv">${fmt(L.intro, { buyer_id: esc(v.buyer_id), codeword_length: v.codeword_length, bit_rule: esc(v.bit_rule) })}</div>
      <div class="bitlabel" style="margin-top:10px">${fmt(L.codeword_label, { buyer_id: esc(v.buyer_id) })}</div>${grid.outerHTML}
      <div class="bitlabel" style="margin-top:12px">${fmt(L.compare_label, { buyer_b: esc(cmp.buyer_b) })}</div>${gridB.outerHTML}
      <div class="kv" style="margin-top:10px">${fmt(L.distance, { hamming: cmp.hamming_distance, d_min: cmp.d_min, note: esc(cmp.note) })}</div>
      <div class="vbox" style="margin-top:14px"><h4>${L.token_table_title}</h4>
        <table class="mtable"><thead><tr><th>${L.th_anchor}</th><th>${L.th_b1_token}</th><th>${L.th_bit}</th><th>${L.th_b2_token}</th><th>${L.th_bit}</th></tr></thead>
        <tbody>${tt}</tbody></table>
        <div class="bitlabel" style="margin-top:6px">${L.rule_note}</div></div>
      ${v.explain ? explainBox(L.explain_title, v.explain) : ""}
      <div class="bitlabel" style="margin-top:16px">${fmt(L.diff_label, { buyer_id: esc(v.buyer_id) })}</div>
      ${renderDiff(v.buyer_diff)}
    </div>`);
  },

  /* 5. 攻击对比 */
  attack_diff(v) {
    const L = UI.visual.attack_diff;
    const hit = new Set(v.affected_positions);
    const t = bitsGrid(v.true_bits, {});
    const o = bitsGrid(v.observed_bits, { hit });
    let fid = "";
    if (v.fidelity_sample && v.fidelity_sample.buyer_example) {
      const out = v.fidelity_sample.buyer_example.output || "";
      fid = `<div class="vbox" style="margin-top:14px"><h4>${L.fidelity_title}</h4>
        <pre class="scroll">${esc(out)}</pre>
        <div class="bitlabel" style="margin-top:6px">${esc(v.fidelity_sample.note)}</div></div>`;
    }
    const cc = v.case_card || {};
    const card = `<div class="vbox" style="margin-bottom:12px"><h4>${L.case_card_title}</h4>
      <div class="kv">${fmt(L.case_card_line, { skill: esc(cc.skill), leaker: esc(cc.ground_truth_leaker), attack: esc(cc.attack) })}</div></div>`;
    const diffBlock = v.skill_diff
      ? `<div class="bitlabel" style="margin-top:16px">${L.diff_label}</div>
         ${renderDiff(v.skill_diff)}
         <div class="bitlabel" style="margin-top:6px">${L.diff_note}</div>`
      : `<div class="explain-box"><b>${L.no_attack_title}</b><p>${L.no_attack_body}</p></div>`;
    return el(`<div>
      ${card}
      ${v.attack_explanation ? explainBox(esc(v.name), v.attack_explanation) : ""}
      ${diffBlock}
      <div class="bitlabel" style="margin-top:16px">${fmt(L.impact_label, { src_tag: srcTag(v.data_source) })}</div>
      <div class="bitlabel">${L.before_label}</div>${t.outerHTML}
      <div class="bitlabel" style="margin-top:10px">${L.after_label}</div>${o.outerHTML}
      <div class="kv" style="margin-top:10px;color:var(--amber)">${L.constraint_prefix}${esc(v.constraint_note)}</div>
      ${fid}
    </div>`);
  },

  /* 6. 正/负探针对照 */
  probe_pair(v) {
    const L = UI.visual.probe_pair;
    const cap = v.positive_example.capsule_output || "";
    const neg = v.negative_example.capsule_output || "";
    const modelPart = v.model ? fmt(L.model_part, { model: esc(v.model), agent: esc(v.agent) }) : "";
    return el(`<div>
      <div class="kv">${fmt(L.intro, { positive_count: v.positive_count, negative_count: v.negative_count, src_tag: srcTag(v.data_source), model_part: modelPart })}</div>
      <div class="cols2" style="margin-top:12px">
        <div class="vbox" style="border-color:var(--green)">
          <h4>${L.positive_title}</h4>
          <div class="bitlabel">${L.question_label}</div><pre class="scroll">${esc(v.positive_example.query || "")}</pre>
          <div class="bitlabel" style="margin-top:8px">${L.positive_answer_label}</div><pre class="scroll">${esc(cap)}</pre>
        </div>
        <div class="vbox" style="border-color:var(--red)">
          <h4>${L.negative_title}</h4>
          <div class="bitlabel">${L.question_label}</div><pre class="scroll">${esc(v.negative_example.query || "")}</pre>
          <div class="bitlabel" style="margin-top:8px">${L.negative_answer_label}</div><pre class="scroll">${esc(neg || L.negative_empty)}</pre>
        </div>
      </div>
      <div class="kv" style="margin-top:10px;color:var(--green)">${L.diff_prefix}${esc(v.differential_note)}</div>
      ${v.token_focus ? `<div class="vbox" style="margin-top:14px"><h4>${L.token_focus_title}</h4>
        <div class="kv">${fmt(L.token_focus_line, { token: esc(v.token_focus.token), bit: esc(v.token_focus.bit), where_to_find: esc(v.token_focus.where_to_find) })}</div>
        <div class="bitlabel" style="margin-top:4px">${esc(v.token_focus.note)}</div></div>` : ""}
    </div>`);
  },

  /* 7. 所有权评分条 */
  score_bar(v) {
    const L = UI.visual.score_bar;
    const verified = v.ownership === "verified";
    const thr = (v.threshold * 100).toFixed(0) + "%";
    const off = v.official
      ? `<div class="official">${fmt(L.official, { true_ws: num(v.official.true_ws), false_ws: num(v.official.false_ws), margin: num(v.official.margin), accuracy: pct(v.official.accuracy) })}</div>`
      : "";
    return el(`<div>
      <div class="kv">${fmt(L.formula, { formula: esc(v.formula), src_tag: srcTag(v.data_source) })}</div>
      <div class="bitlabel" style="margin-top:14px">${fmt(L.true_ws_label, { value: num(v.true_ws) })}</div>
      <div class="scorebar"><div class="fill fill-true" style="width:${v.true_ws * 100}%">${pct(v.true_ws)}</div>
        <div class="threshold" style="left:${v.threshold * 100}%"></div></div>
      <div class="bitlabel" style="margin-top:12px">${fmt(L.false_ws_label, { value: num(v.false_ws) })}</div>
      <div class="scorebar"><div class="fill fill-false" style="width:${Math.max(v.false_ws * 100, 1.5)}%">${pct(v.false_ws)}</div>
        <div class="threshold" style="left:${v.threshold * 100}%"></div></div>
      <div class="thr-label" style="margin-top:6px">${fmt(L.threshold_label, { thr: thr })}</div>
      <div class="kv" style="margin-top:12px;font-size:16px">
        ${fmt(L.summary_line, { margin: num(v.margin), score_own: num(v.score_own) })}
        <b class="${verified ? "ok" : "bad"}">${verified ? L.verified : L.not_verified}</b>
      </div>${off}
      ${v.explain_score ? explainBox(L.explain_score_title, v.explain_score) : ""}
      ${v.explain_why ? explainBox(L.explain_why_title, v.explain_why) : ""}
      ${v.verdict ? `<div class="verdict-line">${L.verdict_prefix}${esc(v.verdict)}</div>` : ""}
    </div>`);
  },

  /* 8. 买家解码排名 */
  decode_grid(v) {
    const L = UI.visual.decode_grid;
    const rows = v.ranking.map((r) => `
      <tr class="${r.buyer_id === v.top1 ? "win" : ""}">
        <td>${esc(r.buyer_id)} ${r.buyer_id === v.top1 ? `<span class="badge">${L.badge_hit}</span>` : ""}</td>
        <td>${r.errors}</td><td>${r.erasures}</td>
        <td>${"●".repeat(Math.min(r.errors, 16))}${r.errors === 0 ? L.exact_match : ""}</td>
      </tr>`).join("");
    const off = v.official
      ? `<div class="official">${fmt(L.official, { top1: pct(v.official.top1), top3: pct(v.official.top3), erasure_rate: pct(v.official.erasure_rate) })}</div>`
      : "";
    const eccOk = v.ecc_satisfied;
    const dt = (v.decode_table || []).map((r) => `
      <tr class="dec-${r.status}">
        <td>${r.anchor_idx}</td><td><code>${esc(r.token)}</code></td>
        <td>${esc(r.bit)}</td><td>${esc(r.expected_bit)}</td>
        <td>${r.status === "matched" ? L.status_matched : r.status === "error" ? L.status_error : L.status_erasure}</td></tr>`).join("");
    const decTable = dt
      ? `<div class="vbox" style="margin:6px 0 14px"><h4>${L.decode_table_title}</h4>
          <table class="mtable"><thead><tr><th>${L.th_anchor}</th><th>${L.th_obs_token}</th><th>${L.th_bit}</th><th>${L.th_expected}</th><th>${L.th_status}</th></tr></thead>
          <tbody>${dt}</tbody></table>
          <div class="bitlabel" style="margin-top:6px">${L.decode_table_note}</div></div>`
      : "";
    return el(`<div>
      ${decTable}
      <div class="bitlabel">${L.observed_label}</div>${bitsGrid(v.observed_bits, {}).outerHTML}
      <div class="kv" style="margin-top:12px">${L.rank_intro}</div>
      <table class="rank" style="margin-top:10px">
        <thead><tr><th>${L.th_buyer}</th><th>${L.th_errors}</th><th>${L.th_erasures}</th><th>${L.th_diff}</th></tr></thead>
        <tbody>${rows}</tbody></table>
      <div class="kv" style="margin-top:14px;font-size:16px">
        ${fmt(L.result_line, { attributed_buyer: esc(v.attributed_buyer), decode_margin: v.decode_margin ?? "—", confidence: pct(v.confidence) })}
      </div>
      <div class="kv">${fmt(L.ecc_line, { ecc_lhs: v.ecc_lhs, op: eccOk ? "<" : "≥", d_min: v.d_min })}
        <b class="${eccOk ? "ok" : "bad"}">${eccOk ? L.ecc_ok : L.ecc_bad}</b></div>
      ${off}
      ${v.verdict ? `<div class="verdict-line">${L.verdict_prefix}${esc(v.verdict)}</div>` : ""}
    </div>`);
  },
};

/* bit 网格 helper：bits 字符串(含 0/1/⊥)，opts.diff / opts.hit 为需高亮的位集合 */
function bitsGrid(bits, opts) {
  const wrap = document.createElement("div");
  wrap.className = "bits";
  [...String(bits)].forEach((ch, i) => {
    const cls = ch === "1" ? "bit-1" : ch === "0" ? "bit-0" : "bit-x";
    const hi = opts.diff && opts.diff.has(i) ? " diff" : opts.hit && opts.hit.has(i) ? " hit" : "";
    const cell = document.createElement("div");
    cell.className = "bit " + cls + hi;
    cell.textContent = ch;
    cell.title = fmt(UI.bit_tooltip, { i });
    wrap.appendChild(cell);
  });
  return wrap;
}

/* ===================== ④ 裁决卡 ===================== */
function renderVerdict() {
  const s = CURRENT.summary, p = CURRENT.provenance;
  const L = UI.verdict;
  $("#verdict-empty").classList.add("hidden");
  const box = $("#verdict");
  box.classList.remove("hidden");
  const okOwn = s.ownership === "verified";
  const okBuy = s.attribution_correct;
  box.innerHTML = `
    <div class="vcard big">
      <h3>${fmt(L.title, { title: esc(CURRENT.title) })}</h3>
      <div class="cols2">
        <div>
          <div class="kv">${L.ownership_label}</div>
          <div class="verdict-stat ${okOwn ? "ok" : "bad"}">${okOwn ? L.ownership_ok : L.ownership_bad}</div>
          <div class="kv">${fmt(L.ownership_stats, { true_ws: num(s.true_ws), false_ws: num(s.false_ws), margin: num(s.margin) })}</div>
        </div>
        <div>
          <div class="kv">${L.attribution_label}</div>
          <div class="verdict-stat ${okBuy ? "ok" : "bad"}">${fmt(L.attribution_value, { attributed_buyer: esc(s.attributed_buyer) })}</div>
          <div class="kv">${fmt(L.attribution_stats, { confidence: pct(s.confidence), errors: s.errors, erasures: s.erasures, decode_margin: s.decode_margin ?? "—" })}</div>
        </div>
      </div>
    </div>
    <div class="vcard"><h3>${L.attack_title}</h3><div class="verdict-stat" style="font-size:20px">${esc(CURRENT.attack.name)}</div>
      <div class="kv">${esc(CURRENT.attack.description || "")}</div></div>
    <div class="vcard"><h3>${L.ecc_title}</h3>
      <div class="verdict-stat ${s.ecc_satisfied ? "ok" : "bad"}" style="font-size:20px">${s.ecc_satisfied ? L.ecc_ok : L.ecc_bad}</div>
      <div class="kv">${L.ecc_note}</div></div>
    <div class="vcard"><h3>${L.source_title}</h3>
      <div class="verdict-stat" style="font-size:18px">${p.data_source === "real" ? L.source_real : L.source_sim}</div>
      <div class="kv">${esc(p.model || "")} ${p.agent ? "+ " + esc(p.agent) : ""}</div></div>`;
}

/* ===================== ⑤ 指标总览 ===================== */
function renderMetrics(m) {
  const box = $("#metrics");
  box.innerHTML = "";
  const pa = m.overall;

  // 整体汇总：所有权 / 买家 / 鲁棒性 / 保真
  box.appendChild(compareBlock(pa.owner_verification));
  box.appendChild(compareBlock(pa.buyer_attribution));
  box.appendChild(robustBlock(pa.robustness));
  box.appendChild(compareBlock(pa.fidelity));

  // 消融
  const M = UI.metrics;
  const ab = pa.ablation;
  const rows = ab.items.map((i) => `<tr><td><code>${esc(i.remove)}</code></td><td>${esc(i.effect)}</td></tr>`).join("");
  box.appendChild(el(`<div class="mblock"><h3>${esc(ab.title)}</h3><p class="take">${esc(ab.takeaway)}</p>
    <table class="mtable"><thead><tr><th>${M.ablation_headers[0]}</th><th>${M.ablation_headers[1]}</th></tr></thead><tbody>${rows}</tbody></table></div>`));

  // 本次真实运行官方指标
  if (m.run_official) {
    const ro = m.run_official;
    const eff = (ro.effectiveness_distinctiveness || []).filter((r) => r.domain !== "__avg__");
    const effRows = eff.map((r) =>
      `<tr><td>${esc(r.domain)}</td><td class="ours">${num(r.true_ws)}</td><td>${num(r.false_ws)}</td><td class="ours">${num(r.margin)}</td><td>${pct(r.accuracy)}</td></tr>`).join("");
    const H = M.run_official_headers;
    box.appendChild(el(`<div class="mblock" style="border-color:var(--green)">
      <h3>${fmt(M.run_official_title, { model: esc(ro.model), agent: esc(ro.agent) })}</h3>
      <p class="take">${esc(ro.note)}</p>
      <table class="mtable"><thead><tr><th>${H[0]}</th><th>${H[1]}</th><th>${H[2]}</th><th>${H[3]}</th><th>${H[4]}</th></tr></thead>
      <tbody>${effRows}</tbody></table></div>`));
  }
}

// 我们 vs 基线 对比表
function compareBlock(b) {
  const H = UI.metrics.compare_headers;
  const rows = b.metrics.map((mt) => {
    const better = mt.higher_is_better !== false;
    const w = Math.min((mt.ours ?? 0) * 100, 100);
    return `<tr>
      <td>${esc(mt.name)}</td>
      <td class="ours">${num(mt.ours)}</td>
      <td>${mt.promptcare != null ? num(mt.promptcare) : "—"}</td>
      <td>${mt.promptcos != null ? num(mt.promptcos) : "—"}</td>
      <td><div class="metricbar"><i style="width:${w}%;background:${better ? "var(--green)" : "var(--red)"}"></i></div></td>
    </tr>`;
  }).join("");
  return el(`<div class="mblock"><h3>${esc(b.title)}</h3><p class="take">${esc(b.takeaway)}</p>
    <table class="mtable"><thead><tr><th>${H[0]}</th><th>${H[1]}</th><th>${H[2]}</th><th>${H[3]}</th><th>${H[4]}</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`);
}

// 鲁棒性表
function robustBlock(b) {
  const H = UI.metrics.robust_headers;
  const rows = b.metrics.map((mt) =>
    `<tr><td>${esc(mt.name)}</td><td class="ours">${pct(mt.buyer_top1)}</td><td class="ours">${pct(mt.owner_acc)}</td></tr>`).join("");
  return el(`<div class="mblock"><h3>${esc(b.title)}</h3><p class="take">${esc(b.takeaway)}</p>
    <table class="mtable"><thead><tr><th>${H[0]}</th><th>${H[1]}</th><th>${H[2]}</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`);
}
