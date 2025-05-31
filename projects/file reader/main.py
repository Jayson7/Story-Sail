import os
import pyttsx3
import PyPDF2

# Initialize TTS engine
engine = pyttsx3.init()

# Folder containing your books
LIBRARY_PATH = "./library"

def speak(text):
    print(f"[SPEAKING] {text}")
    engine.say(text)
    engine.runAndWait()

def list_books():
    files = os.listdir(LIBRARY_PATH)
    books = [f for f in files if f.endswith('.pdf') or f.endswith('.txt')]
    books.sort()
    return books

def read_txt_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        speak(content)
    except Exception as e:
        speak(f"Sorry, I could not read this text file. Reason: {e}")

def read_pdf_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            if reader.is_encrypted:
                speak("Sorry, this PDF is encrypted and cannot be read.")
                return
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if text.strip():
                speak(text)
            else:
                speak("This PDF appears to be empty or non-readable.")
    except Exception as e:
        speak(f"Sorry, I could not read this PDF. Reason: {e}")

def handle_user_choice(books, choice):
    try:
        index = int(choice) - 1
        if 0 <= index < len(books):
            book = books[index]
            path = os.path.join(LIBRARY_PATH, book)
            speak(f"Reading {book}")
            if book.endswith('.pdf'):
                read_pdf_file(path)
            elif book.endswith('.txt'):
                read_txt_file(path)
        else:
            speak(f"Invalid number. Please select a number between 1 and {len(books)}.")
    except ValueError:
        speak("Please enter a valid number.")

def main():
    while True:
        books = list_books()
        if not books:
            speak("Your library is empty.")
            break

        speak("Here are the books in your library:")
        for i, book in enumerate(books, 1):
            speak(f"{i}. {book}")

        speak(f"Please enter a number between 1 and {len(books)} to select a book.")
        choice = input("Your choice: ")
        handle_user_choice(books, choice)
        speak("Would you like to choose another book? Type y for yes or any other key to exit.")
        if input("Continue? [y/N]: ").lower() != 'y':
            break

if __name__ == "__main__":
    main()
