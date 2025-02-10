from django.shortcuts import render, redirect
import random

def inicio_juego(request):
    # Inicialización de sesión si es la primera vez
    session = request.session
    session.setdefault('secret_number', str(random.randint(1000, 9999)))
    session.setdefault('trys', 0)
    session.setdefault('history', [])

    mensaje = ''
    
    if request.method == 'POST':
        intento = request.POST.get('intento', '')

        if not (intento.isdigit() and len(intento) == 4):
            mensaje = "Se debe ingresar un número de sólo 4 dígitos"
        else:
            secret_number = session['secret_number']
            trys = session['trys'] + 1

            # Cálculo de puntos y famas
            puntos = sum(1 for i, num in enumerate(intento) if num == secret_number[i])
            famas = sum(min(intento.count(d), secret_number.count(d)) for d in set(intento)) - puntos

            # Registrar intento en history
            session['history'].append({'intento': intento, 'puntos': puntos, 'famas': famas})
            session['trys'] = trys

            # Determinar estado del juego
            if puntos == 4:
                mensaje = f'¡Wow! Adivinaste el número: {secret_number} en  tan sólo {trys} intentos.'
                session.flush()  # Reinicia la sesión al ganar
            elif trys >= 7:
                mensaje = f'¡Ya no tienes más intentos! :(. El número secreto era {secret_number}.'
                session.flush()  # Reinicia la sesión al perder
            else:
                mensaje = f'Intento {trys}: {intento} - Puntos: {puntos}, Famas: {famas}'

    return render(request, 'juego.html', {
        'mensaje': mensaje,
        'history': session.get('history', []),
        'trys_restantes': 7 - session.get('trys', 0)
    })

def reiniciar_juego(request):
    request.session.flush()
    return redirect('inicio_juego')
