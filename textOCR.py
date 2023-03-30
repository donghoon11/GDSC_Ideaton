
import cv2
import pytesseract
from PIL import Image
import googletrans

from easyocr import Reader


def tesseract_ocr(path):
    # ocr 실행
    # 아직 정규식 처리 하지 않은 상태여서 특수문자가 리턴값에 들어있을 수 있음.
    image = Image.open(path)

    options = '-l kor+eng --oem 3 --psm 6'
    sentence = pytesseract.image_to_string(image, config=options)
    
    return sentence

def tesseract_ocr_ko(path):
    # ocr 실행
    # 아직 정규식 처리 하지 않은 상태여서 특수문자가 리턴값에 들어있을 수 있음.
    image = Image.open(path)

    options = '-l kor+eng --oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=options)

    translator = googletrans.Translator()
    sentence = translator.translate(text, dest='en', src='ko')
    sentence = sentence.text

    return sentence


def easyocr_ko(path):
    image = Image.open(path)

    langs = ['ko', 'en']
    reader = Reader(lang_list=langs, gpu=True)
    sentence = reader.readtext(image, detail=0)
    sentence = ''.join(sentence)

    # 번역
    translator = googletrans.Translator()
    sentence = translator.translate(sentence, src='ko', dest='en')
    setence = sentence.text

    return sentence

# text = easyocr_kor('/content/rabbit.png')
# print(text.text)
# print(type(text))
