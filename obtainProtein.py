import gzip
import requests
import shutil
import shlex, subprocess
import os
from os import remove
from os import mkdir
from os import rmdir
import os.path
from urllib import request
from urllib.request import urlopen, HTTPError, URLError
import pickle
import ssl

def modelosIndividualizados():
    mkdir("/home/joannadal/TFG/modelosIndividualizados")
    modeloshmm = open("final_list.hmms","r")
    contenido = modeloshmm.readlines()
    maxLines = len(contenido)
    i=0
    while i<maxLines:
        fichero = open("/home/joannadal/TFG/modelosIndividualizados/" + str(i) + ".hmm", 'w')
        while contenido[i] != "//\n":
            fichero.write(contenido[i])
            i=i+1
        fichero.write(contenido[i])
        fichero.close()
        i=i+1
    modeloshmm.close()

def obtenerProteinas():
    mkdir("/home/joannadal/TFG/hmmrProtein")
    for archivo in os.listdir("/home/joannadal/TFG/modelosIndividualizados/"):
        modeloFile= open('/home/joannadal/TFG/modelosIndividualizados/' + archivo,"r")
        contenido = modeloFile.readlines()
        name = contenido[1][6:]
        name = name.replace(".hmm", '').replace('\n', '')
        command_line = 'hmmsearch --pfamtblout /home/joannadal/TFG/hmmrProtein/' + name + '.txt /home/joannadal/TFG/modelosIndividualizados/' + archivo + ' uniprot-reviewed\ yes+taxonomy\ 10239.fasta'
        args = shlex.split(command_line)
        subprocess.call(args)
        modeloFile.close()

def eliminarModelosSinProteinas():
        for archivo in os.listdir("/home/joannadal/TFG/hmmrProtein/"):
            proteinFile= open('/home/joannadal/TFG/hmmrProtein/' + archivo,"r")
            line= proteinFile.readlines()[5]
            if len(line) == 1:
                remove('/home/joannadal/TFG/hmmrProtein/' + archivo)
            proteinFile.close()


def modelProteinFunction():
        mkdir("/home/joannadal/TFG/modelProteinaFunction")
        mkdir("/home/joannadal/TFG/GOProtein")
        for archivo in os.listdir("/home/joannadal/TFG/hmmrProtein/"):
            fichero = open("/home/joannadal/TFG/modelProteinaFunction/" + archivo, 'w')
            file = open("/home/joannadal/TFG/hmmrProtein/" + archivo, 'r')
            fichero.write("Model:" + '\n')
            archivo = archivo.replace(".txt", '')
            fichero.write(archivo + '\n\n')
            fichero.write ("Proteïnes víriques:" + '\n')
            contenido = file.readlines()
            i = 5
            while contenido[i] != '\n':
                fichero.write(contenido[i])
                code=contenido[i][3:9]
                f=open("/home/joannadal/TFG/GOProtein/" + code + ".txt", "ab")
                archivo = archivo + '\n\n'
                arch = archivo.encode('UTF-8')
                f.write(arch)
                try:
                    uniprot=request.urlopen("https://www.uniprot.org/uniprot/" + code + ".txt")
                    goFile=uniprot.read()
                    f.write(goFile)
                except HTTPError as e:
                    print('HTTP Error code: ', e.code)
                    finalAr = "//"
                    finalArBytes = finalAr.encode('UTF-8')
                    f.write(finalArBytes)
                except URLError as e:
                    print('URL Error: ', e.reason)
                    finalAr = "//"
                    finalArBytes = finalAr.encode('UTF-8')
                    f.write(finalArBytes)
                f.close()
                i= i+1
            fichero.write ('\n\n'+ "GO functions:" + '\n')
            file.close()
            fichero.close()

def modelGoFunction():
        for archivo in os.listdir("/home/joannadal/TFG/GOProtein/"):
            i=0
            j=0
            file = open("/home/joannadal/TFG/GOProtein/" + archivo, 'r')
            contenido = file.readlines()
            code = contenido[0]
            code = code.replace('\r', '').replace('\n', '')
            fichero = open("/home/joannadal/TFG/modelProteinaFunction/" + code + ".txt", "a+")
            for line in contenido:
                i=i+1
            line = contenido[j];
            line = line.replace('\r', '').replace('\n', '')
            while j<i:
                while line != "//":
                    if 'GO; GO:' in line:
                        fichero.write(line + '\n')
                    j=j+1
                    if j<i:
                        line=contenido[j]
                        line = line.replace('\r', '').replace('\n', '')
                j=j+1
                if j<i:
                    code = contenido[j]
                    code = code.replace('\r', '').replace('\n', '')
                    fichero.close()
                    fichero = open("/home/joannadal/TFG/modelProteinaFunction/" + code + ".txt", "a+")
                    line=contenido[j]
                    line = line.replace('\r', '').replace('\n', '')
            file.close()
            fichero.close()

#A0A0H5




def main():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    #modelosIndividualizados()
    #obtenerProteinas()
    #eliminarModelosSinProteinas()
    modelProteinFunction()
    modelGoFunction()

if __name__ == "__main__":
    main()
