import { $$ } from "/static/debug_toolbar/js/utils.js";

const djDebugRoot = document.getElementById("djDebug");
let cachedContextId = null;

async function fetchDjdtPanelContents(panelIds = []) {
  const storeId = djDebugRoot.dataset.storeId;
  if (!storeId) throw new Error("storeId not found");

  const results = {};
  for (const panelId of panelIds) {
    const url = `/__debug__/render_panel/?store_id=${storeId}&panel_id=${panelId}`;
    try {
      const response = await fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      results[panelId] = response.ok ? await response.text() : `Error: ${response.status}`;
    } catch (e) {
      results[panelId] = `Fetch failed: ${e}`;
    }
  }
  return results;
}

async function uploadContext(contextData) {
  const response = await fetch("/__debug__/upload-context/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ context: contextData }),
  });
  const data = await response.json();
  return data.context_id;
}

async function chatWithAssistant(contextId, messages, model) {
  const response = await fetch("/__debug__/llm-chat/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ context_id: contextId, messages, model }),
  });
  const data = await response.json();
  return data.response;
}

function scrollToBottom() {
  const responseEl = document.getElementById("ai-response");
  responseEl.scrollTop = responseEl.scrollHeight;
}

function renderQueryAssistantPanel() {
  const panel = document.getElementById("AssistantPanel");
  if (!panel) return;

  const askButton = panel.querySelector("#ask-ai");
  const modelSelect = panel.querySelector("#model-select");
  const textarea = panel.querySelector("#ai-question");
  const responseEl = panel.querySelector("#ai-response");
  const suggestionButtons = panel.querySelectorAll(".ai-suggestion");

  suggestionButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      textarea.value = btn.textContent;
      askButton.click();
    });
  });

  askButton?.addEventListener("click", async () => {
    const userMessage = textarea.value.trim();
    if (!userMessage) return;

    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.textContent = userMessage;
    responseEl.appendChild(userDiv);
    scrollToBottom();

    textarea.value = "";

    const spinnerDiv = document.createElement("div");
    spinnerDiv.className = "assistant-msg";
    spinnerDiv.innerHTML = `<div class="ai-loading-spinner"></div>`;
    responseEl.appendChild(spinnerDiv);
    scrollToBottom();

    if (!cachedContextId) {
      const contextHTML = Object.values(await fetchDjdtPanelContents([
        "HistoryPanel", "VersionsPanel", "TimerPanel", "SettingsPanel",
        "HeadersPanel", "RequestPanel", "SQLPanel", "StaticFilesPanel",
        "TemplatesPanel", "AlertsPanel", "CachePanel", "RedirectsPanel", "ProfilingPanel"
      ])).join("\n");

      cachedContextId = await uploadContext(contextHTML);
    }

    const selectedModel = modelSelect?.value || "gemini-1.5-flash";
    const reply = await chatWithAssistant(cachedContextId, [
      { role: "user", content: userMessage }
    ], selectedModel);

    spinnerDiv.innerHTML = reply;
    scrollToBottom();
  });
}

$$.onPanelRender(djDebugRoot, "AssistantPanel", renderQueryAssistantPanel);
renderQueryAssistantPanel();