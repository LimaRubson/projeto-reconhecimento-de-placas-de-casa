# Criar o arquivo evaluation_utils.py
import jiwer


def calculate_wer(true_text, predicted_text):
    # Verificar se os textos estão vazios ou inválidos antes de calcular o WER
    if not true_text.strip() or not predicted_text.strip():
        print("Um dos textos está vazio ou inválido. WER não será calculado.")
        return None

    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemovePunctuation(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip()
    ])

    # Transformar os textos
    transformed_true_text = transformation(true_text)
    transformed_predicted_text = transformation(predicted_text)

    # Verificar se os textos transformados contêm palavras válidas
    if not transformed_true_text.split() or not transformed_predicted_text.split():
        print("Texto transformado está vazio ou inválido. WER não será calculado.")
        return None

    # Calcular WER se os textos forem válidos
    wer_score = jiwer.wer(transformed_true_text, transformed_predicted_text)
    print(f"WER (Word Error Rate): {wer_score:.2f}")
    return wer_score
