import pandas as pd
import os
import nltk
import re

def count_words(text):
    words = nltk.word_tokenize(text)
    words_only = [word for word in words if re.match(r"^\w+$", word)]
    return len(words_only)

def read_review(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) >= 4:
            review_text = ''.join(line.rstrip() for line in lines[3:])
            return review_text.strip()
        else:
            return None

root_folder = 'dataset'

data = []

for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                review_text = read_review(file_path)
                data.append({'Количество звёзд': folder, 'Текст рецензии': review_text})

df = pd.DataFrame(data)

df.fillna('ПУСТОЙ ОТЗЫВ', inplace=True)

df['Количество слов'] = df['Текст рецензии'].apply(count_words)

print(df.head())
df.to_csv('data.csv', index=False)