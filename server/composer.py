import re

import numpy as np
import pretty_midi
from transformers import AutoTokenizer, AutoModel


ckpt_path = "Mar2Ding/songcomposer_sft"
cache_folder= '../models/songcomposer_sft'

def load_models():
    tokenizer = AutoTokenizer.from_pretrained(ckpt_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(cache_folder, trust_remote_code=True).half().cuda()

    return tokenizer, model

def parse_generated_text(text):
    m1 = re.search(r'The first line.*', text)
    parsed_text = m1.group(0) if m1 else ""
    parsed_text = parsed_text.replace("<eop> [UNUSED_TOKEN_145]", '')
    # m2 = re.search(r'^.*(?=(\.[The first line]))', parsed_text)
    # parsed_text = m2.group(0)
    # print(m2.group(0))

    return parsed_text.strip()

def reverse_log_float(x, bins=512):
    if x == 79:
        return 0
    eps = 1
    x_min = np.log(eps-0.3)
    x_max = np.log(6+eps)
    x = x * (x_max - x_min)/(bins-1) + x_min
    x = np.exp(x) - eps
    return float("{:.3f}".format(x))
    
def tuple2dict(line):
    order_string = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    line = line.replace(" ", "")
    line = line.replace("\n", "")
    line = re.sub(r'\. |\.', '', line)
    # line = re.sub(r'The\d+line:', ' |', line)
    for string in order_string:
        line = line.replace(f'The{string}line:', ' |')
    special_pattern = r'<(.*?)>'
    song = {'lyrics':[], 'notes':[], 'notes_duration':[], 'rest_duration':[], 'pitch':[], 'notes_dict': [], 'rest_dict': []}
     
    for item in line.split('|')[1:]:
        x = item.split(',')
        notes = re.findall(special_pattern,x[1])
        note_ds = re.findall(special_pattern,x[2])
        rest_d = re.findall(special_pattern,x[3])[0]
        assert len(notes)== len(note_ds), f"notes:{'|'.join(notes)}, note_ds:{'|'.join(note_ds)}"
        for i in range(len(notes)):
            if i == 0:
                song['lyrics'].append(x[0])
            else:
                song['lyrics'].append('-')
            song['notes'].append(notes[i])
            song['pitch'].append(int(pretty_midi.note_name_to_number(notes[i])))
            song['notes_duration'].append(reverse_log_float(int(note_ds[i])))
            song['notes_dict'].append(int(note_ds[i]))
            if i == len(notes)-1:
                song['rest_duration'].append(reverse_log_float(int(rest_d)))
                song['rest_dict'].append(int(rest_d))
            else:
                song['rest_duration'].append(0)
                song['rest_dict'].append(0)
    return song

def dict2midi(song):
    # new_midi = pretty_midi.PrettyMIDI(charset="utf-8")#
    new_midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    # print(len(song["notes"]))
    current_time = 0  # Time since the beginning of the song, in seconds
    # pitch = []
    for i in range(0, len(song["notes"])):
        #add notes
        notes_duration = song["notes_duration"][i]
        note_obj = pretty_midi.Note(velocity=100, pitch=int(pretty_midi.note_name_to_number(song["notes"][i])), start=current_time,
                                end=current_time + notes_duration)
        instrument.notes.append(note_obj)
        #add lyrics
        # lyric_event = pretty_midi.Lyric(text=str(song["lyrics"][i])+ "\0", time=current_time)
        # new_midi.lyrics.append(lyric_event)
        current_time +=  notes_duration + song["rest_duration"][i]# Update of the time
   
    new_midi.instruments.append(instrument)
    lyrics = ' '.join(song["lyrics"])
    return new_midi, lyrics

def gen_midi(line, file_name):
    song  = tuple2dict(line)
    #song['lyrics'] = ['I','-','you','-','I','-','you','-','I','-','you','-','he','-']
    new_midi, lyrics = dict2midi(song)

    # save midi file and lyric text
    new_midi.write(file_name+'.mid')

    with open(file_name+'.txt', "w") as file:
        file.write(lyrics)
    print(f'midi saved at ~/{file_name}.mid, lyrics saved at ~/{file_name}.txt')


def generate(prompt, model, tokenizer):
    result = model.inference(prompt, tokenizer)
    selected_song = parse_generated_text(result[0])

    gen_midi(selected_song, 'christmas')

    return result