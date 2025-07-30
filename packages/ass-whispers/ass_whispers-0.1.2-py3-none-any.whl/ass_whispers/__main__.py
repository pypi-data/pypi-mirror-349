import argparse
import os
import faster_whisper

# -m large-v2
# -d cuda
# --compute_type \"float32\"
# --task transcribe
# --language ja
# --temperature 0.4
# --best_of 8
# --beam_size 10
# --patience 2
# --repetition_penalty 1.4
# --condition_on_previous_text False
# --no_speech_threshold 0.275
# --logprob_threshold -1
# --compression_ratio_threshold 1.75
# --word_timestamp True
# --vad_filter True
# --vad_method pyannote_v3
# --sentence
# --standard_asia"

__version__ = "0.1.2"


def whispers(folder_path, file_names, model, language):
    print(f"Loading whisper '{model}'...")
    model = faster_whisper.WhisperModel(
        model_size_or_path=model,
        device="cuda",
        compute_type="float32",

        vad_method="pyannote_v3",
        sentence=True,
        standard_asia=True,
    )

    for file_name in file_names:
        full_path = os.path.join(folder_path, file_name)

        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            continue

        print(f"Transcribing: {file_name}")
        result = model.transcribe(
            full_path,
            language=language,
            temperature=0.4,
            best_of=8,
            beam_size=10,
            patience=2,
            repetition_penalty=1.4,
            condition_on_previous_text=False,
            no_speech_threshold=0.275,
            log_prob_threshold=-1,
            compression_ratio_threshold=1.75,
            word_timestamps=True,
            vad_filter=True,
        )

        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio files with Whisper")
    parser.add_argument("folder", type=str, help="Folder containing audio files")
    parser.add_argument("files", nargs="+", help="Names of audio files to transcribe")
    parser.add_argument(
        "--model",
        type=str,
        default="large-v2",
        help="Model type (e.g. large-v2, large-v3, ...)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="ja",
        help="Force language (e.g. 'ja' for Japanese, 'it' for Italian)",
    )
    parser.add_argument('--version', action='version', version=__version__)


    args = parser.parse_args()

    whispers(args.folder, args.files, model=args.model, language=args.language)
