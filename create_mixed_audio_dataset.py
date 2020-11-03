import argparse
import os
import random
from tqdm import tqdm

from create_mixed_audio_file import create_mixed_audio 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean_dir', type=str, required=True)
    parser.add_argument('--noise_dir', type=str, required=True)
    parser.add_argument('--output_mixed_dir', type=str, default='', required=True)
    parser.add_argument('--output_clean_dir', type=str, default='')
    parser.add_argument('--snr', type=float, default='', required=True)
    args = parser.parse_args()
    return args

def get_paths(path):
    result = []

    def recursive_file_check(path):
        if os.path.isdir(path):
            # directoryだったら中のファイルに対して再帰的にこの関数を実行
            files = os.listdir(path)
            for file in files:
                recursive_file_check(path + "/" + file)
        else:
            _, ext = os.path.splitext(path)
            if (ext == '.wav'):
                result.append(path)
    
    recursive_file_check(path)

    return result

def get_filename(path):
    return os.path.basename(path)

def get_output_path(clean_path, output_dir):
    return output_dir + '/' + get_filename(clean_path)

if __name__ == '__main__':
    args = get_args()
    
    clean_paths = get_paths(args.clean_dir)
    noise_paths = get_paths(args.noise_dir)
    
    for clean_path in tqdm(clean_paths):
        noise_path = random.choice(noise_paths)
        output_path = get_output_path(clean_path, args.output_mixed_dir)
        create_mixed_audio(clean_path, noise_path, output_path, args.snr)