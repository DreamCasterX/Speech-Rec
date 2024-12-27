import sounddevice as sd
import speech_recognition as sr
from scipy.io.wavfile import write
from pydub import AudioSegment
from colorama import Fore, Style 


def record_audio(filename="recording.wav", duration=10, samplerate=44100, channels=2):
    print(f"開始錄音，持續 {duration} 秒...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()
    print("錄音完成")
    write(filename, samplerate, myrecording)


def audio_to_txt(audio_file="recording.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='zh-TW')
        print(f"辨識內容 >> {Fore.GREEN}{text}{Style.RESET_ALL}")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print("API Error:", e)


def convert_audio(input_file, output_file="converted_audio.wav"):
    """Converts audio to PCM WAV."""
    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav", codec="pcm_s16le")  # Use codec instead of filter
        return output_file
    except Exception as e:
        print(f"Error converting audio: {e}")
        return None

if __name__ == "__main__":
    while True:
        option = input("功能選項:\n  (1) 錄音\n  (2) 音檔辨識\n\n選擇: ")
        if option == "1":
            record_audio()
        elif option == "2":
            converted_file = convert_audio("recording.wav")
            if converted_file:
                audio_to_txt(converted_file)
        elif option.lower() == "q":
            break
        else:
            continue


