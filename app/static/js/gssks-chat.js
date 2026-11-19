(() => {
  const launcher = document.getElementById("gssksChatLauncher");
  const panel = document.getElementById("gssksChatPanel");
  const closeButton = document.getElementById("gssksChatClose");
  const clearButton = document.getElementById("gssksChatClear");
  const form = document.getElementById("gssksChatForm");
  const input = document.getElementById("gssksChatInput");
  const messages = document.getElementById("gssksChatMessages");
  const suggestions = document.getElementById("gssksChatSuggestions");
  const quickMenu = document.getElementById("gssksChatTopics");
  if (!launcher || !panel || !form || !input || !messages || !suggestions) return;

  let busy = false;
  const welcome = "Namaste! Welcome to GSSKS. I'm here to help you learn about our organisation, child-protection work, Open Shelter Homes, services and how to connect with our team.";
  const quickQuestions = ["About GSSKS", "Open Shelter Home", "Services for children", "Contact details"];
  const topicQuestions = [
    ["Organisation", "Tell me about GSSKS"],
    ["Child protection", "What child protection support is available?"],
    ["Shelter locations", "Where are the Open Shelter Homes?"],
    ["Education", "What education support is provided?"],
    ["Health & wellbeing", "What health and counselling support is available?"],
    ["Get involved", "How can I volunteer or support GSSKS?"]
  ];

  function setOpen(open) {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", open ? "true" : "false");
    launcher.classList.toggle("is-open", open);
    if (open) window.setTimeout(() => input.focus(), 80);
    else launcher.focus();
  }

  function scrollMessages() { messages.scrollTop = messages.scrollHeight; }

  function addMessage(text, kind, options = {}) {
    const wrap = document.createElement("article");
    wrap.className = "gssks-chat-entry " + (kind === "user" ? "from-user" : "from-bot");
    const avatar = document.createElement("span");
    avatar.className = "gssks-chat-avatar";
    if (kind === "bot") {
      const logo = document.createElement("img");
      logo.src = launcher.querySelector("img").src;
      logo.alt = "";
      avatar.appendChild(logo);
    } else {
      avatar.textContent = "You";
    }
    const bubble = document.createElement("div");
    bubble.className = "gssks-chat-message " + (kind === "user" ? "is-user" : "is-bot");
    bubble.textContent = text;
    wrap.append(avatar, bubble);
    messages.appendChild(wrap);

    if (Array.isArray(options.links) && options.links.length) {
      const linkRow = document.createElement("div");
      linkRow.className = "gssks-chat-links";
      options.links.forEach((item) => {
        if (!item || typeof item.label !== "string" || typeof item.url !== "string") return;
        const url = new URL(item.url, window.location.origin);
        if (url.origin !== window.location.origin) return;
        const a = document.createElement("a");
        a.href = url.pathname;
        a.textContent = item.label;
        linkRow.appendChild(a);
      });
      if (linkRow.childElementCount) messages.appendChild(linkRow);
    }
    scrollMessages();
    return wrap;
  }

  function renderSuggestions(items) {
    suggestions.replaceChildren();
    (items || []).slice(0, 5).forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "gssks-chat-chip";
      button.textContent = item;
      button.addEventListener("click", () => ask(item));
      suggestions.appendChild(button);
    });
  }

  function renderTopics() {
    if (!quickMenu) return;
    quickMenu.replaceChildren();
    topicQuestions.forEach(([label, question]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "gssks-chat-topic";
      button.textContent = label;
      button.addEventListener("click", () => ask(question));
      quickMenu.appendChild(button);
    });
  }

  async function ask(raw) {
    const question = String(raw || "").trim();
    if (!question || busy) return;
    addMessage(question, "user");
    input.value = "";
    busy = true;
    form.classList.add("is-loading");
    const pending = addMessage("Checking GSSKS information…", "bot");
    pending.classList.add("is-pending");
    renderSuggestions([]);
    if (quickMenu) quickMenu.hidden = true;

    try {
      const response = await fetch("/api/chat?q=" + encodeURIComponent(question), {
        method: "GET",
        headers: { "Accept": "application/json" },
        credentials: "same-origin",
        cache: "no-store"
      });
      const data = await response.json();
      pending.remove();
      if (!response.ok) throw new Error(data.error || "Unable to answer right now.");
      addMessage(data.answer || "Please contact GSSKS for more information.", "bot", {links: data.links || []});
      renderSuggestions(data.suggestions || quickQuestions);
    } catch (_) {
      pending.remove();
      addMessage("I'm unable to connect at the moment. Please try again shortly, or contact GSSKS at 0755-4278487 or gyanpathngo.176@gmail.com.", "bot");
      renderSuggestions(["Contact details", "About GSSKS"]);
    } finally {
      busy = false;
      form.classList.remove("is-loading");
      input.focus();
    }
  }

  function resetChat() {
    if (busy) return;
    messages.replaceChildren();
    addMessage(welcome, "bot");
    renderSuggestions(quickQuestions);
    if (quickMenu) quickMenu.hidden = false;
    renderTopics();
    input.focus();
  }

  launcher.addEventListener("click", () => setOpen(panel.hidden));
  closeButton?.addEventListener("click", () => setOpen(false));
  clearButton?.addEventListener("click", resetChat);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    ask(input.value);
  });
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) setOpen(false);
  });

  addMessage(welcome, "bot");
  renderSuggestions(quickQuestions);
  renderTopics();
})();