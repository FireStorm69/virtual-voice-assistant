""" This file contains the functions that are used to convert text to speech and vice versa"""
import os

import azure.cognitiveservices.speech as speechsdk

# import pyttsx3
# import speech_recognition as sr

# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[1].id)


def recognizer():
    """This function will take in audio and convert it to text"""
    speech_config = speechsdk.SpeechConfig(
        speech_recognition_language="en-IN",
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak now...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {speech_recognition_result.text}")
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            f"No speech could be recognized: {speech_recognition_result.no_match_details}"
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
            print("Did you set the speech resource key and region values?")
    return speech_recognition_result.text


def speak(text: str):
    """This function will take in text and convert it to speech"""
    speech_config = speechsdk.SpeechConfig(
        speech_recognition_language="en-IN",
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized to speaker for text [{text}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if (
            cancellation_details.reason == speechsdk.CancellationReason.Error
            and cancellation_details.error_details
        ):
            print(f"Error details: {cancellation_details.error_details}")
        print("Did you update the subscription info?")
    return result


def takecommand():
    # # sourcery skip: extract-method, inline-immediately-returned-variable
    # """
    # It takes a command from the user, and returns it as a string
    # :return: A string
    # """

    # with sr.Microphone() as source:
    #     print("Listening...")
    #     # r.pause_threshold = 0.7
    #     # r.energy_threshold = 10
    #     # r.energy_threshold = 300
    #     print("Now you can speak...")
    #     audio = recognizer()
    # try:
    #     print("Recognizing...")
    #     query = recognizer()
    #     print(f"User said: {query}\n")

    # except sr.RequestError as exception:
    #     print(exception)
    #     print("Unable to Recognize your voice.")
    #     return "None"
    query = recognizer()
    return query
