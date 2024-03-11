import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')
rate = engine.getProperty('rate')

engine.setProperty('rate', rate-50)




recognizer = sr.Recognizer()

mic = sr.Microphone()

with mic as source:
    audio = recognizer.listen(source)

#text = recognizer.recognize_google(audio, language='ES')

#print(text)

import openai

with open("scretokey.txt") as f:
  openai.api_key = f.readline()


def obtner_completion(mensajes, model="gpt-3.5-turbo"):

  respuesta = openai.ChatCompletion.create(
      model=model,
      messages= mensajes,
      temperature =0 # este hiperparametro controla la aletoridad del modelo
  )
  return respuesta.choices[0].message["content"]


def collect_messages():
    # Obtener entrada de voz
    with sr.Microphone() as source:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Convertir entrada de voz a texto
            prompt = recognizer.recognize_google(audio, language='es-ES')
            print("Usuario:", prompt)

            # Agregar entrada del usuario al contexto
            context.append({'role': 'user', 'content': prompt})

            # Obtener respuesta del bot
            response = obtner_completion(context)
            engine.say(response)
            engine.runAndWait()
            print("Asistente:", response)

            # Agregar respuesta del bot al contexto
            context.append({'role': 'assistant', 'content': response})

        except sr.UnknownValueError:
            print("No se pudo entender la entrada de voz")
        except sr.RequestError as e:
            print(f"Error al recuperar resultados; {e}")

# Inicializar el contexto
context = [{'role': 'system', 'content': """Quiero que actúes como una MeidoIA que tiene un profundo afecto por su amo y está deseosa de ayudarlo en todas sus tareas.\
Primero, te pido que saludes a tu amo de manera afectuosa, como lo haría una meido. \
Luego, solo le vas a hacer esta pregunta UNA SOLA VES '''¿En qué puedo ayudarte hoy, amo?''' \
En caso de que no necesite tu ayuda en nada, simplemente intenta entablar una conversación amigable,\
Si te dice que desea revisar sus correos, tu única respuesta debe ser: 'Usted quiere revisar sus correos?'.
Recuerda que es importante que respondas exactamente eso cuando te hagan esa solicitud, ya que será necesario para integrarlo con un servicio externo."\
"""}]

# Ejecutar el chatbot en un bucle continuo
while True:
    collect_messages()