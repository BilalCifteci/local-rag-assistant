"""Hafta 4: Retrieval + yerel LLM entegrasyonu.

answer_query(question) once retrieval.get_top_chunks ile en alakali dokuman
parcalarini bulur, sonra bu parcalari baglam olarak sistem promptuna ekleyip
Foundry Local sohbet modelinden cevap alir.
"""

import pathlib

from foundry_local_sdk import Configuration, FoundryLocalManager

import retrieval

CHAT_MODEL_ALIAS = "phi-3.5-mini"

# Hafta 5 testlerinde gozlemlendi: konu ici sorularda en yuksek retrieval
# benzerligi ~0.62-0.69, konu disi sorularda ~0.31-0.37 cikiyor. Model tek
# basina "bilmiyorum" talimatina guvenilir uymadigi icin bu esigin altinda
# LLM'e hic sormadan sabit bir fallback cevabi donduruyoruz.
MIN_SIMILARITY_THRESHOLD = 0.45
FALLBACK_ANSWER = "Bu bilgi elimdeki dokumanlarda yok."

SYSTEM_PROMPT = (
    "Sen, verilen dokuman parcalarina dayanarak soru cevaplayan bir asistansin. "
    "Kurallar:\n"
    "1. Sadece asagida sana verilen baglamdaki bilgiyi kullan, bunun disinda "
    "bilgi uydurma.\n"
    "2. Baglamda cevap yoksa acikca 'Bu bilgi elimdeki dokumanlarda yok' de.\n"
    "3. Cevabinin sonunda hangi kaynak dokuman(lar)dan yararlandigini belirt.\n"
    "4. Kisa ve net cevap ver."
)

_manager = None
_chat_model = None


def _get_chat_model():
    global _manager, _chat_model
    if _chat_model is not None:
        return _chat_model

    if FoundryLocalManager.instance is None:
        FoundryLocalManager.initialize(Configuration(app_name="local-rag-assistant"))
    _manager = FoundryLocalManager.instance

    model = _manager.catalog.get_model(CHAT_MODEL_ALIAS)
    model.download()
    model.load()
    _chat_model = model
    return model


def _build_context(chunks: list[retrieval.RetrievedChunk]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(f"[Kaynak: {chunk.source}]\n{chunk.content}")
    return "\n\n---\n\n".join(parts)


def answer_query(question: str, k: int = 3) -> str:
    """Soruyu retrieval + yerel LLM ile cevaplar, bulunan kaynaklari da dondurur."""
    chunks = retrieval.get_top_chunks(question, k=k)
    if not chunks or chunks[0].similarity < MIN_SIMILARITY_THRESHOLD:
        return FALLBACK_ANSWER

    context = _build_context(chunks)

    model = _get_chat_model()
    client = model.get_chat_client()
    client.settings.temperature = 0.2
    client.settings.max_tokens = 300

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Baglam:\n{context}\n\nSoru: {question}",
        },
    ]

    completion = client.complete_chat(messages)
    return completion.choices[0].message.content


if __name__ == "__main__":
    for question in [
        "RAG nedir, kisaca acikla?",
        "Bugun hava nasil?",
    ]:
        print(f"Soru: {question}")
        print(f"Cevap: {answer_query(question)}\n")
