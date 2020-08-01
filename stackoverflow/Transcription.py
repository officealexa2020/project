import speech_recognition as sr
from os import path
from pydub import AudioSegment
import wave
import contextlib
import os   # subdir
import glob
#pip3 install speechrecognition
# convert mp3 file to wav                                                       
#sound = AudioSegment.from_mp3("sample.mp3")
#sound.export("sample.wav", format="wav")
input_folder_path = "output.wav"    # input path of audio files
output_folder_path = "./Results/" 

def audio_text():
	AUDIO_FILE = input_folder_path
	wav_file1 = AudioSegment.from_file(file=AUDIO_FILE)
	wav_file1.set_frame_rate(100)
	loudness = wav_file1.dBFS
	x=23-abs(loudness)
	#print("Original dB range of Customer : ",loudness)
	wav_file1=wav_file1-x
	loudness = wav_file1.dBFS
	wav_file1.export("./data.wav", format="wav")

	# Trancription
	AUDIO_FILE = "./data.wav"
	text_file_name=input_folder_path
	text_file_name= text_file_name.split('.')[0]
	files= open(output_folder_path+text_file_name+".txt","w+")
	# use the audio file as the audio source
	r = sr.Recognizer()
	with contextlib.closing(wave.open(AUDIO_FILE,'r')) as f:  # to calculate the duration of file
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
		print("Total Duration : ",duration," Seconds")
		a=duration
		print("Transcription Start...\n\n")
		with sr.AudioFile(AUDIO_FILE) as source:
			r.adjust_for_ambient_noise(source,duration=0.5)
			while a >= 10:
				audio = r.record(source,duration=10)  # read the entire audio file
				try:
					text =r.recognize_google(audio)
					print(text)
					files.write(format(text) +"\n")
				except sr.UnknownValueError:                          # speech is unintelligible
					print(" ")
					files.write("\n")
				except sr.RequestError as e:
					print("Check your internet connection")
				a-=10
			if a < 10 :
				audio = r.record(source,duration=a)  # read the entire audio file
				try:
					text =r.recognize_google(audio)
					print(text)
					files.write(format(text) +"\n")
				except sr.UnknownValueError:                          # speech is unintelligible
					print(" ")
					files.write("\n")
				except sr.RequestError as e:
					print("Check your internet connection")
					

