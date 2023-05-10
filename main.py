# Proyecto de practica Python para consumir API de ChatGPT e integrarla a la API de Telegram basado en el proyecto  de Guillermo Izquierdo
# https://github.com/memonkey01

import telebot 
import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Cargar API key desde una variable de entorno
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
openai.api_key = os.getenv("OPENAI_TOKEN")

#Funcion que devuelve la respuesta de ChatGPT, definimos la informacion y el tipo de respuesta que necesitamos a traves de un prompt
def get_answer(question):
    request = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            
            {"role": "system", "content":"Tu eres un excelennte inegeniero, matematico y programador experto en Python, ciencia de datos e inteligencia artificial "},
            {"role": "user", "content": f"""Eres un excelennte inegeniero, matematico y programador experto en Python, ciencia de datos e inteligencia artificial, vas a responder a mis preguntas de manera sencilla y de ser posible con refrencias extrernas, al finalizar tu respuesta siempre debes agregar 'Atte Bot GPT',
            solamente vas a responder preguntas de tu area de expertis, para otras preguntas responderas:'Esta pregunta esta fuera de mi area de conocimiento', mi pregunta es: {question}, recuerda que solo vas a responder preguntas de tu area de conocimeinto que es Matematica, programcion Python, ciencia de datos e inteligencia artificial"""}
        ]
    )
    print(request)
    output = request['choices'][0]['message']['content']
    return output

# Respuesta al comando /start que da incio a la conversacion
@bot.message_handler(commands= ["start","ayuda","help"])
def respuesta_start(message):
    #Mensaje de bienvenida al usuario
    bot.reply_to(message, "Hola mi nombre Es BotGPT, estoy para  ayudarte, por favor inicia tus consultas con la plabra 'Pregunta'")
    
#Respuesta a la consulta del usuario, solo si empieza con la palabra 'Pregunta'
@bot.message_handler(content_types='text')
def respuesta(message):
    prompt = message.text
    if message.text.startswith('Pregunta') :
        prompt = message.text
        answer = get_answer(prompt[9:])
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Haga su pregunta')



#
if __name__ == '__main__':
    print('Iniciando bot')
    bot.infinity_polling()        