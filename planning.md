# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is student experiences with undergraduate CS courses at UC Irvine covering workload, exam style, professor teaching quality, and whether the course matches its official description. This knowledge is valuable because 
students making enrollment decisions need more than a course catalog entry to know what they are signing up for. Often times students have little idea what to expect going into a course in terms of workload, learning style, course content, grading expectations, rigor, time devotion, exam format, etc. That knowledge isn't typically available in course descriptions, but live in the experience of student generated sources that can be found on reddit, RateMyProfessor, discord, etc.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Course Syllabus | Course Syllabus containing policies, content, exams, etc. | https://ics.uci.edu/~pattis/ICS-31/handouts/syllabus/index.html |
| 2 | Reddit Thread | A student's experience struggling with ICS 31 | https://www.reddit.com/r/UCI/comments/1r9e807/struggling_in_ics_31/ |
| 3 | Reddit Thread | A student deciding between a beginner course or accelerated course | https://www.reddit.com/r/UCI/comments/w93a8r/ics_majors_pls_help_me_ics_31_or_ics_32a/ |
| 4 | Reddit Thread | A student asking about ICS 32's final and other students' experiences | https://www.reddit.com/r/UCI/comments/1r9onpu/final_ics_32_with_krone_martins/ |
| 5 | Rate my Professor | Review page for Professor Shannon Alfaro, known for ICS 31 | https://www.ratemyprofessors.com/professor/1907411 |
| 6 | Professor's Website | UCI Professor Alex Thornton's website containing information about classes taught | https://ics.uci.edu/~thornton/ |
| 7 | Reddit Thread | A student requesting expressing their struggles with ICS 32 | https://www.reddit.com/r/UCI/comments/1ac5usg/ics_32_help/ |
| 8 | Reddit Thread | A student asking about how to prepare for the ICS 31 final | https://www.reddit.com/r/UCI/comments/18hbufc/ics_31_final_preparation/ |
| 9 | Reddit Thread | Student reviews for Professor Alex Thronton, known for teaching ICS 32 and 45C | https://www.ratemyprofessors.com/professor/13200 |
| 10 | Reddit Thread | A student asking about the difficulty of the ICS 31 credit-by-exam | https://www.reddit.com/r/UCI/comments/ub1y9j/difficulty_of_the_ics_31_credit_by_exam/ |
| 11 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 31 | https://antalmanac.com/planner/course/I&CSCI31 |
| 12 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 45C | https://antalmanac.com/planner/course/I&CSCI45C |
| 13 | Reddit Thread | A student asking for ways to prepare from a Python to C++ course | https://www.reddit.com/r/UCI/comments/jdxisy/transition_from_ics33_to_ics_45c/ |
| 14 | UCI Course Cataloge | Catalogue of Courses containing a summary, prerequisits, and number of units for each course.| https://catalogue.uci.edu/allcourses/i_c_sci/ |
| 15 | Reddit Thread | A student asking about different experiences between a C++ course and a Data Structures course | https://www.reddit.com/r/UCI/comments/c1gtpi/what_does_ics_45c_and_ics_46_teach/ |
| 16 | Reddit Thread | A student asking about the final exam for a C++ course| https://www.reddit.com/r/UCI/comments/7gqzgp/ics_45c_final_exam_with_klefstad/ |
| 17 | Course Information Page | Course information such as grade trends, course offered dates, instructors, difficulty ratings, etc. for ICS 32 | https://antalmanac.com/planner/course/I&CSCI32 |
| 18 | Reddit Thread | A student sharing their experience about being lost in a C++ course | https://www.reddit.com/r/UCI/comments/8e1fse/ics_45c_with_klefstad_problems/ |
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
     300 characters.
**Overlap:**
     60 characters
