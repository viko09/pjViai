import os
import mido
import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt('testLux.csv', delimiter=',', skiprows=1)

# Extract time and lux values
time = data[:, 0]
lux = data[:, 1]

# Plot lux values
plt.plot(time, lux)
plt.xlabel('Time')
plt.ylabel('Lux')
plt.title('Lux Values over Time')
plt.grid()
# Save the plot as an image file
plt.savefig('gLux.png')
plt.show()

# Create MIDI file
midi_file = mido.MidiFile()
track = mido.MidiTrack()
midi_file.tracks.append(track)

# Set tempo
bpm = 3600*10
track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))

# Set time signature
time_signature = (4, 4)
numerator, denominator = time_signature
clocks_per_click = 2
notated_32nd_notes_per_beat = 8
track.append(mido.MetaMessage('time_signature', numerator=numerator, denominator=denominator,
                              clocks_per_click=clocks_per_click,
                              notated_32nd_notes_per_beat=notated_32nd_notes_per_beat))

# Set instrument
instrument = 101  # acoustic grand piano
program_change = mido.Message('program_change', program=instrument, time=0)
track.append(program_change)

# Convert data to MIDI notes
max_value = np.max(data[:, 1])
min_value = np.min(data[:, 1])
range_value = max_value - min_value
notes = []
for row in data:
    # Map lux values to MIDI note values (60 is middle C)
    value = row[1]
    note = int(np.interp(value, [min_value, max_value], [0, 127]))
    notes.append(note)

# Add notes to MIDI file
note_duration = 0.360  # in seconds
ticks_per_beat = midi_file.ticks_per_beat
print(enumerate(notes))
for i, note in enumerate(notes):
    print(i)
    time = i * note_duration
    note_on = mido.Message('note_on', note=note, velocity=127, time=int(time * ticks_per_beat))
    track.append(note_on)
    note_off = mido.Message('note_off', note=note, velocity=127, time=int(note_duration * ticks_per_beat))
    track.append(note_off)

# Save MIDI file
midi_file.save('luxFinal.mid')

# Play MIDI file using timidity
# os.system("timidity lux.mid")
os.system("rm lux_ghostly.mp3")
# ~ os.system("timidity -Ow -A120 -EFreverb=0.8 -s 10 lux.mid -o - | ffmpeg -i - -filter:a "atempo=2.0" -acodec
# libmp3lame -ab 64k lux10.mp3") ~ command = 'timidity -Ow -A120 -EFreverb=0.8 -s 10 lux.mid -o - | sox - -p reverb
# 80 echo 0.8 0.5 5 0.4 | ffmpeg -i - -acodec libmp3lame -ab 64k lux_ghostly.mp3' ~ command = 'timidity -Ow -A120
# -EFreverb=0.8 -s 10 lux.mid -o - | ffmpeg -i - -filter:a "atempo=2.0" -acodec libmp3lame -ab 64k lux10.mp3'

# command = 'timidity -Ow -A120 -EFreverb=0.8 -EFchorus=0.8,0.7,130 -EFflanger=0.8,0.65,0.5 luxFinal.mid -o - |
# ffmpeg ' \ '-i - ' \ '-acodec libmp3lame -ab 64k lux_ghostly.mp3'
command = 'timidity '
# ~ command = 'timidity -Ow -A120 -EFreverb=0.8 -EFchorus=0.8,0.7,130 -EFflanger=0.8,0.65,0.5 lux.mid -o - | ffmpeg
# -i - -af "volume=19dB" -acodec libmp3lame -ab 64k lux_ghostly.mp3'
os.system(command)
# ~ os.system("smplayer lux_ghostly.mp3")
