from django.shortcuts import render, redirect
from PIL import Image
from . import forms
from .utils.cifrar_mensaje import ocultar_texto
from .utils.leer_mensaje import leer
from arc4 import ARC4
from django.http import HttpResponse
import binascii

import os

def esteganografia(request, form_cifrado=forms.EsteganografiaCifradoForm(), form_descifrado=forms.EsteganografiaDescifradoForm()):
    # form_cifrado = forms.EsteganografiaCifradoForm()
    # form_descifrado = forms.EsteganografiaDescifradoForm()
    context = {
        'form_cifrado': form_cifrado,
        'form_descifrado': form_descifrado,
    }
    return render(request, 'form_cifrar_descifrar.html', context)

def descifrar(request):
    form_descifrado = forms.EsteganografiaDescifradoForm()
    if request.method == 'POST':
        form_descifrado = forms.EsteganografiaDescifradoForm(request.POST, request.FILES)

        if form_descifrado.is_valid():
            datos_imagen = form_descifrado.cleaned_data['imagen']
            llave_secreta = form_descifrado.cleaned_data['llave_secreta']
            imagen = Image.open(datos_imagen)

            mensaje_cifrado = leer(imagen)
            mensaje_cifrado = mensaje_cifrado.encode(encoding='ISO-8859-1')


            cifrador = ARC4(llave_secreta)
            try:
                mensaje_descifrado = cifrador.decrypt(mensaje_cifrado).decode('utf-8')
            except:
                mensaje_descifrado = cifrador.decrypt(mensaje_cifrado)

            return render(request, 'mensaje_revelado.html', {'mensaje_descifrado': mensaje_descifrado})
    return redirect('esteganografia', form_descifrado=form_descifrado)

def cifrar(request):
    form_cifrado = forms.EsteganografiaCifradoForm()
    if request.method == 'POST':
        form_cifrado = forms.EsteganografiaCifradoForm(request.POST, request.FILES)

        if form_cifrado.is_valid():
            datos_imagen = form_cifrado.cleaned_data['imagen']
            nombre_imagen = datos_imagen.name
            llave_secreta = form_cifrado.cleaned_data['llave_secreta']
            mensaje_cifrar = form_cifrado.cleaned_data['mensaje_cifrar']

            imagen = Image.open(datos_imagen)
            imagen = imagen.convert("RGB")
            cifrador = ARC4(llave_secreta)
            mensaje_cifrado = cifrador.encrypt(mensaje_cifrar)
            mensaje_cifrado = mensaje_cifrado.decode('unicode-escape')

            ruta_final = ocultar_texto(mensaje_cifrado, imagen, nombre_imagen)

            if os.path.exists(ruta_final):
                with open(ruta_final, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="image/png")
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(ruta_final)
                    return response
    return redirect('esteganografia', form_cifrado=form_cifrado)