import PySimpleGUI as sg
import requests
from algorythm import RSA

is_LoggenIn = False
username = ""
e, n, d = RSA().generate_keys()
s_exp, s_module = None, None

sg.theme('BluePurple')

layout = [[sg.Text('Input username:', key='name', size=(20, 1)), sg.Text(size=(20, 1), key='output')],
          [sg.Text(key='raw_text_sent', size=(30, 1)), sg.Text(key='text_sent', size=(30, 1))],
          [sg.Text(key='raw_text_received', size=(30, 1)), sg.Text(key='text_received', size=(30, 1))],
          [sg.Input(key='input')],
          [sg.Button('Send'), sg.Button('Exit')]]

window = sg.Window('RSA simple chat', layout)

while True:  # Event Loop
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == 'Send':
        if is_LoggenIn and values['input'] is not None:
            text = values['input']
            to_response_text = RSA().encrypt_str(text, s_exp, s_module)
            data = {'username': username, 'text': to_response_text}
            response = requests.post('http://127.0.0.1:8000/chat/', data).json()
            if 'text' in response:
                window['raw_text_sent'].update(text)
                window['text_sent'].update(to_response_text)
                window['text_received'].update(response['text'])
                decrypted_text = RSA().decrypt_str(response['text'], d, n)
                window['raw_text_received'].update(decrypted_text)
        else:
            if values['input'] is not None:
                data = {'username': values['input'], 'user_key_module': n, 'user_key_exponent': e}
                response = requests.post('http://127.0.0.1:8000/register/', data).json()
                if 'response' in response:
                    is_LoggenIn = True

                    window['name'].update('Enter your message:')
                    username = response['username']
                    window['output'].update('Your name: '+username)
                    s_exp, s_module = response['server_exponent'], response['server_module']
                    window['input'].update('')


window.close()