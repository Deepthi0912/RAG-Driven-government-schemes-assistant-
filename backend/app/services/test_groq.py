
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from app.services.retriever import retrieve_relevant_chunks


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to your .env file."
    )


# --------------------------------------------------
# 2. GROQ CONFIGURATION
# --------------------------------------------------

MODEL_NAME = "openai/gpt-oss-120b"

client = Groq(
    api_key=API_KEY,
    timeout=60.0,
    max_retries=1
)


# --------------------------------------------------
# 3. TEST QUESTION
# --------------------------------------------------

question = (
    "What benefits are available for the second "
    "girl child under PMMVY?"
)


def main():

    total_start = time.perf_counter()

    try:

        # ------------------------------------------
        # STEP 1: RETRIEVE DOCUMENTS
        # ------------------------------------------

        print("\nSearching government documents...", flush=True)

        retrieval_start = time.perf_counter()

        chunks = retrieve_relevant_chunks(
            question,
            top_k=4
        )

        retrieval_time = time.perf_counter() - retrieval_start

        if not chunks:
            print("No relevant documents found.")
            return

        # ------------------------------------------
        # STEP 2: PREPARE CONTEXT AND SOURCES
        # ------------------------------------------

        context_parts = []
        sources = []

        for chunk in chunks:

            source_file = chunk.get(
                "source_file",
                "Unknown document"
            )

            page_number = chunk.get(
                "page_number",
                "Unknown"
            )

            chunk_text = chunk.get("text", "")

            if not chunk_text.strip():
                continue

            context_parts.append(
                f"""
Source: {source_file}
Page: {page_number}

Content:
{chunk_text}
"""
            )

            source = {
                "source_file": source_file,
                "page_number": page_number
            }

            if source not in sources:
                sources.append(source)

        if not context_parts:
            print("Retrieved documents contain no usable text.")
            return

        context = "\n\n".join(context_parts)

        print(
            "Retrieval time:",
            round(retrieval_time, 2),
            "seconds"
        )

        # ------------------------------------------
        # STEP 3: BUILD PROMPT
        # ------------------------------------------

        prompt = f"""
You are SchemeWise, an AI assistant that explains
Indian government welfare schemes.

Answer the user's question using ONLY the supplied
government document context.

USER QUESTION:
{question}

GOVERNMENT DOCUMENT CONTEXT:
{context}

INSTRUCTIONS:

1. Give an accurate and easy-to-understand answer.
2. Use only the supplied document information.
3. Do not invent benefits, amounts or eligibility rules.
4. Explain important conditions clearly.
5. Distinguish eligibility from registration requirements.
6. Cite source filenames and page numbers.
7. If the answer is not available, say so.
8. Keep the answer concise, around 250-350 words.
9. Mention when information should be checked against
   the latest official government guidelines.

ANSWER:
"""

        # ------------------------------------------
        # STEP 4: GENERATE ANSWER USING GROQ
        # ------------------------------------------

        print(
            "\nGenerating answer using Groq...",
            flush=True
        )

        generation_start = time.perf_counter()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SchemeWise. "
                        "Answer government scheme questions "
                        "accurately using the supplied context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=1536,
            temperature=0.2,
            reasoning_effort="low"
        )

        generation_time = time.perf_counter() - generation_start

        answer = response.choices[0].message.content

        # ------------------------------------------
        # STEP 5: DISPLAY ANSWER
        # ------------------------------------------

        print("\n========== SCHEMEWISE ANSWER ==========\n")

        print(answer or "No answer generated.")

        print("\n========== SOURCES ==========")

        for source in sources:
            print(
                f"- {source['source_file']} "
                f"(Page {source['page_number']})"
            )

        # ------------------------------------------
        # STEP 6: PERFORMANCE
        # ------------------------------------------

        total_time = time.perf_counter() - total_start

        print("\n========== PERFORMANCE ==========")

        print(
            "Retrieval time:",
            round(retrieval_time, 2),
            "seconds"
        )

        print(
            "Generation time:",
            round(generation_time, 2),
            "seconds"
        )

        print(
            "Total time:",
            round(total_time, 2),
            "seconds"
        )

        # ------------------------------------------
        # STEP 7: TOKEN USAGE
        # ------------------------------------------

        if response.usage:

            print("\n========== TOKEN USAGE ==========")

            print(
                "Prompt tokens:",
                response.usage.prompt_tokens
            )

            print(
                "Completion tokens:",
                response.usage.completion_tokens
            )

            print(
                "Total tokens:",
                response.usage.total_tokens
            )

    except Exception as error:

        print("\nGROQ TEST FAILED")
        print(type(error).__name__, error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
