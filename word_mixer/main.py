import random
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def get_files():
    return [f.stem for f in DATA_DIR.glob("*.md") if f.is_file()]

def read_words(file_name):
    file_path = DATA_DIR / f"{file_name}.md"
    word_map = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                word, meaning = line.split(":", 1)
                word_map[word.strip()] = meaning.strip()

    return word_map

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        files = get_files()

        if not files:
            print("\n⚠️ No files found in /data folder.")
            print("👉 Add some .md files and try again.\n")
            break

        print("\n📂 Available files:")
        print("   " + " | ".join(files))

        response = input("\n>>> Select a file ('q' to quit): ").strip()

        if response.lower() == 'q':
            print("\n👋 Exiting. See you next time!\n")
            break

        if response in files:
            word_map = read_words(response)

            # ------------------ Stage 1 ------------------
            print(f"\n📖 --- {response} Content ---\n")
            for word, meaning in word_map.items():
                print(f"• {word} → {meaning}")

            # ------------------ Stage 2 ------------------
            if input("\n🔀 Ready for Stage 2 (Scrambled words)? (y/n): ").lower() == 'y':
                guessed = 0
                clear_console()

                for word, meaning in word_map.items():
                    clean_word = word.split(". ", 1)[-1] if ". " in word else word
                    shuffled_word = "".join(random.sample(clean_word, len(clean_word)))

                    print(f"\n🔤 Scrambled: {shuffled_word}")
                    print(f"💡 Meaning: {meaning}")

                    answer = input(">>> Your guess: ").strip()

                    if answer.lower() == clean_word.lower().strip():
                        print(f"✔ Correct: {clean_word}")
                        guessed += 1
                    else:
                        print(f"❌ Wrong. Answer: {clean_word}")

                print(f"\n📊 Stage 2 Score: {guessed}/{len(word_map)}")

                # ------------------ Stage 3 ------------------
                if input("\n🧠 Ready for Stage 3 (Meaning → Word)? (y/n): ").lower() == 'y':
                    guessed = 0
                    clear_console()

                    items = list(word_map.items())
                    random.shuffle(items)

                    for word, meaning in items:
                        clean_word = word.split(". ", 1)[-1] if ". " in word else word

                        normalized_word = clean_word.lower().strip()
                        if normalized_word.startswith("to "):
                            normalized_word = normalized_word[3:]
                        elif normalized_word.startswith("a "):
                            normalized_word = normalized_word[2:]

                        print(f"\n🧠 Meaning: {meaning}")
                        answer = input(">>> Enter word: ").strip().lower()

                        if answer == normalized_word or answer == clean_word.lower().strip():
                            print(f"✔ Correct: {clean_word}")
                            guessed += 1
                        else:
                            print(f"❌ Wrong. Answer: {clean_word}")

                    print(f"\n🏁 Final Score: {guessed}/{len(word_map)}\n")

        else:
            print("\n❌ Invalid selection. Try again.")

if __name__ == "__main__":
    main()
