import argparse
import html2text
import os
import re
import string


base_folder = '/home/ilya/hard_drive/mirror/lib.ru/files/full/extracted/'


def get_text(input_file_name):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    text_maker.unicode_snob = True
    text_maker.body_width = 0

    with open(input_file_name, 'r') as content_file:
        return text_maker.handle(content_file.read())


def convert_text(text):
    exclude = set(string.punctuation)
    exclude.remove('.')
    exclude.remove('!')
    exclude.remove('?')
    text = text.replace('--', '.').replace(';', '.')
    text = text.lower()
    converted = ''.join(ch for ch in text if ch not in exclude)
    converted = converted.splitlines()
    if 'примечания' in converted:
        converted = converted[:converted.index('примечания')]
        print('Got ya!')
    else:
        converted = converted[:int(len(converted) * .7)]
        print('No luck. Take .7 of text')

    converted = [s for s in converted if len(s) > 0]
    converted = converted[20::]
    return ' '.join(converted)


def is_cyrillic(sym):
    return 'а' <= sym <= 'я' or sym == 'ё'


def split_sentences(converted_text):
    by_sant = re.split('[.!?]+', converted_text)
    by_sant = [s.strip() for s in by_sant if len(s) > 0]
    by_sant = [''.join(sym for sym in s if is_cyrillic(sym) or sym == ' ') for s in by_sant]
    return [' '.join(re.split('\W+', s)) for s in by_sant]


def convert2lines(input_file_name, dest_file_name):
    text = get_text(input_file_name)
    converted_text = convert_text(text)
    sentences = split_sentences(converted_text)
    with open(dest_file_name, 'a') as f:
        for sentence in sentences:
            s = sentence.strip()
            if len(s) > 0:
                print(s, file=f)


def main():
    parser = argparse.ArgumentParser(description='Process list of files.')
    parser.add_argument('-d', action='store', dest='destination_file',
                        help='Destination file name')
    parser.add_argument('input_files', nargs='+',
                        help='File names to process')

    args = parser.parse_args()
    for input_file_name in args.input_files:
        print('Processing: {}'.format(input_file_name))
        convert2lines(os.path.join(base_folder, input_file_name), args.destination_file)

    print('All done!')


main()


# python3 ./text_converter.py -d ./converted pushkin_a_s-text_0030.fb2
# pushkin_a_s-text_0170.fb2 pushkin_a_s-text_1836_poe.fb2
# pushkin_a_s-text_0040.fb2 pushkin_a_s-text_0422.fb2 pushkin_a_s-text_0425.fb2
# pushkin_a_s-text_0430.fb2 pushkin_a_s-text_0426.fb2
