(() => {
  const launcher = document.getElementById("gssksChatLauncher");
  const panel = document.getElementById("gssksChatPanel");
  const closeButton = document.getElementById("gssksChatClose");
  const form = document.getElementById("gssksChatForm");
  const input = document.getElementById("gssksChatInput");
  const messages = document.getElementById("gssksChatMessages");
  const suggestions = document.getElementById("gssksChatSuggestions");
  if (!launcher || !panel || !form || !input || !messages) return;

  let busy = false;
  const quickQuestions = ["About GSSKS", "Open Shelter Home", "Services for children", "Contact details"];

  function setOpen(open) {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) window.setTimeout(() => input.focus(), 80);
    else launcher.focus();
  }

  function addMessage(text, kind) {
    const bubble = document.createElement("div");
    bubble.className = "gssks-chat-message " + (kind === "user" ? "is-user" : "is-bot");
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  }

  function renderSuggestions(items) {
    suggestions.replaceChildren();
    (items || []).forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "gssks-chat-chip";
      button.textContent = item;
      button.addEventListener("click", () => ask(item));
      suggestions.appendChild(button);
    });
  }

  async function ask(raw) {
    const question = String(raw || "").trim();
    if (!question || busy) return;
    addMessage(question, "user");
    input.value = "";
    busy = true;
    form.classList.add("is-loading");
    const pending = addMessage("One moment…", "bot");
    pending.classList.add("is-pending");
    renderSuggestions([]);

    try {
      const response = await fetch("/api/chat?q=" + encodeURIComponent(question), {
        method: "GET",
        headers: { "Accept": "application/json" },
        credentials: "same-origin"
      });
      const data = await response.json();
      pending.remove();
      if (!response.ok) throw new Error(data.error || "Unable to answer right now.");
      addMessage(data.answer || "Please contact GSSKS for more information.", "bot");
      renderSuggestions(data.suggestions || quickQuestions);
    } catch (error) {
      pending.remove();
      addMessage("I'm having trouble connecting right now. Please try again, or contact GSSKS at 0755-4278487 or gyanpathngo.176@gmail.com.", "bot");
      renderSuggestions(["Contact details", "About GSSKS"]);
    } finally {
      busy = false;
      form.classList.remove("is-loading");
      input.focus();
    }
  }

  launcher.addEventListener("click", () => setOpen(panel.hidden));
  closeButton.addEventListener("click", () => setOpen(false));
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

  addMessage("Hello! I'm the GSSKS assistant. Ask me about the organisation, our child-protection work, Open Shelter Homes, services, locations or how to get in touch.", "bot");
  renderSuggestions(quickQuestions);
})();