import torch
import numpy as np
from scipy.io.wavfile import write
from IPython.display import Audio

tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2')
tacotron2 = tacotron2.to('cuda')
tacotron2.eval ()

waveglow = torch.hub.load('nvidia/DeepLearningExamples:torchhub' , 'nvidia_waveglow')
waveglow = waveglow.remove_weightnorm(waveglow)
waveglow = waveglow.to('cuda')
waveglow.eval()

text = "hello, i hope i sound nice in jesus name!"

sequence = np.array(tacotron2.text_to_sequence(text, ['english_cleaners'])) [None, :]
sequence = torch.from_numpy(sequence).to(device = 'cuda', dtype=torch.int64)

with torch.no_grad():
    _, mel, _, _ = tacotron2.infer(sequence)
    audio = waveglow.infer(mel)
    
audio_numpy = audio[0].data.cpu().numpy()
rate = 22050
Audio(audio_numpy,rate=rate)
