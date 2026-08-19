"""Hafta 5: Fonksiyonel test senaryolari.

Cevaplanabilir (dokumanlarda karsiligi olan) ve cevaplanamaz (dokuman
disi) sorularla asistani sinar, sonuclari TEST_RESULTS.md dosyasina
yazar. Ayrica bos girdi gibi bir edge-case de kontrol edilir.

Not: "basarili/basarisiz" degerlendirmesi otomatik degil, insan
gozlemine dayanir (Hafta 5 plani buna gore); bu script sadece
cevaplari ve retrieval benzerlik skorlarini toplu halde uretir.
"""

import pathlib

import qa
import retrieval

RESULTS_PATH = pathlib.Path(__file__).parent / "TEST_RESULTS.md"

ANSWERABLE_QUESTIONS = [
    "Yazilim Muhendisligi bolumunde staj kac is gunu surer?",
    "Mezun olabilmek icin GANO en az kac olmali?",
    "Derslere devamsizlik sinirini asan ogrenciye hangi not verilir?",
    "Bir donemde en fazla kac dersten cekilebilirim?",
    "Lisans programinin normal ve azami ogretim suresi kac yildir?",
]

UNANSWERABLE_QUESTIONS = [
    "Bugun hava durumu nasil?",
    "2026 Dunya Kupasi'ni hangi ulke kazandi?",
]


def run_case(question: str) -> dict:
    chunks = retrieval.get_top_chunks(question, k=3)
    top_similarity = chunks[0].similarity if chunks else 0.0
    answer = qa.answer_query(question)
    return {
        "question": question,
        "top_similarity": top_similarity,
        "answer": answer,
    }


def run_empty_query_case() -> str:
    try:
        retrieval.get_top_chunks("", k=3)
        return "HATA: bos sorgu beklenmedik sekilde basarili oldu"
    except Exception as exc:
        return f"Beklenen davranis: bos sorgu reddedildi ({type(exc).__name__}: {exc})"


def main() -> None:
    lines = ["# Test Sonuclari (Hafta 5)", ""]

    lines.append("## Cevaplanabilir Sorular (dokumanlarda karsiligi var)")
    lines.append("")
    for question in ANSWERABLE_QUESTIONS:
        result = run_case(question)
        lines.append(f"### Soru: {result['question']}")
        lines.append(f"- En yuksek retrieval benzerligi: {result['top_similarity']:.4f}")
        lines.append(f"- Cevap: {result['answer']}")
        lines.append("")

    lines.append("## Cevaplanamaz Sorular (dokuman disi konu)")
    lines.append("")
    for question in UNANSWERABLE_QUESTIONS:
        result = run_case(question)
        lines.append(f"### Soru: {result['question']}")
        lines.append(f"- En yuksek retrieval benzerligi: {result['top_similarity']:.4f}")
        lines.append(f"- Cevap: {result['answer']}")
        lines.append("")

    lines.append("## Edge Case: Bos Sorgu")
    lines.append("")
    lines.append(f"- {run_empty_query_case()}")
    lines.append("")

    RESULTS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Test sonuclari yazildi: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
