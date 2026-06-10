# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     My domain are the student experiences, structural expectations, and workload realities of undergraduate computer science courses 
     (specifically lower-division introductory tracks like ICS 31, 32, and 45C) at UC Irvine. This knowledge is valuable because students making enrollment decisions need more than a course catalog entry to know what they are actually signing up for. Often times, students have little idea what to expect going into a course in terms of workload, learning style, grading expectations, time devotion, and exam formats. For example, official descriptions won't tell you about Professor Alfaro's exam retake policies, Professor Klefstad's strict grading penalties on handwritten quizzes, or the actual weekly time commitment required to complete a project. This practical information is missing from university channels, leaving it scattered across lengthy Reddit threads, Discord messages, and chaotic RateMyProfessor pages. This system consolidates that decentralized knowledge to help underclassmen make strategic scheduling decisions.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Course Syllabus | Course Syllabus containing policies, content, exams, etc. | https://ics.uci.edu/~pattis/ICS-31/handouts/syllabus/index.html |
| 2 | Reddit Thread | A student's experience struggling with ICS 31 | https://www.reddit.com/r/UCI/comments/1r9e807/struggling_in_ics_31/ |
| 3 | Reddit Thread | A student deciding between a beginner course or accelerated course | https://www.reddit.com/r/UCI/comments/w93a8r/ics_majors_pls_help_me_ics_31_or_ics_32a/ |
| 4 | Reddit Thread | A student asking about ICS 32's final and other students' experiences | https://www.reddit.com/r/UCI/comments/1r9onpu/final_ics_32_with_krone_martins/ |
| 5 | Rate my Professor | Review page for Professor Shannon Alfaro, known for ICS 31 | https://www.ratemyprofessors.com/professor/1907411 |
| 6 | Reddit Thread | Student experiences in 45C with Professor Klefstad | https://www.reddit.com/r/UCI/comments/1rcazw1/hows_icsci_45c_with_klefstad/ |
| 7 | Reddit Thread | A student requesting expressing their struggles with ICS 32 | https://www.reddit.com/r/UCI/comments/1ac5usg/ics_32_help/ |
| 8 | Reddit Thread | A student asking about how difficult ICS 45C is | https://www.reddit.com/r/UCI/comments/7cmajv/ics_45c_difficulty/ |
| 9 | Rate my Professor | Student reviews for Professor Alex Thronton, known for teaching ICS 32 and 45C | https://www.ratemyprofessors.com/professor/13200 |
| 10 | Reddit Thread | A student asking about the difficulty of the ICS 31 credit-by-exam | https://www.reddit.com/r/UCI/comments/ub1y9j/difficulty_of_the_ics_31_credit_by_exam/ |
| 11 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 31 | https://antalmanac.com/planner/course/I&CSCI31 |
| 12 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 45C | https://antalmanac.com/planner/course/I&CSCI45C |
| 13 | Reddit Thread | A student asking for ways to prepare from a Python to C++ course | https://www.reddit.com/r/UCI/comments/jdxisy/transition_from_ics33_to_ics_45c/ |
| 14 | UCI Course Cataloge | Catalogue of Courses containing a summary, prerequisits, and number of units for each course.| https://catalogue.uci.edu/allcourses/i_c_sci/ |
| 15 | Reddit Thread | A student asking about different experiences between a C++ course and a Data Structures course | https://www.reddit.com/r/UCI/comments/c1gtpi/what_does_ics_45c_and_ics_46_teach/ |
| 16 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 32 | https://antalmanac.com/planner/course/I&CSCI32 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
     350 characters
**Overlap:**
     60 characters
**Why these choices fit your documents:**
     A chunk size of 350 characters (around 50 to 60 words) was chosen as an intentional compromise to handle two completely different text layouts in our collection: short, single-sentence data snapshots from AntAlmanac/Course Catalogs, and long, multi-paragraph conversational threads from Reddit. Because RateMyProfessor reviews are often brief and opinionated, larger chunk sizes would dilute their unique sentiments. The 60-character overlap functions as roughly one sentence of padding. This ensures that if a vital tip or an exam policy gets mechanically sliced at a boundary, its full semantic context is kept intact and retrievable in the adjacent text chunk.
**Final chunk count:**
     320 chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
     all-MiniLM-L6-v2 via the sentence-transformers library, stored inside a local persistent ChromaDB collection configured for cosine distance metrics.
**Production tradeoff reflection:**
     I would weigh several critical infrastructure and performance tradeoffs before changing models. 1. all-MiniLM-L6-v2 enforced a hard limit on 256 tokens, while a comercial model like OpenAI's text embedding-3-large supports up to 8,192 tokens. Migrating would allow us to chunk by entire discussion threads or complete syllabus modules instead of individual comments which would capture more conversational context. Running our current model is local and free, which is as good as it gets, while introducing an comercial API-network call would introduce latency and higher costs which is a tradeoff of better performance.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
     Grounding is strictly enforced by pairing explicit negative-constraint parameters within the system instruction prompt with an increased chunk extraction pool. The model prompt is structured as follows:
     "You are an expert academic advisor helping students navigate UCI computer science courses. Answer the user's question using ONLY the provided text snippets below. Do not use your own external general knowledge, and do not assume or extrapolate facts. If the provided snippets do not contain the explicit facts required to completely answer the question, state exactly: "I don't have enough information on that." Your response must be objective and directly grounded in the context."