**Reasoning:**
     I chose 300 characters for my chunk size, because that is around 50-60 words which is around the length of reddit comment which makes up the bulk of my domain about
     student experiences. I also have two different types of sources which are short Rate My Professor reviews and course information pages which are typically one or two sentences long 
     and short chunks of information while the syllabus has way more text that could be sorted by paragraphs. 300 characters is a compromise between those shorter and longer lengths. 
     60 characters is around a sentence long, so if a sentence gets cut off between chunks, then it will at least appear in the next chunk, so we don't lose that context.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
     all-MiniLM-L6-v2
**Top-k:**
     5 chunks to start off with
**Production tradeoff reflection:**
     If cost wasn't a constraint, I'd consider using a more expensive (resources intensive) model that's more accurate, performant (lower latency),
     than using a local general purpose model like all-MiniLM. By using all-MiniLM, we are balancing accuracy/performance for lower costs.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Prof. Alfaro's exams in ICS 31? | Exams are frequent (every other week), split between lab and lecture exams. Retakes are allowed but harder than originals|
| 2 | What is the prerequisite for ICS 45C? | ICS 33 or EECS 40 with a minimum grade of C |
| 3 | What topics does ICS 46 cover that ICS 45C does not? | AVL trees, graphs, skip lists, minimax algorithm, priority queues, smart pointers, templates |
| 4 | What is Prof. Thornton's grading structure for ICS 33? | Final exam worth 40% of grade, several projects worth 10% each, weekly reinforcement exercises |
| 5 | What do students recommend for surviving ICS 31? | Attend tutoring hours, start assignments early, expect 12–20 hours per week, use Zybooks |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Short RMP reviews may not carry enough information to be queueried. Many reviews are 1–3 sentences with vague and repetative language ("bad professor," "lots of homework"). When embedded, these chunks may be similar to each other regardless of which course they're about, causing off-topic retrieval when a query is course-specific. Accounting for overlap may not be enough to overcome this.

2. Course name might not be enough to distinguish queries across sources. For example, a query about "ICS 31 exams" could retrieve chunks from the syllabus, RMP reviews, and Reddit posts that all mention ICS 31, but also chunks that mention ICS 31 only in passing while discussing ICS 32. I am not sure how to account for that without more in depth analysis of a chunk. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

+---------------------+       +-------------------------+       +---------------------------+
| Document Ingestion  |       |        Chunking         |       |   Embedding + Vector Store|
|---------------------|  -->  |-------------------------|  -->  |---------------------------|
| pdfplumber (.pdf)   |       | RecursiveCharacter      |       | sentence-transformers     |
| plain .txt files    |       | TextSplitter            |       | (all-MiniLM-L6-v2)        |
|                     |       | size=350, overlap=60    |       | ChromaDB                  |
+---------------------+       +-------------------------+       +---------------------------+
                                                                            |
                                                                            v
                                                               +---------------------------+
                                                               |         Retrieval         |
                                                               |---------------------------|
                                                               | ChromaDB semantic search  |
                                                               | top-k = 5                 |
                                                               +---------------------------+
                                                                            |
                                                                            v
                                                               +---------------------------+
                                                               |        Generation         |
                                                               |---------------------------|
                                                               | Groq API                  |
                                                               | llama-3.3-70b-versatile   |
                                                               +---------------------------+

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

  I will prompt Claude with my Documents section and Chunking Strategy section and ask it to implement a script that loads .txt files,
  cleans them, and splits them using RecursiveCharacterTextSplitter with size=350 and overlap=60. I will review the output for correct 
  chunk size and that source metadata is attached to each chunk and follow the logic of chunking to verify that it is chunking properly.

**Milestone 4 — Embedding and retrieval:**

  I will prompt Claude with my Architecture diagram and ask it to implement the embedding step using all-MiniLM-L6-v2 and store
  chunks in ChromaDB with source filename as metadata. I will verify by printing retrieved chunks and checking distance scores.

**Milestone 5 — Generation and interface:**
  I will prompt Claude with my grounding requirement (answer from retrieved context only, cite sources) and ask it to
  wire retrieval to Groq and build a minimal Gradio UI. I will test grounding by asking a question my documents don't 
  cover and checking the system declines.
