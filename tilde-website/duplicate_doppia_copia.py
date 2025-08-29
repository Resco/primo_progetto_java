import os
try:
    import torch
    torch.set_num_threads(1)
except ImportError:
    pass
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

def translate_text_transformers(text, from_lang='it', to_lang='en'):
    if not pipeline:
        print("transformers non installato: la seconda copia non verrà tradotta.")
        return text
    translator = pipeline('translation', model='Helsinki-NLP/opus-mt-it-en')
    # Traduci ogni riga separatamente per mantenere la formattazione
    lines = text.split('\n')
    translated_lines = []
    for line in lines:
        if line.strip():
            result = translator(line)[0]['translation_text']
            translated_lines.append(result)
        else:
            translated_lines.append('')
    return '\n'.join(translated_lines)

def duplicate_doppia_copia(input_filename, output_dir):
    # Leggi il file sorgente
    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if '++DOPPIACOPIA++' in line and start_idx is None:
            start_idx = i
        if '++DOPPIACOPIAFINE++' in line and start_idx is not None:
            end_idx = i
            break

    # Sezioni
    head = lines[:start_idx] if start_idx is not None else []
    middle = lines[start_idx+1:end_idx] if start_idx is not None and end_idx is not None else []
    tail = lines[end_idx+1:] if end_idx is not None else []

    # Duplico il blocco centrale, traducendo la seconda copia in inglese
    middle_text = ''.join(middle)
    translated_text = translate_text_transformers(middle_text, from_lang='it', to_lang='en')
    translated_lines = [line + '\n' for line in translated_text.split('\n')]
    new_middle = middle + translated_lines

    # Unisco tutto
    new_lines = head + new_middle + tail

    # Output filename
    base_name = os.path.basename(input_filename)
    output_path = os.path.join(output_dir, base_name)

    # Scrivi il nuovo file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Creato: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, 'txt', 'totranslate')
    output_dir = os.path.join(base_dir, 'txt')
    # Prendi tutti i file .txt nella cartella di input
    if not os.path.exists(input_dir):
        print(f"La cartella {input_dir} non esiste.")
    else:
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                input_path = os.path.join(input_dir, filename)
                duplicate_doppia_copia(input_path, output_dir)
