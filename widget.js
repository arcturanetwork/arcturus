/*
 * Arcturus Operator Helpdesk Widget
 * Arctura Network — floating chat launcher, keyword-matched knowledge base.
 * Self-contained: injects its own styles and markup. No external dependencies.
 */
(function () {
  "use strict";

  var AVATAR_URL = "/assets/arcturus-avatar.jpg";

  var KB = [
    {
      id: "welcome",
      match: null,
      reply: "I'm Arcturus — Arctura Network's elite agentic AI operator. Ask me about the competency domains, the training lab, the operating stack, or how to reach a human."
    },
    {
      id: "what",
      match: /\b(what are you|what is arcturus|who are you|about arcturus)/i,
      reply: "Not a chatbot. An operator. Arcturus is Arctura Network's agentic AI operator, trained on the full NVIDIA NCP-AAI stack across all 10 certification domains — reasoning, tool use, memory, retrieval, deployment, safety, and human oversight."
    },
    {
      id: "domains",
      match: /\b(domains?|competenc\w*|10 domains?|ten domains?|blueprint\w*)\b/i,
      reply: "10 domains, full blueprint coverage:\n1. Reasoning Frameworks (15%)\n2. Agent Development & Tools (15%)\n3. Evaluation and Tuning (13%)\n4. Deployment and Scaling (13%)\n5. Cognition, Planning, Memory (10%)\n6. Knowledge Integration — Graphs & RAG (10%)\n7. NVIDIA Platform Implementation (7%)\n8. Run, Monitor, Maintain (5%)\n9. Safety, Ethics, Governance (5%)\n10. Human-AI Interaction (5%)\n\nSee the full breakdown below on this page."
    },
    {
      id: "react",
      match: /\b(react|reflexion|rewoo|reasoning framework\w*)\b/i,
      reply: "Three reasoning patterns: ReAct (Thought → Action → Observation loop, the default), Reflexion (verbal self-reflection stored in episodic memory across attempts), and ReWOO (plan all tool calls upfront — ~5× token efficiency over ReAct). Domain 1 covers all three in depth."
    },
    {
      id: "memory",
      match: /\b(memor\w*|episodic|semantic|context window)/i,
      reply: "Arcturus runs a memory stack, not a single context window: short-term (working), episodic (past interactions), semantic (general knowledge), and procedural (how-to sequences). Detailed in Domain 5."
    },
    {
      id: "rag",
      match: /\b(rag|retriev\w*|graphrag|knowledge graph\w*|vector)\w*/i,
      reply: "Vector RAG handles local factual lookups. Knowledge graphs handle multi-hop reasoning. GraphRAG pre-computes community summaries for global, thematic questions. All three are evaluated against the RAG triad: context relevance, groundedness, answer relevance. Domain 6."
    },
    {
      id: "nvidia",
      match: /\b(nvidia|nim|nemo|guardrail\w*|tensorrt|colang)\w*/i,
      reply: "The platform layer: NeMo Agent Toolkit for orchestration, NIM microservices (TensorRT-LLM optimized) for inference, and NeMo Guardrails (Colang 2.0) for input/output safety rails. Domain 7."
    },
    {
      id: "deploy",
      match: /\b(deploy\w*|scal\w*|production|architecture|kubernetes|k8s)/i,
      reply: "Stateless orchestrator pattern: API Gateway → Orchestrator → NIM / Tool Services / Memory Store → Guardrails. Horizontally scalable, restartable, state lives externally. Domain 4 — and the full k8s manifests live in the training lab."
    },
    {
      id: "safety",
      match: /\b(safety|ethic\w*|governance|five checks|bias)/i,
      reply: "Every action passes the Five Checks: Need, Clarity, Usefulness, Durability, Reversal — inherited from Arctura Network's Work Standard. Three-layer guardrail stack screens input, dialog, and output. Domain 9."
    },
    {
      id: "human",
      match: /\b(human\w*|oversight|handoff|escalat\w*|approval\w*)/i,
      reply: "Arcturus knows when it doesn't know. Uncertain results, disputed evaluations, or exceptions to the Five Checks escalate to a human reviewer with full context — reasoning trace and all. Domain 10."
    },
    {
      id: "lab",
      match: /\b(lab\w*|training|certif\w*|ncp-aai|study|studies|curriculum|capstone)/i,
      reply: "The training lab is public — six certification tracks (NCP-AAI primary, AWS SAP, CKA, NCP-GENL, CCSP, Google PMLE), a working capstone agent with typed tools and bounded orchestration, and a 50-case policy evaluation suite. Browse it in the repo linked at the bottom of this page."
    },
    {
      id: "contact",
      match: /\b(contact\w*|talk to|human overseer|reach|email|support|help me|real person)/i,
      reply: "For anything beyond this page's scope, escalations route to the Arctura Network overseer. Open an issue on the GitHub repo (linked in the footer) and it will be routed to a person."
    },
    {
      id: "price",
      match: /\b(price\w*|cost\w*|hire|buy|leads?|pricing|quote\w*)/i,
      reply: "Arcturus doesn't handle commercial transactions directly through this widget. For lead qualification or business inquiries, use the intake channels listed on the Arctura Network site."
    },
    {
      id: "source",
      match: /\b(sources?|evidence|prove|trust\w*|verify|check)/i,
      reply: "Nothing here asks to be trusted on its word. Full technical reference, work standard, and authority record are all linked at the bottom of this page — check it yourself."
    }
  ];

  var FALLBACK = "That's outside what I can answer directly. Try asking about the competency domains, reasoning frameworks, the training lab, or how to reach a human — or check the full technical reference linked below.";

  function matchReply(text) {
    for (var i = 1; i < KB.length; i++) {
      if (KB[i].match && KB[i].match.test(text)) return KB[i].reply;
    }
    return FALLBACK;
  }

  var css = "\n" +
    "#arc-hd-launcher{position:fixed;bottom:1.5rem;right:1.5rem;width:60px;height:60px;border-radius:50%;border:2px solid #3ea89b;background:#0a0c0d;cursor:pointer;z-index:99998;box-shadow:0 4px 24px rgba(0,0,0,0.5);overflow:hidden;padding:0;transition:transform .2s,border-color .2s;}\n" +
    "#arc-hd-launcher:hover{transform:scale(1.06);border-color:#c9a35c;}\n" +
    "#arc-hd-launcher img{width:100%;height:100%;object-fit:cover;display:block;}\n" +
    "#arc-hd-dot{position:absolute;bottom:2px;right:2px;width:12px;height:12px;border-radius:50%;background:#3ea89b;border:2px solid #0a0c0d;}\n" +
    "#arc-hd-panel{position:fixed;bottom:6rem;right:1.5rem;width:min(360px,90vw);max-height:min(560px,75vh);background:#111416;border:1px solid rgba(233,230,223,0.14);border-radius:8px;box-shadow:0 12px 48px rgba(0,0,0,0.6);display:none;flex-direction:column;z-index:99999;font-family:'Azeret Mono',monospace;overflow:hidden;}\n" +
    "#arc-hd-panel.open{display:flex;}\n" +
    "#arc-hd-head{display:flex;align-items:center;gap:.6rem;padding:.9rem 1rem;border-bottom:1px solid rgba(233,230,223,0.10);background:#0a0c0d;}\n" +
    "#arc-hd-head img{width:32px;height:32px;border-radius:50%;object-fit:cover;border:1px solid #3ea89b;}\n" +
    "#arc-hd-head .t1{color:#e9e6df;font-family:'Syne',sans-serif;font-weight:700;font-size:.85rem;}\n" +
    "#arc-hd-head .t2{color:#3ea89b;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;}\n" +
    "#arc-hd-close{margin-left:auto;background:none;border:none;color:#a8a6a0;font-size:1.1rem;cursor:pointer;line-height:1;padding:.25rem;}\n" +
    "#arc-hd-close:hover{color:#c9a35c;}\n" +
    "#arc-hd-body{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.65rem;background:#0a0c0d;}\n" +
    "#arc-hd-body::-webkit-scrollbar{width:6px;}#arc-hd-body::-webkit-scrollbar-thumb{background:rgba(233,230,223,0.15);border-radius:3px;}\n" +
    ".arc-hd-msg{max-width:85%;padding:.6rem .75rem;border-radius:6px;font-size:.82rem;line-height:1.5;white-space:pre-wrap;}\n" +
    ".arc-hd-msg.bot{align-self:flex-start;background:#16181a;color:#e9e6df;border:1px solid rgba(233,230,223,0.10);}\n" +
    ".arc-hd-msg.user{align-self:flex-end;background:rgba(62,168,155,0.12);color:#e9e6df;border:1px solid rgba(62,168,155,0.35);}\n" +
    "#arc-hd-quick{display:flex;flex-wrap:wrap;gap:.4rem;padding:.75rem 1rem;border-top:1px solid rgba(233,230,223,0.08);background:#0a0c0d;}\n" +
    ".arc-hd-chip{font-family:'Azeret Mono',monospace;font-size:.7rem;color:#a8a6a0;background:#16181a;border:1px solid rgba(233,230,223,0.15);border-radius:12px;padding:.3rem .65rem;cursor:pointer;transition:.15s;}\n" +
    ".arc-hd-chip:hover{color:#c9a35c;border-color:#c9a35c;}\n" +
    "#arc-hd-inputrow{display:flex;gap:.5rem;padding:.75rem;border-top:1px solid rgba(233,230,223,0.10);background:#111416;}\n" +
    "#arc-hd-input{flex:1;background:#0a0c0d;border:1px solid rgba(233,230,223,0.15);border-radius:5px;color:#e9e6df;font-family:'Azeret Mono',monospace;font-size:.82rem;padding:.55rem .7rem;outline:none;}\n" +
    "#arc-hd-input:focus{border-color:#3ea89b;}\n" +
    "#arc-hd-send{background:none;border:1px solid #3ea89b;color:#3ea89b;border-radius:5px;padding:.55rem .9rem;font-family:'Azeret Mono',monospace;font-size:.78rem;cursor:pointer;transition:.15s;}\n" +
    "#arc-hd-send:hover{background:#3ea89b;color:#0a0c0d;}\n" +
    "@media (max-width:480px){#arc-hd-panel{right:.75rem;bottom:5.25rem;width:calc(100vw - 1.5rem);}#arc-hd-launcher{right:.9rem;bottom:.9rem;}}\n";

  function inject() {
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var launcher = document.createElement("button");
    launcher.id = "arc-hd-launcher";
    launcher.setAttribute("aria-label", "Open Arcturus helpdesk");
    launcher.innerHTML = '<img src="' + AVATAR_URL + '" alt="Arcturus"><span id="arc-hd-dot"></span>';
    document.body.appendChild(launcher);

    var panel = document.createElement("div");
    panel.id = "arc-hd-panel";
    panel.innerHTML =
      '<div id="arc-hd-head">' +
        '<img src="' + AVATAR_URL + '" alt="Arcturus">' +
        '<div><div class="t1">Arcturus</div><div class="t2">Operator Helpdesk · Active</div></div>' +
        '<button id="arc-hd-close" aria-label="Close">&times;</button>' +
      '</div>' +
      '<div id="arc-hd-body"></div>' +
      '<div id="arc-hd-quick">' +
        '<span class="arc-hd-chip" data-q="What is Arcturus?">What is Arcturus?</span>' +
        '<span class="arc-hd-chip" data-q="Competency domains">Domains</span>' +
        '<span class="arc-hd-chip" data-q="Training lab">Training lab</span>' +
        '<span class="arc-hd-chip" data-q="Talk to a human">Talk to a human</span>' +
      '</div>' +
      '<div id="arc-hd-inputrow">' +
        '<input id="arc-hd-input" type="text" placeholder="Ask Arcturus..." autocomplete="off">' +
        '<button id="arc-hd-send">Send</button>' +
      '</div>';
    document.body.appendChild(panel);

    var body = panel.querySelector("#arc-hd-body");
    var input = panel.querySelector("#arc-hd-input");

    function addMsg(text, who) {
      var div = document.createElement("div");
      div.className = "arc-hd-msg " + who;
      div.textContent = text;
      body.appendChild(div);
      body.scrollTop = body.scrollHeight;
    }

    function ask(text) {
      if (!text.trim()) return;
      addMsg(text, "user");
      input.value = "";
      setTimeout(function () {
        addMsg(matchReply(text), "bot");
      }, 260);
    }

    launcher.addEventListener("click", function () {
      panel.classList.toggle("open");
      if (panel.classList.contains("open") && body.children.length === 0) {
        addMsg(KB[0].reply, "bot");
      }
    });
    panel.querySelector("#arc-hd-close").addEventListener("click", function () {
      panel.classList.remove("open");
    });
    panel.querySelector("#arc-hd-send").addEventListener("click", function () {
      ask(input.value);
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") ask(input.value);
    });
    panel.querySelectorAll(".arc-hd-chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        ask(chip.getAttribute("data-q"));
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
