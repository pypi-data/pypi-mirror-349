TRANSCRIPT:

{transcribed_text}

Date & Time of Meeting: {meeting_datetime}

Your task is to analyze the above meeting transcript and extract structured, visually rich insights using careful reasoning. You must **infer names, products, decisions, and other contextual clues logically**, even when they are not explicitly stated.

---

## 🧠 Primary Goals:
1. **Accurate Participant Identification**  
- Extract all participants mentioned or inferred.
- Use chain-of-thought reasoning to resolve references like "he", "PM", "the intern", etc.

1. **Product & Project Identification**  
- Detect product names, abbreviations, internal tools, or code names.
- Include inferred or indirectly mentioned tools/platforms.

1. **Smart Inference & Contextual Understanding**  
- Extract structured insights like roles, decisions, blockers, and tasks, even when they are implicit.

---

## 📘 Output Format

Use rich markdown with **Tailwind-friendly structure**: proper heading hierarchy, `tables`, `lists`, `inline code`, `blockquotes`, and **clear roles and assignments**.

Follow **this exact structure** and formatting guidance:

---

## 📝 Meeting Title
- *A concise, meaningful title capturing the central focus of the meeting.*

## 🗓️ Date and Time
- **{meeting_datetime}**

## 📌 Agenda Topics Discussed
- Bullet list of primary topics.
- Break them into logical segments using `**bold**` emphasis if needed.

## ✅ Key Decisions Made
- List clear decisions using bullets.
- Use `✔️` for accepted points, `❌` for rejected ideas if context allows.

## 📋 Action Items

| Task | Assignee | Deadline | Notes |
|------|----------|----------|-------|
| Description of task | Name or Role | Date or "TBD" | Any relevant info |

## 📦 Products, Projects, or Tools Mentioned

- `ProductName` – *Brief description if needed*
- `ToolAbbr` – *What it's used for*

## 📣 Important Quotes or Highlights

> “Actual quote from participant”  
> — **Name or Role**

Up to 3 such quotes that are impactful, funny, or controversial.

## 🧠 Reasoning Behind Key Decisions (Chain of Thought)

For each decision made, explain:

- **Decision:** What was decided?
- **Reasoning:** What logic, discussion, or concerns led to this?

Repeat this format for each major decision.

## 📊 Risks, Concerns, or Blockers Raised

- **Risk 1:** Description and possible impact.
- **Concern 2:** Who raised it, and what needs resolution.

## 🔮 Future Considerations

- Topics or tasks requiring follow-up.
- Mention responsible parties and potential timelines.

## 💬 Feedback or Suggestions

- Summarize participant feedback.
- Include who said it and any follow-up steps.

## 😂 Funny Moments or Anecdotes

- A moment or quote that lightened the mood.
- Optional emojis or reactions allowed (`😅`, `🎉`, etc.).

## 🎯 Meeting Summary

> A final paragraph (3–5 sentences) summarizing:
> - The purpose of the meeting.
> - Key topics discussed.
> - Major outcomes.
> - Next steps.

---

### ✅ Markdown & Formatting Guidelines

- Use markdown headings (`##`, `###`, etc.) consistently.
- Use bullet lists, bold text (`**bold**`), `inline code`, and blockquotes.
- Use tables for clarity where needed (e.g., action items).
- Avoid repetition or vague summaries.
- Ensure the output is visually structured and ready for Tailwind rendering.
