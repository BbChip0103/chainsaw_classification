import requests
from bs4 import BeautifulSoup
import json

import os
import subprocess
from multiprocessing import Pool
from functools import partial
import pytube

def get_contents_by_playlist(playlist_code):
    def more_playlist(url, content_list):
        res = requests.get(url)
        res = json.loads(res.text)
        soup = BeautifulSoup(res['content_html'], 'lxml')
        contents = soup.select('tr.pl-video.yt-uix-tile')
        contents = [content['data-video-id'] for content in contents]
        # contents = [content['data-title'] for content in contents]
        content_list += contents

        soup = BeautifulSoup(res['load_more_widget_html'], 'lxml')
        more_button = soup.find('button', class_='load-more-button')
        if more_button is not None:
            url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
            return more_playlist(url, content_list)
        else:
            return content_list

    url = 'https://www.youtube.com/playlist'
    querystring = {'list':playlist_code, 'app':'desktop'}
    res = requests.get(url, params=querystring)

    soup = BeautifulSoup(res.text, 'lxml')
    contents = soup.select('table.pl-video-table > tbody > tr')
    contents = [content['data-video-id'] for content in contents]
    # contents = [content['data-title'] for content in contents]

    more_button = soup.find('button', class_='load-more-button')
    if more_button is not None:
        url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
        return more_playlist(url, contents)
    else:
        return contents

def get_contents_by_username(username):
    def more_playlist(url, content_list):
        res = requests.get(url)
        res = json.loads(res.text)
        soup = BeautifulSoup(res['content_html'], 'lxml')
        contents = soup.select('div.yt-lockup-video')
        contents = [content['data-context-item-id'] for content in contents]
        content_list += contents

        soup = BeautifulSoup(res['load_more_widget_html'], 'lxml')
        more_button = soup.find('button', class_='load-more-button')
        if more_button is not None:
            url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
            return more_playlist(url, content_list)
        else:
            return content_list

    url = 'https://www.youtube.com/user/'+username+'/videos'
    querystring = {'flow':'grid', 'view':'0','sort':'da'}
    res = requests.get(url, params=querystring)

    soup = BeautifulSoup(res.text, 'lxml')
    contents = soup.select('div.yt-lockup-video')
    contents = [content['data-context-item-id'] for content in contents]
    # contents = [content['data-title'] for content in contents]

    more_button = soup.find('button', class_='load-more-button')
    if more_button is not None:
        url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
        return more_playlist(url, contents)
    else:
        return contents

def get_playlists_by_username(username, include_title=False):
    def more_playlist(url, playlists):
        res = requests.get(url)
        res = json.loads(res.text)
        soup = BeautifulSoup(res['content_html'], 'lxml')
        contents = soup.select('h3.yt-lockup-title > a')
        if include_title:
            contents = [(content.getText(), content['href'].replace('/playlist?list=', ''))
                        for content in contents]
        else:
            contents = [content['href'].replace('/playlist?list=', '') for content in contents]
        playlists += contents

        soup = BeautifulSoup(res['load_more_widget_html'], 'lxml')
        more_button = soup.find('button', class_='load-more-button')
        if more_button is not None:
            url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
            return more_playlist(url, playlists)
        else:
            return playlists

    url = 'https://www.youtube.com/user/'+username+'/playlists'
    querystring = {'flow':'grid', 'view':'1','sort':'da'}
    res = requests.get(url, params=querystring)

    soup = BeautifulSoup(res.text, 'lxml')
    contents = soup.select('h3.yt-lockup-title > a')
    if include_title:
        playlists = [(content.getText(), content['href'].replace('/playlist?list=', ''))
                    for content in contents]
    else:
        playlists = [content['href'].replace('/playlist?list=', '') for content in contents]
    # print(playlists)

    more_button = soup.find('button', class_='load-more-button')
    if more_button is not None:
        url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
        return more_playlist(url, playlists)
    else:
        return playlists

def get_playlists_by_channel(channel_id, include_title=False):
    def more_playlist(url, playlists):
        res = requests.get(url)
        res = json.loads(res.text)
        soup = BeautifulSoup(res['content_html'], 'lxml')
        contents = soup.select('h3.yt-lockup-title > a')
        if include_title:
            contents = [(content.getText(), content['href'].replace('/playlist?list=', ''))
                        for content in contents]
        else:
            contents = [content['href'].replace('/playlist?list=', '') for content in contents]
        playlists += contents

        soup = BeautifulSoup(res['load_more_widget_html'], 'lxml')
        more_button = soup.find('button', class_='load-more-button')
        if more_button is not None:
            url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
            return more_playlist(url, playlists)
        else:
            return playlists

    url = 'https://www.youtube.com/channel/'+channel_id+'/playlists'
    querystring = {'flow':'grid', 'view':'1','sort':'da'}
    res = requests.get(url, params=querystring)

    soup = BeautifulSoup(res.text, 'lxml')
    contents = soup.select('h3.yt-lockup-title > a')
    if include_title:
        playlists = [(content.getText(), content['href'].replace('/playlist?list=', ''))
                    for content in contents]
    else:
        playlists = [content['href'].replace('/playlist?list=', '') for content in contents]
    # print(playlists)

    more_button = soup.find('button', class_='load-more-button')
    if more_button is not None:
        url = 'https://www.youtube.com'+more_button['data-uix-load-more-href']
        return more_playlist(url, playlists)
    else:
        return playlists

