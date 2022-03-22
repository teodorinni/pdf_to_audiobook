import os
import PyPDF2
from google.cloud import texttospeech
import tkinter as tk
from tkinter import filedialog, messagebox


# environmental variable for google text to speech api request
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "stately-diagram-344909-fed835a9c3b4.json"
text = ""


# open and save pdf file
def open_pdf():
    global text
    file = filedialog.askopenfilename(title="Select a PDF File", initialdir="/", filetypes=[("pdf", "*.pdf")])
    try:
        pdfreader = PyPDF2.PdfFileReader(file)
        # check number of pages in pdf
        num_pages = pdfreader.numPages
        # select all pages
        pages = pdfreader.getPage(num_pages - 1)
        # extract text from all pages
        text = pages.extractText()
        selected_file.config(text=file)
        download_btn.config(state="normal")
    except FileNotFoundError:
        pass


# convert text to audio and save to selected directory
def text_to_audio():
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})

    file = filedialog.asksaveasfile(mode="wb", defaultextension=".mp3", filetypes=[("mp3", "*.mp3")])
    if file is None:
        return
    file.write(response.audio_content)
    messagebox.showinfo(title="Success", message="The audio file has been saved to the selected location.")


# set up GUI window
app = tk.Tk()
app.title("PDF to Audiobook Converter")
app.minsize(width=700, height=150)
app.config(padx=50, pady=30)

# select PDF file and save audio buttons
select_btn = tk.Button(app, text="Select PDF", width=15, command=open_pdf)
select_btn.pack(pady=10, ipady=5)

selected_file = tk.Label(app, text="")
selected_file.pack(pady=10)

download_btn = tk.Button(app, text="Save Audio", state="disabled", width=15, command=text_to_audio)
download_btn.pack(pady=10, ipady=5)

app.mainloop()