**How source attribution is surfaced in the response:**
     Source attribution is decoupled from the LLM's behavior to prevent formatting failures. The retrieval step extracts the origin filename directly from the metadata layer of the matching ChromaDB chunks (match['source']). Once the LLM generates its response text, the app pipeline appends a clean, dedicated bulleted checklist at the bottom of the interface displaying the unique text file names utilized (e.g., Sources used: • rmp_alfaro.txt), ensuring transparent source tracking.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Prof. Alfaro's exams in ICS 31? | Exams are frequent, split between lab and lecture. Retakes are allowed but harder. | Correctly notes that she isn't as bad as rumored, provides ample extra credit, and grants two exam retake tickets. | Relevant | Accurate |
| 2 | What is the prerequisite for ICS 45C? | ICS 33 or EECS 40 with a minimum grade of C | Discusses student anxiety transitioning from 33 to 45C instead of listing hard requirements. | Off-target | Inaccurate |
| 3 | What topics does ICS 46 cover that ICS 45C does not? | AVL trees, graphs, skip lists, minimax algorithm, priority queues, smart pointers, templates | Pinpoints a thread asking what they teach, but references looking at Thornton and Pattis' websites instead of listing specific technical topics. | Partially relevant | Partially accurate |
| 4 | What is Professor Thornton's grading structure for ICS 33 | I don't have enough information on that. (The provided documents contain grading and review data for Professor Thornton in ICS 32 and ICS 45C, but do not contain syllabus details or grading breakdowns for his section of ICS 33.) | | | |
| 5 | What do students recommend for surviving ICS 31? | Students recommend being proactive with assignments because they are easy to miss, and preparing for mandatory class attendance. For the course material or testing, it is highly recommended to study using the practice exams from previous ICS 31 courses, as the actual exam questions are historically very similar | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
     What is the prerequisite for ICS 45C
**What the system returned:**
     Instead of returning the factual course requirement listing, the system extracted casual conversational chunks from student discussion posts (reddit_ics33_to_45c.txt and reddit_45c_and_46.txt) detailing how difficult the classes are to pass and whether students should take a quarter off to study.
**Root cause (tied to a specific pipeline stage):**
     Because our chunk size is capped at 350 characters, the official catalog text chunk (uci_course_catalog.txt) is very short, dry, and concise. Meanwhile, our informal student Reddit documents repeat the words "ICS 33" and "ICS 45C" dozens of times across highly emotional paragraphs. The embedding model (all-MiniLM-L6-v2) calculated a closer semantic vector distance to the dense chatter inside the conversational Reddit posts than to the cold, factual entry in the catalog text. Because our top-k search limit was set to 3, the actual textbook prerequisite chunk was pushed entirely out of the context window, leaving the generation model with no facts to read.
**What you would change to fix it:**
     1. Expand Top-K Retrieval: I would increase top_k from 3 to 5. Opening up the context window allows lower-ranked, data-dense chunks from the official catalog to slide into view, giving the Llama generation model the data it needs to separate raw student opinions from official rules.
     2. Metadata Category Filtering: I would implement meta-tag filtering. If a user query contains hard structural terms (like "prerequisite," "units," or "catalog"), the system would prioritize official course catalog files over forum discussions.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
     The planning.md template was critical for setting strict data contract boundaries before writing code. Having a clear technical layout prevented me from writing generic logic, ensuring that the metadata keys (text, source, chunk_index) generated by my document processor seamlessly aligned with the incoming database schema expected by the vector database client.
**One way your implementation diverged from the spec, and why:**
     My implementation diverged during the document parsing logic in ingest.py. While the specification assumed we would run uniform character splitting across all materials, running manual inspections revealed that raw extractions generated a large number of meaningless text fragments (such as standalone thread metadata or solitary author numbers) under 80 characters. I had to explicitly modify the chunker code to evaluate and drop any text segment under 80 characters to prevent junk chunks from corrupting our database search results.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

What I gave the AI: I provided the AI assistant with my strict pipeline architecture ASCII diagram and the Chunking Strategy specifications written in my planning.md document, asking it to implement a LangChain text loader.

What it produced: It returned a modular Python script utilizing RecursiveCharacterTextSplitter configured for a size of 350 and an overlap of 60 characters.

What I changed or overrode: I overrode the loop logic by appending an explicit character length guard statement (if len(chunk) < 80: continue). The initial code structure produced by the AI was saving tiny, empty strings derived from document whitespace breaks, which would have occupied valuable vector storage and caused irrelevant search matches.

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

What I gave the AI: I requested an implementation for a modern ChromaDB search engine file (retriever.py), instructing that it must accept data payloads from the ingestion module and persistently save the index.

What it produced: It generated an implementation that used a deprecated collection method from an older, outdated edition of the ChromaDB library API.

What I changed or overrode: I completely overrode the outdated database connection calls and updated the code to use the modern storage client pattern (chromadb.PersistentClient) and explicitly defined standard cosine distance searching (metadata={"hnsw:space": "cosine"}) to ensure vector persistence on disk and accurate distance output scores.