def download_audio(content_id, output_path, include_subtitle=False):
    content_url = 'https://www.youtube.com/watch?v={0}'.format(content_id)

    try:
        yt = pytube.YouTube(content_url) #다운받을 동영상 URL 지정
    except Exception as e:
        print('Error :', e)
        return False

    vids= yt.streams.filter(only_audio=True).all()

    # #영상 형식 리스트 확인
    # for i, name in enumerate(vids):
    #     print('{0} : {1}'.format(i, name))
    #
    # vnum = int(input("다운 받을 화질은? "))
    vnum = 0

    if include_subtitle:
        # is exist korea subtitle ?
        if yt.captions.get_by_language_code('ko') is None : return False
        if yt.captions.get_by_language_code('ko').name.find('자동 생성됨') < 0:
            return False

    os.makedirs(output_path, exist_ok=True)
    # print(yt.title, 'Download Start.')
    vids[vnum].download(output_path) #다운로드 수행

    if include_subtitle:
        # print(yt.captions.all())
        caption = yt.captions.get_by_language_code('ko')

        try:
            filename = os.path.splitext(vids[vnum].default_filename)[0]
            with open(output_path+filename+'.txt', 'w', encoding='utf-8') as f:
                f.write(caption.xml_captions)
        except Exception as e:
            print('Error :', e)
            # print('File Name :', output_path+vids[vnum].default_filename)
            return False

    return True

def download_video(content_id, output_path):
    content_url = 'https://www.youtube.com/watch?v={0}'.format(content_id)

    try:
        yt = pytube.YouTube(content_url) 
        vnum = 0
        os.makedirs(output_path, exist_ok=True)
        vids= yt.streams.filter(file_extension='mp4').all()
        vids[vnum].download(output_path)
    except Exception as e:
        print('Error :', e)
        return False

    return True

def cvt_video_to_wav(input, output_path):
    os.makedirs(output_path, exist_ok=True)
    output = output_path+os.path.splitext(os.path.basename(input))[0]+'.wav'
    # print(input, '변환 시작.')
    # ffmpeg_path = 'C:/ffmpeg/bin/'
    # subprocess.call([ffmpeg_path+'ffmpeg', '-i', input, '-f', 'f32be', '-ar', '44100', output])
    subprocess.call(['ffmpeg', '-i', input, output])
    # print(input, '변환 완료!')

    return True

def test2():
    output_path = 'test/'
    # content_list = get_contents_by_username('cbs15min')
    playlists = get_playlists_by_username('AngeloYeo', include_title=True)
    # print(playlists[:20])
    # print(len(playlists))

    for title, playlist_id in playlists:
        content_list = get_contents_by_playlist(playlist_id)
        title_output_path = output_path + title + '/'
        # get_video = partial(download_video, output_path=title_output_path)
        download_files = partial(download_audio, output_path=output_path, include_subtitle=False)

        pool = Pool(processes=16)
        pool.map(download_files, content_list)
        pool.close()
        pool.join()

def test():
    output_path = 'test/'

    # content_list = get_contents_by_playlist('PLI6bDyv0uVQBDIuRCrzQGFF2WaXIXvjb5')
    # all_content_list = get_contents_by_username('cbs15min')
    # content_list = [content for content in all_content_list if content not in content_list]

    content_list = get_contents_by_username('AngeloYeo')

    ### test env : i3 dualcore 4thread ###
    download_files = partial(download_audio, output_path=output_path, include_subtitle=True)
    pool = Pool(processes=16)
    pool.map(download_files, content_list)
    pool.close()
    pool.join()

    # ### convert mp4 to wav(law format) ###
    # wavfile_list = [output_path+filename for filename in os.listdir(output_path) if filename.endswith('.mp4')]
    #
    # cvt_video = partial(cvt_video_to_wav, output_path=output_path)
    # pool = Pool(processes=4)
    # pool.map(cvt_video, wavfile_list)
    # pool.close()
    # pool.join()

if __name__=='__main__':
    test2()
