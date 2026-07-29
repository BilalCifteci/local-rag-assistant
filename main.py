"""Hafta 4: Local RAG Assistant - komut satiri arayuzu.

Kullaniciyi bir dongude soru sormaya davet eder, her soru icin
qa.answer_query() cagirip cevabi ekrana basar. "q" veya "exit" yazilarak
cikilir.
"""

import pathlib

import qa

DB_PATH = pathlib.Path(__file__).parent / "documents.db"


def main() -> None:
    print("=== Local RAG Assistant ===")
    print("Foundry Local ile tamamen cevrimdisi calisan dokuman soru-cevap asistani.")
    print("Cikmak icin 'q' yazin.\n")

    if not DB_PATH.exists():
        print("Uyari: documents.db bulunamadi. Once 'python ingest.py' calistirin.\n")
        return

    while True:
        question = input("Soru: ").strip()
        if not question:
            continue
        if question.lower() in {"q", "exit", "quit"}:
            print("Gorusmek uzere!")
            break

        try:
            answer = qa.answer_query(question)
        except Exception as exc:  # SDK/model hatalarini kullaniciya duzgun goster
            print(f"Hata olustu: {exc}\n")
            continue

        print(f"Cevap: {answer}\n")


if __name__ == "__main__":
    main()
