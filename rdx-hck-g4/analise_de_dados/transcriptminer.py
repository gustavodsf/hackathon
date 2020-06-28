# -*- coding: utf-8 -*-
import os
import difflib as dfl
import re
import nltk.corpus
import pandas as pd

pattern = re.compile(r'\b(' + r'|'.join(nltk.corpus.stopwords.words('portuguese')) + r')\b\s*')

def tensao (texto):
    ret=[]
    ret.append(sum([dfl.SequenceMatcher(None,item,"tensao").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"volt").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"kV").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"eleva").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"reduzi").ratio()>0.75 for item in texto]))
    #ret.append(sum([dfl.SequenceMatcher(None,item,"máximo").ratio()>0.75 for item in texto]))
    #ret.append(sum([dfl.SequenceMatcher(None,item,"mínimo").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"barra").ratio()>0.75 for item in texto]))
    return ret

def reverter (texto):
    ret=[]
    ret.append(sum([dfl.SequenceMatcher(None,item,"revert").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"compensa").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"comutaç").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"uma_unidade").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"CAG").ratio()>0.75 for item in texto]))
    return ret

def hidro (texto):
    ret=[]
    ret.append(sum([dfl.SequenceMatcher(None,item,"hidrologia").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"chuva").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"milímetros").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"nível").ratio()>0.75 for item in texto]))
    return ret

def vertimento (texto):
    ret=[]
    ret.append(sum([int("verti" in item) for item in texto]))
    ret.append(sum([int("vertedouro" in item) for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"cúbicos").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"vazão").ratio()>0.75 for item in texto]))
    return ret
#esta função está fraca. Similaridade com revertido. 0.75 é um bom threshold.

def interrup (texto):
    ret=[]
    ret.append(sum([dfl.SequenceMatcher(None,item,"intervenção").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"deslig").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"manutenção").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"ocorrência").ratio()>0.75 for item in texto]))
    ret.append(sum([dfl.SequenceMatcher(None,item,"manobra").ratio()>0.75 for item in texto]))
    return ret

def classificacao(texto):
    return[sum(tensao(texto)),
     sum(reverter(texto)),
     sum(hidro(texto)),
     sum(vertimento(texto)),
     sum(interrup(texto))]

def preprocess(entry):
    entry=entry.replace("\n",' ').replace("Locutor 1:",' ').replace("Locutor 2:",' ').replace("uma unidade","uma_unidade").lower()
    entry=entry.replace("salto santiago","salto_santiago").replace("cana brava","cana_brava").replace("jorge lacerda","jorge_lacerda").replace("pampa sul","pampa_sul").replace("são salvador","são_salvador").replace("passo fundo","passo_fundo")
    entry = pattern.sub('', entry)
    entry =entry.replace("."," ").replace(","," ")
    arr_texto=entry.split(" ")
    return arr_texto

def get_data(texto):
    arr_texto=preprocess(texto)
    data=arr_texto[1][:4]+"-"+arr_texto[1][4:6]+"-"+arr_texto[1][6:8]+","+arr_texto[1][9:11]+":"+arr_texto[1][11:13]+":"+arr_texto[1][13:15]
    return data

def get_data_os(file):
    return os.path.basename(file)[:4]+"-"+os.path.basename(file)[4:6]+"-"+os.path.basename(file)[6:8]+","+os.path.basename(file)[9:11]+":"+os.path.basename(file)[11:13]+":"+os.path.basename(file)[13:15]

def get_ONS(tex):
    vetor=["ONS","Nordeste","Norte","Sul","Sudeste","COG","Oeste","Centro",'Sul,','Regional','Sul.',"Oi","Prado","Thibes","Schimanski","Mauro"]
    text=tex.split('\n')
    if "ONS" in text[1] or "COG" in text[1] or "CNOS" in text[1]:
        a=text[1].replace("Locutor 1:","").replace("Locutor 2:","").replace(".","").replace(",","")
        a= pattern.sub('', a).replace("\n","")
        b=a.split(" ")
        b = list(filter(None, b))
        c=''
        for i in range(0,len(b)): 
                if b[i][0].isupper():
                    if b[i] not in vetor:
                        c=b[i]
        return c
    if "ONS" in text[2] or "COG" in text[2] or "CNOS" in text[2]:
        a=text[2].replace("Locutor 1:","").replace("Locutor 2:","").replace(".","").replace(",","")
        a= pattern.sub('', a).replace("\n","")
        b=a.split(" ")
        b = list(filter(None, b))
        c=''
        for i in range(0,len(b)): 
            if b[i][0].isupper():
                if b[i] not in vetor:
                    c=b[i]
        return c

def get_tags(text):
    ret=[]
    stext=preprocess(text)
    c=classificacao(stext)
    if(c[0]>0):
        t=tensao(stext)
        if t[3]>0:
            if sum([dfl.SequenceMatcher(None,item,"máximo").ratio()>0.75 for item in stext])>0:
                ret.append("Aumento para tensão máxima")
            else:
                ret.append("Aumento de tensão")
        elif t[4]>0:
            if sum([dfl.SequenceMatcher(None,item,"mínimo").ratio()>0.75 for item in stext])>0:
                ret.append("Redução para tensão mínima")
            else:
                ret.append("Redução de tensão")
        elif t[0]>0:
            if sum([dfl.SequenceMatcher(None,item,"máximo").ratio()>0.75 for item in stext])>0:
                ret.append("Aumento para tensão máxima")
            elif sum([dfl.SequenceMatcher(None,item,"mínimo").ratio()>0.75 for item in stext])>0:
                ret.append("Redução para tensão mínima")
    if(c[1]>0):
        if reverter(stext)[4]>0:
            ret.append("Reversão de unidade em CAG")
        else:
            ret.append("Compensação de gerador")
    if(c[2]>0):
        h=hidro(stext)
        if h[0]>0:
            ret.append("Informação hidrológica")
        if h[2]>0 or hidro(stext)[1]>0:
            ret.append("Informação pluviométrica")
        if h[3]>0:
            ret.append("Informação de nível")
    if(c[3]>0):
        ret.append("Vertimento")
    if(c[4]>0):
        i=interrup(stext)
        if i[1]>0:
            ret.append("Desligamento")
        if i[2]>0 or i[0]>0:
            ret.append("Manutenção de unidade")
        else: ret.append("Ocorrência")
    return ret

def get_complexidade(tex):
    text=preprocess(tex)
    if sum(classificacao(text)[2:])>0:
        return "Complexo"
    else:
        return "Simples"

def get_usinas(text):
    usinas=["salto_santiago","itá","cana_brava","são_salvador","jaguara","umburanas","pampa_sul","jorge_lacerda","estreito","utlc","machadinho","osório","passo_fundo","lages"]
    text2=preprocess(text)
    ret=list(filter(lambda x:x in text2,usinas))
    return [i.upper() for i in ret]

def get_json(metatext):
    data={'Data':list(map(get_data,metatext)),'Requerente':list(map(get_ONS,metatext)),'Tags':list(map(get_tags,metatext)),'Usina':list(map(get_usinas,metatext)),'Complexidade':c5=list(map(get_complexidade,metatext))}
    dfpd=pd.DataFrame(data)
    dfpd.to_json('dados.json',force_ascii=False)




