import os
import subprocess
import random

def csv_to_list(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    lines = lines[1:]   # except tagging line
    lines = [line.split('\t') for line in lines]
    return lines

def make_chainsaw_csv(video_dir, origin, output_filename):
    video_list = [filename for filename in os.listdir(video_dir)
                  if filename.endswith('.mp4')]

    inform_list =  csv_to_list(origin)
    inform_list = [line[1:] for line in inform_list]    # excep index
    inform_list = [info for info in inform_list if info[0] in video_list]

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\t'.join(['filename', 'id', 'begin_sec', 'end_sec'])+'\n')
        for info in inform_list:
            f.write('\t'.join(info)+'\n')

def cvt_video_to_wav(input, output, begin=None, end=None):
    output_path = os.path.dirname(output)
    os.makedirs(output_path, exist_ok=True)

    if begin==None or end==None:
        subprocess.call(['ffmpeg', '-i', input, '-ar', '44100', '-ac', '1'
                         , '-threads', '4', '-loglevel', 'error', output])
    else:
        # subprocess.call([ffmpeg_path+'ffmpeg', '-i', input, '-f', 'f32be', '-ar', '44100', output])
        subprocess.call(['ffmpeg', '-i', input, '-ar', '44100', '-ac', '1'
                         , '-ss', str(begin), '-t', str(int(end)-int(begin))
                         , '-threads', '4', '-loglevel', 'error', output])
    return True

def main():
    video_dir = 'video/'
    output_dir = 'wav_chainsaw_5sec/'
    timetable_dir = 'wav_timetable/'

    # make_chainsaw_csv(video_dir, 'chainsaw_data.csv', 'arranged_chainsaw_data.csv')
    # inform_list = csv_to_list('arranged_chainsaw_data.csv')

    # for filename, _, begin, end in inform_list:
    #     cvt_video_to_wav(video_dir+filename, begin, end, output_dir)

    sum = 0

    timetable_filelist = [timetable_dir+file for file in os.listdir(timetable_dir)
                            if file.endswith('.txt')]
    for timetable_name in timetable_filelist:
        with open(timetable_name, 'r') as f:
            timetable_list = [float(timetable) for timetable in f.read().splitlines()]

        if len(timetable_list) > 3:
            timetable_list = random.sample(timetable_list, 3)

        basename = os.path.basename(timetable_name)
        name = os.path.splitext(basename)[0]

        for timetable in timetable_list:
            cvt_video_to_wav(video_dir+name+'.mp4', 
                output_dir+name+'_{}'.format(timetable)+'.wav',
                begin=timetable, end=timetable+5)
            sum+=1

    print('Number of wav:', sum)
    # file_list = [file for file in os.listdir(video_dir) if file.endswith('.mp4')]
    # for filename in file_list:
    #     cvt_video_to_wav(video_dir+filename, output_dir)


if __name__=='__main__':
    main()
