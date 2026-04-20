const state = {
  bridgeUrl: "",
  userId: "",
};

const els = {
  bridgeUrl: document.getElementById("bridgeUrl"),
  userId: document.getElementById("userId"),
  saveBtn: document.getElementById("saveBtn"),
  pingBtn: document.getElementById("pingBtn"),
  chatForm: document.getElementById("chatForm"),
  sendBtn: document.getElementById("sendBtn"),
  messageInput: document.getElementById("messageInput"),
  messages: document.getElementById("messages"),
  status: document.getElementById("status"),
  sessionLabel: document.getElementById("sessionLabel"),
  chips: Array.from(document.querySelectorAll(".chip")),
};

function randomId(prefix) {
  const n = Math.random().toString(36).slice(2, 10);
  return `${prefix}-${n}`;
}

function normalizeUrl(url) {
  return (url || "").trim().replace(/\/$/, "");
}

function setStatus(kind, text) {
  els.status.className = `status ${kind}`;
  els.status.textContent = text;
}

function appendMessage(type, text) {
  const node = document.createElement("div");
  node.className = `msg ${type}`;
  node.textContent = text;
  els.messages.appendChild(node);
  scrollMessagesToBottom();
}

function showTypingIndicator() {
  let node = document.getElementById("typingIndicator");
  if (node) return;

  node = document.createElement("div");
  node.id = "typingIndicator";
  node.className = "msg bot typing";
  node.setAttribute("aria-live", "polite");
  node.setAttribute("aria-label", "Agent is typing");
  node.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';

  els.messages.appendChild(node);
  scrollMessagesToBottom();
}

function hideTypingIndicator() {
  const node = document.getElementById("typingIndicator");
  if (node) {
    node.remove();
  }
}

function scrollMessagesToBottom(behavior = "smooth") {
  requestAnimationFrame(() => {
    els.messages.scrollTo({
      top: els.messages.scrollHeight,
      behavior,
    });
  });
}

async function callAgent(message) {
  const payload = {
    message,
    user_id: state.userId,
    userId: state.userId,
  };

  const chatUrl = `${state.bridgeUrl}/chat`;
  const response = await fetch(chatUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const txt = await response.text();
    throw new Error(`HTTP ${response.status}: ${txt}`);
  }

  const data = await response.json();
  if (data.user_id) {
    state.userId = data.user_id;
  }
  return data.reply || "L'agent n'a renvoye aucun texte.";
}

function persistConfig() {
  const saved = {
    bridgeUrl: state.bridgeUrl,
    userId: state.userId,
  };
  localStorage.setItem("matos-playground-config", JSON.stringify(saved));
}

function loadConfig() {
  try {
    const raw = localStorage.getItem("matos-playground-config");
    if (!raw) return;
    const saved = JSON.parse(raw);
    if (saved.bridgeUrl) state.bridgeUrl = saved.bridgeUrl;
    if (saved.userId) state.userId = saved.userId;
  } catch {
    // ignore
  }
}

function syncInputs() {
  els.bridgeUrl.value = state.bridgeUrl;
  els.userId.value = state.userId;
  els.sessionLabel.textContent = `session: ${state.userId || "-"}`;
}

function validateConfig() {
  if (!state.bridgeUrl.startsWith("http")) {
    throw new Error("Bridge URL invalide. Exemple: https://matos-bridge-xxx.run.app");
  }
  if (!state.userId) {
    throw new Error("User ID est requis.");
  }
}

function readConfigFromInputs() {
  state.bridgeUrl = normalizeUrl(els.bridgeUrl.value);
  state.userId = (els.userId.value || "").trim();
}

async function pingAgent() {
  readConfigFromInputs();
  validateConfig();

  els.pingBtn.disabled = true;
  setStatus("idle", "Test connexion en cours...");

  try {
    const health = await fetch(`${state.bridgeUrl}/health`);
    if (!health.ok) {
      throw new Error(`health HTTP ${health.status}`);
    }
    setStatus("ok", "Connexion bridge OK. Vous pouvez chatter.");
    appendMessage("system", "Connexion web-chat validee via le bridge.");
  } catch (err) {
    setStatus("err", `Connexion echouee: ${err.message}`);
  } finally {
    els.pingBtn.disabled = false;
  }
}

async function onSend(evt) {
  evt.preventDefault();

  const text = (els.messageInput.value || "").trim();
  if (!text) return;

  readConfigFromInputs();

  try {
    validateConfig();
  } catch (err) {
    setStatus("err", err.message);
    return;
  }

  appendMessage("user", text);
  els.messageInput.value = "";
  els.sendBtn.disabled = true;
  setStatus("idle", "L'agent reflechit...");
  showTypingIndicator();

  try {
    const reply = await callAgent(text);
    hideTypingIndicator();
    appendMessage("bot", reply);
    syncInputs();
    setStatus("ok", "Reponse recue.");
  } catch (err) {
    hideTypingIndicator();
    const msg = String(err.message || err);
    appendMessage("system", `Erreur: ${msg}`);
    if (msg.includes("Failed to fetch") || msg.includes("CORS")) {
      setStatus("err", "Echec reseau/CORS. Verifiez BRIDGE_URL et l'etat du service backend.");
    } else {
      setStatus("err", `Erreur bridge/agent: ${msg}`);
    }
  } finally {
    els.sendBtn.disabled = false;
  }
}

function onSave() {
  try {
    readConfigFromInputs();
    if (!state.userId) {
      state.userId = randomId("demo-user");
    }
    validateConfig();
    persistConfig();
    syncInputs();
    setStatus("ok", "Configuration sauvegardee.");
  } catch (err) {
    setStatus("err", err.message);
  }
}

function init() {
  loadConfig();
  if (!state.userId) {
    state.userId = randomId("demo-user");
  }
  syncInputs();

  appendMessage("system", "Bienvenue. Configurez BRIDGE_URL puis testez la connexion.");
  scrollMessagesToBottom("auto");

  els.saveBtn.addEventListener("click", onSave);
  els.pingBtn.addEventListener("click", () => {
    pingAgent().catch((err) => setStatus("err", String(err.message || err)));
  });
  els.chatForm.addEventListener("submit", onSend);

  els.chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      els.messageInput.value = chip.dataset.prompt || "";
      els.messageInput.focus();
    });
  });
}

init();
