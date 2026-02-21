from deep_translator import GoogleTranslator

def translate_to_hindi(transcription_segments):
    print("Translating transcriptions to Hindi...")
    translator = GoogleTranslator(source='en', target='hi')
    hindi_segments = []

    for seg in transcription_segments:
        # Context-aware translation can be added by swapping to IndicTrans2
        translated = translator.translate(seg['text'])
        hindi_segments.append({
            "start": seg['start'],
            "end": seg['end'],
            "en_text": seg['text'],
            "hi_text": translated
        })
    return hindi_segments
