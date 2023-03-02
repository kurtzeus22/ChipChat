import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import pyttsx3, pygame, json, re, shutil, os, random_responses, random

#ChipChat V0.5 by DZeus

if not os.path.exists('tempvoice'):
    os.makedirs('tempvoice')

# Load OUTPUTS
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)
response_data = load_json("bot.json")

# Initialize the voice Recognition
r = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()

# Create an MP3 for the Text
def speak(text):
    date_string = datetime.utcnow().strftime("%d%m%Y%H%M%S")
    filename = "tempvoice/voice"+date_string+".mp3"
    tts = gTTS(text=text, lang='en', tld='com.au')
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

#Print Interaction
def listen():
    with sr.Microphone() as source:
        print("Speak something!")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
            return text
        except:
            print("Sorry, I did not understand that.")
            return ""

#Response Definition
def respond(command):
    split_message = re.split(r'\s+|[,;?!.-]\s*', command.lower())
    score_list = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if command == "":
        return speak("Please tell me something so we can talk to each other")

    # Return if blank voice
    if best_response != 0:
        response = response_data[response_index]["bot_response"]

    #Specific Responses
        #TIME
        if "time" in command: 
            current_time_now = datetime.now()
            current_time = current_time_now.strftime("%H:%M")
            bot_response = response.replace("LATIME", current_time)

        #DATE
        if "date" in command:
            current_date_now = datetime.now()
            current_date = current_date_now.strftime("%m-%d-%Y")
            bot_response = response.replace("LADATE", current_date)
        
        #JOKES
        if "tell" and "joke" in command:
            randjoke = random.randint(1,3)
            match randjoke:
                case 1: bot_response = ("Why did the chatbot go to therapy? Because it had too many unresolved dialogues!")
                case 2: bot_response = ("Why did the chatbot go on a diet? It wanted to reduce its word count!")
                case 3: bot_response = ("What did the chatbot say when it got confused? I need to reboot my artificial stupidity!")
        return speak(bot_response)
    
        

    return speak(random_responses.random_string())

#Google Voice
while True:
    command = listen().lower()
    if "exit" in command:
        shutil.rmtree('tempvoice', ignore_errors=True)
        break        
    respond(command)
    
pygame.mixer.quit()