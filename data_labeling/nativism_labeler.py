# Run "python nativism_labeler.py label"

import nltk.data
import argparse
import os
import csv

parser = argparse.ArgumentParser(description="Let's label some speeches. Directory must be of the format provided.")
parser.add_argument("folder", help="contains speeches and data folders")
args = parser.parse_args()

speeches = f"{args.folder}/speeches"
data_folder = f"{args.folder}/labeled_data"
nativist = open(f"{data_folder}/nativist.txt", 'w')
not_nativist = open(f"{data_folder}/not_nativist.txt", 'w')
unknown = open(f"{data_folder}/unknown.txt", 'w')
already_labeled = open(f"{data_folder}/already_labeled.txt", 'r+')
current_info = open(f"{data_folder}/current_info.txt", 'r+')
master_csv = open(f"{data_folder}/master_list.csv", 'r+')
master_writer = csv.writer(master_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# First, read current speech name and sentence number from current_info.txt
info = current_info.readlines()[-1].split()
current_sentence = info[-1]
current_speech = info[0]
print(f"Currently labeling {info[len(info)-2]}, beginning from sentence {current_sentence}")

# Go through files in speech_folder, and get uncompleted ones.
labeled_speeches = already_labeled.read().split()
print(f"Already labeled: {labeled_speeches}")

unlabeled_speeches = []
for filename in os.listdir(speeches):
    if filename.endswith(".txt"):
        filename = os.path.join(speeches, filename)
        if (filename not in labeled_speeches) and (filename != current_speech):
            unlabeled_speeches.append(filename)
print(f"Unlabeled: {unlabeled_speeches}")

# Label current speech

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
if current_speech != "NA":
    print(f"resuming {current_speech}...")
    fp = open(current_speech)
    speech = tokenizer.tokenize(fp.read())
    for number, sentence in enumerate(speech):
        if number > int(current_sentence):
            print(f"'{sentence}'")
            inp = input("Nativist (1) or Not-nativist (0)? ")
            if inp == "close" or not inp.isdigit():
                nativist.close()
                not_nativist.close()
                unknown.close()
                already_labeled.close()
                current_info.close()
                raise ValueError
            des = int(inp)
            current_info.write(f" {str(number)}")
            if des != 1 and des != 0:
                print("Invalid entry, adding to unknown.txt")
                unknown.write(f"{sentence}\n")
                continue
            if des == 1:
                nativist.write(f"{sentence}\n")
                master_writer.writerow([sentence, 1])
            elif des == 0:
                not_nativist.write(f"{sentence}\n")
                master_writer.writerow([sentence, 0])

    print("SPEECH DONE")
    already_labeled.write(f" {current_speech}")
    fp.close()

# Continue to new speeches
for sp in unlabeled_speeches:
    print(f"Starting {sp}...")
    fp = open(sp)
    current_info.write(f"\n{sp} 0")
    speech = tokenizer.tokenize(fp.read())
    for number, sentence in enumerate(speech):
        if number > int(current_sentence):
            print(f"'{sentence}'")
            inp = input("Nativist (1) or Not-nativist (0)? ")
            if inp == "close" or not inp.isdigit():
                nativist.close()
                not_nativist.close()
                unknown.close()
                already_labeled.close()
                current_info.close()
                raise ValueError
            des = int(inp)
            current_info.write(f" {str(number)}")
            if des != 1 and des != 0:
                print("Invalid entry, adding to unknown.txt")
                unknown.write(f"{sentence}\n")
                continue
            if des == 1:
                nativist.write(f"{sentence}\n")
                master_writer.writerow([sentence, 1])
            elif des == 0:
                not_nativist.write(f"{sentence}\n")
                master_writer.writerow([sentence, 0])

    print("SPEECH DONE")
    already_labeled.write(f" {sp}")
    fp.close()

nativist.close()
not_nativist.close()
unknown.close()
already_labeled.close()
current_info.close()
