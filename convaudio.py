import subprocess
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
import time

# Configure to log to stdout
logging.basicConfig(format='%(asctime)s\t%(threadName)s\t%(message)s',
                    level=logging.INFO)

def conv_audio(infile, outfile, delete):
    logging.info("  [......]: %s -> %s", infile, outfile)
    r = subprocess.run(args=['ffmpeg.exe', '-hide_banner', '-y', '-i', infile,
                        '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', outfile],
                        capture_output=True)
    logging.info("  [%6s]: %s -> %s", 'done' if r.returncode== 0 else 'failed', infile, outfile)
    if r.returncode == 0:
        os.remove(infile)
        logging.info("            removed %s", infile)

def submit_work(executor, indir, outdir, outtype, delete):
    for dirpath, _, filenames in os.walk(indir):
        for f in filenames:
            executor.submit(conv_audio, os.path.join(dirpath, f), os.path.join(outdir, f'{os.path.splitext(f)[0]}.{outtype}'), delete)

def main(indir, outdir, outtype, delete):
    logging.info('[> %s]: %s -> %s', outtype, indir, outdir)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=os.cpu_count(), thread_name_prefix="Converter") as executor:
        submit_work(executor, indir, outdir, outtype, delete)

    logging.info('[%.2fs]: %s -> %s', time.perf_counter()-start, indir, outdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert audio files to a specific audio format concurrently with multiple processes")
    parser.add_argument('-i', '--indir', default=".", type=str, help="convert all media files under this directory")
    parser.add_argument('-o', '--outdir', default=".", type=str, help="directory to save output audio files")
    parser.add_argument('-t', '--type', default='mp3', type=str, help="output audio file type")
    parser.add_argument('-d', '--delete', default=False, type=bool, help="whether to delete original file after successfully converted")
    
    args = parser.parse_args()

    main(args.indir, args.outdir, args.type, args.delete)
