import librosa
import librosa.display
import matplotlib.pyplot as plt

UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/noise/static/upload/'

def plot(path, name):
    #저장경로, 이름 설정
    png_path = f"{UPLOAD_FOLDER}{name.split('.')[0]}.png"
    png_name = f"{name.split('.')[0]}.png"
    y, sr = librosa.load(path)
    librosa.display.waveplot(y, sr, alpha = 0.5)
    plt.xlabel("time(s)")
    plt.grid()
    plt.savefig(png_path)
    return png_name
