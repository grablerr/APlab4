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

def filter_by_word_count(dataframe, word_count):
    return dataframe[dataframe['Количество слов'] <= word_count]

def filter_by_stars(dataframe, label):
    dataframe['Количество звёзд'] = dataframe['Количество звёзд'].astype(str)
    if label in ['1', '2', '3', '4', '5']:
        filtered_df = dataframe[dataframe['Количество звёзд'] == label]
    elif label == "other":
        filtered_df = dataframe[~dataframe['Количество звёзд'].isin(['1', '2', '3', '4', '5'])]
    else:
        raise ValueError("Неверное значение для метки класса. Допустимые значения: от 1 до 5 и 'other'")
    return filtered_df

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

numeric_info1 = df[['Количество звёзд']].describe()
print(numeric_info1)

numeric_info2 = df[['Количество слов']].describe()
print(numeric_info2)

df.to_csv('data.csv', index=False)

filtered_df = filter_by_word_count(df,20)
print(filtered_df)
filtered_df.to_csv('data_of_filtered_df_by_words.csv', index=False)

filterd_df_by_stars = filter_by_stars(df, "1")
print(filterd_df_by_stars)
filterd_df_by_stars.to_csv('data_filterd_df_by_stars.csv', index=False)