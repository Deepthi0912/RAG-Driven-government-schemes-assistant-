
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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to your .env file."
    )


# --------------------------------------------------
# 2. GROQ CONFIGURATION
# --------------------------------------------------

MODEL_NAME = "openai/gpt-oss-120b"

client = Groq(
    api_key=GROQ_API_KEY,
    timeout=60.0,
    max_retries=1
)


# --------------------------------------------------
# 3. ANSWER GENERATION FUNCTION
# --------------------------------------------------

def generate_answer(question: str):

    total_start = time.perf_counter()

    # ----------------------------------------------
    # STEP 1: RETRIEVE RELEVANT DOCUMENTS
    # ----------------------------------------------

    print("\nSearching government documents...", flush=True)

    retrieval_start = time.perf_counter()

    try:

        retrieved_chunks = retrieve_relevant_chunks(
            question,
            top_k=4
        )

    except Exception as error:

        print("Retrieval error:", error)

        return {
            "answer": (
                "SchemeWise could not retrieve information "
                "from its knowledge base. Please try again."
            ),
            "sources": [],
            "timings": {}
        }

    retrieval_time = time.perf_counter() - retrieval_start

    if not retrieved_chunks:

        return {
            "answer": (
                "I could not find relevant information in the "
                "available government scheme documents."
            ),
            "sources": [],
            "timings": {
                "retrieval_seconds": round(retrieval_time, 2)
            }
        }

    # ----------------------------------------------
    # STEP 2: PREPARE DOCUMENT CONTEXT
    # ----------------------------------------------

    context_parts = []
    sources = []

    for chunk in retrieved_chunks:

        source_file = chunk.get(
            "source_file",
            "Unknown document"
        )

        page_number = chunk.get(
            "page_number",
            "Unknown"
        )

        text = chunk.get("text", "")

        if not text.strip():
            continue

        context_parts.append(
            f"""
SOURCE FILE: {source_file}
PAGE NUMBER: {page_number}

DOCUMENT CONTENT:
{text}
"""
        )

        source_info = {
            "source_file": source_file,
            "page_number": page_number
        }

        if source_info not in sources:
            sources.append(source_info)

    if not context_parts:

        return {
            "answer": (
                "Relevant documents were retrieved, but "
                "they contained no usable text."
            ),
            "sources": sources,
            "timings": {
                "retrieval_seconds": round(retrieval_time, 2)
            }
        }

    context = "\n\n".join(context_parts)

    # ----------------------------------------------
    # STEP 3: BUILD STRICT RAG PROMPT
    # ----------------------------------------------

    prompt = f"""
You are SchemeWise, an AI assistant that explains
Indian government welfare schemes.

Your task is to answer the user's question using ONLY
the retrieved government document passages below.

USER QUESTION:
{question}

RETRIEVED GOVERNMENT DOCUMENTS:
{context}

STRICT INSTRUCTIONS:

1. Answer using only facts explicitly supported by
   the retrieved document passages.

2. Never add information from your general knowledge.

3. Do not assume eligibility conditions. If the documents
   do not explicitly establish a condition, do not state it
   as a requirement.

4. Do not introduce unrelated scheme benefits or services.

5. Clearly distinguish:
   - Eligibility criteria
   - Financial benefits
   - Application and registration requirements
   - Payment conditions

6. Mention the exact benefit amount and payment structure
   only if supported by the retrieved documents.

7. Cite the actual source filename and page number
   provided in the context.

8. Never invent a citation or attribute information
   to a document that does not support it.

9. If the retrieved passages do not contain enough
   information, clearly say what is missing.

10. If the documents may be outdated, advise the user
    to verify the latest official government guidelines.

11. Use simple language and concise formatting.

12. Keep the answer within approximately 250-350 words.

ANSWER:
"""

    # ----------------------------------------------
    # STEP 4: GENERATE ANSWER USING GROQ
    # ----------------------------------------------

    print("Generating answer with Groq...", flush=True)

    generation_start = time.perf_counter()

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SchemeWise. "
                        "Provide accurate, document-grounded "
                        "answers about Indian government schemes. "
                        "Never invent facts or citations."
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

        answer = response.choices[0].message.content

        if not answer:
            answer = (
                "Groq did not return an answer. "
                "Please try again."
            )

    except Exception as error:

        print("\nGroq generation error:", error)

        answer = (
            "SchemeWise could not generate an answer right now. "
            "Please try again after some time."
        )

    generation_time = time.perf_counter() - generation_start

    total_time = time.perf_counter() - total_start

    # ----------------------------------------------
    # STEP 5: PERFORMANCE METRICS
    # ----------------------------------------------

    timings = {
        "retrieval_seconds": round(retrieval_time, 2),
        "generation_seconds": round(generation_time, 2),
        "total_seconds": round(total_time, 2)
    }

    print("\nPerformance:")
    print(
        "Retrieval time:",
        timings["retrieval_seconds"],
        "seconds"
    )

    print(
        "Groq generation time:",
        timings["generation_seconds"],
        "seconds"
    )

    print(
        "Total time:",
        timings["total_seconds"],
        "seconds"
    )

    # ----------------------------------------------
    # STEP 6: RETURN RESULT
    # ----------------------------------------------

    return {
        "answer": answer,
        "sources": sources,
        "timings": timings
    }


# --------------------------------------------------
# 4. COMMAND-LINE INTERFACE
# --------------------------------------------------

def main():

    print("\n========== SchemeWise AI Assistant ==========")
    print("Ask questions about Indian government schemes.")
    print("Type 'exit' to quit.")

    try:

        while True:

            question = input("\nYour question: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("\nThank you for using SchemeWise!")
                break

            if not question:
                print("Please enter a question.")
                continue

            result = generate_answer(question)

            print("\n========== SCHEMEWISE ANSWER ==========\n")

            print(result["answer"])

            print("\n========== SOURCES ==========")

            if result["sources"]:

                for source in result["sources"]:

                    print(
                        f"- {source['source_file']} "
                        f"(Page {source['page_number']})"
                    )

            else:

                print("No sources available.")

            print("\n========== PERFORMANCE ==========")

            for metric, value in result["timings"].items():

                print(f"{metric}: {value} seconds")

    finally:

        client.close()


if __name__ == "__main__":
    main()
