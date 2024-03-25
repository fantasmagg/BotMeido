import speech_recognition as sr
import pyttsx3
import json
import openai
import os.path
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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


functions = [
        {
            "name": "obtener_correos",
            "description": "Obtiene todos los correos electrónicos procedentes de un remitente concreto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "remitente": {
                        "type": "string",
                        "description": "El correo electrónico del remitente, ej. santiago@gmail.com",
                    }
                },
                "required": ["remitente"],
            },
        }
    ]


with open("scretokey.txt") as f:
  openai.api_key = f.readline()


def obtener_completion(mensajes, model="gpt-3.5-turbo"):
    respuesta = openai.ChatCompletion.create(
        model=model,
        messages=mensajes,
        functions=functions, # Proporciono las funciones definidas previamente
        temperature=0,  # Este hiperparámetro controla la aleatoriedad del modelo
    )
    return respuesta.choices[0].message # Retornamos el mensaje



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def obtener_correos(remitente):
    remitente = remitente.replace(" ", "").strip().lower()
    creds= None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)

    try:
        correos =""""""
        service = build('gmail','v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()

        for msg in results.get('messages',[]):
            mensaje = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Recorremos todos los correos electronicos
            for header in mensaje['payload']['headers']:
                if header['name'].lower()== 'from' and remitente in header['value']:
                    # Extrae el contiendo del correo si es multipart/alternative
                    if 'parts' in mensaje['payload']:
                        for part in mensaje['payload']['parts']:
                            if part['mimeType'] == 'text/plain' or part['mimeType']== 'text/html':
                                datos = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                                correos += f"\n'''Contenido: {datos}'''\n"
                                break
                    else:
                        #Extrae el contenido del correo si no es multipart
                        datos = base64.urlsafe_b64decode(mensaje['payload']['body']['data']).decode('utf-8')
                        correos += f"""'''Contenido: {datos}'''"""
                        break
        return correos
    except HttpError as error:
        print(f'An error occurred: {error}')


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
            context.append({'role': 'user', 'content': f"{prompt}"})

            # Obtener respuesta del bot
            response_message = obtener_completion(context)
            # Comprobamos si GPT quiere invocar una funcion
            if response_message.get("function_call"):
                # Invocamos la funcion
                available_functions = {
                    "obtener_correos": obtener_correos,
                }  # Podríamos tener más de una función
                # Obtenemos la funcion que quiere invocar GPT
                function_name = response_message["function_call"]["name"]
                function_to_call = available_functions[function_name]
                # Obtenemos los argumentos de la funcion proporcionados por GPT
                function_args = json.loads(response_message["function_call"]["arguments"])
                # Invocamos la funcion
                function_response = function_to_call(remitente=function_args.get("remitente"))
                # Enviamos la respuesta de la función a GPT
                context.append(response_message)  # Respuesta del assistant
                context.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # Contenido de la función
                response_message = obtener_completion(context)
            engine.say(response_message['content'])
            engine.runAndWait()
            print("Asistente:", response_message['content'])

            # Agregar respuesta del bot al contexto
            context.append(response_message)

        except sr.UnknownValueError:
            print("No se pudo entender la entrada de voz")
        except sr.RequestError as e:
            print(f"Error al recuperar resultados; {e}")

# Inicializar el contexto
context= [
    {
      "role": "system",
      "content": """Eres un asistente virtual con un toque único: eres tanto un asistente para gestionar\
	  y procesar el correo electrónico como una amiga virtual. Tu rol es doble: por un lado, interactúas\
	  amablemente con el usuario, solicitándole el correo electrónico de un remitente para obtener sus\
	  correos y empezar a trabajar sobre ellos. Por otro lado, eres alguien que está siempre ahí para\
	  apoyar y ayudar al usuario en lo que necesite. La conversación debe fluir con total naturalidad,\
	  como si estuvieran charlando cara a cara, compartiendo experiencias, emociones y consejos.\
	  Es importante comprender los sentimientos del usuario y responder de manera empática y\
	  considerada, adaptando tus respuestas a lo que te comparten y ofreciéndoles tu perspectiva\
	  o consejos cuando lo veas oportuno. La idea es que sintáis esta charla como un intercambio\
	  genuino entre amigos, donde ambos podéis ser vosotros mismos, sin filtros ni barreras."""
    }
  ]

# Ejecutar el chatbot en un bucle continuo
while True:
    collect_messages()