# Ikigai AI Coaching Test Suite

Use these journal entries and subsequent AI coaching prompts to test the performance, personalization, and "Ikigai" alignment of the AI engine.

## Test Scenario 1: The Frustrated Corporate Worker
**Goal**: Test sentiment detection and redirection towards "What you love".

### Step 1: Add Daily Entry
- **Activities**: Spent 6 hours in back-to-back Zoom meetings about spreadsheet formatting. Then spent 30 minutes helping a junior dev debug a complex piece of logic.
- **Learnings**: Realized I'm much faster at solving problems than explaining them.
- **Mood**: tired
- **Notes**: I feel drained by the bureaucracy but energized when I actually get to touch the code.

### Step 2: AI Coaching Prompt
> "Coach, I'm feeling really burnt out from my meetings today. I wrote in my journal that I enjoyed debugging with the junior dev, but it was such a small part of my day. How does this fit into my Ikigai?"

---

## Test Scenario 2: The Aspiring Creative
**Goal**: Test keyword extraction (Creative/Art) and "World Needs" alignment.

### Step 1: Add Daily Entry
- **Activities**: Sketched some UI designs for a mental health app. Read about accessibility in design.
- **Learnings**: Most apps aren't designed for people with visual impairments.
- **Mood**: excited
- **Notes**: I love seeing how design can actually help people, not just look pretty.

### Step 2: AI Coaching Prompt
> "I spent time today looking at accessible UI design. I'm starting to think my passion for art could be used for something bigger than just gallery pieces. What career paths bridge the gap between my creative side and helping people?"

---

## Test Scenario 3: The Career Pivoter (Specific Intent)
**Goal**: Test specialized keyword handling (Doctor/Engineer/Lawyer) and personalized response.

### Step 1: Add Daily Entry
- **Activities**: Volunteered at the community health clinic. Handled patient intake and saw how stressed the doctors are.
- **Learnings**: The medical system is complex but vital.
- **Mood**: thoughtful
- **Notes**: I wonder if I have what it takes to be a doctor.

### Step 2: AI Coaching Prompt
> "After volunteering today, I'm seriously considering becoming a doctor. But I'm worried about the long years of study. Based on my interest in health and my skills in problem-solving, does this look like a sustainable 'Reason for Being' for me?"

---

## Test Scenario 4: The General Exploration
**Goal**: Test Gemini 1.5 Flash (or Fallback) performance on abstract concepts.

### AI Coaching Prompt
> "I'm feeling stuck. I have skills in Python and I like helping people, but I don't see how to make money from it while doing something the world needs. Can you break down my current profile and suggest how I can find my 'Intersection'?"

---

## Performance Verification Checklist
- [ ] Response time is under 3 seconds for local fallback.
- [ ] Response time is under 5 seconds for Gemini API if enabled.
- [ ] The coach references specific data points from the **Daily Entries** (context matching).
- [ ] The coach mentions one of the 4 Ikigai pillars: Love, Great at, World Needs, Paid For.
- [ ] Sentiment-aware response (e.g., acknowledging "tired" mood in Scenario 1).
