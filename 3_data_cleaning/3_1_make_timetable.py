import os

if __name__=='__main__':
    wav_path = 'wav/'
    output_path = wav_path+'result/'

    wav_list = [wav_path+fname for fname in os.listdir(wav_path) if fname.endswith('.wav')]

    os.makedirs(output_path, exist_ok=True)
    for wav_name in wav_list:
        basename = os.path.basename(wav_name)
        name = os.path.splitext(basename)[0]
        os.system( '{} > {}'.format(
                    'auditok -i {} -n 5 -m 10 -d True -s 0.2 -e 70 --printf '.format(wav_name)+'\"{start}\"',
                    output_path+name+'.txt'
                    )
                )
