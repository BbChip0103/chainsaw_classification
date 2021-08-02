import requests
import json
import re

def get_video_list(url, count):
    req_num = count//500 + 1
    result = []

    for i in range(1, req_num+1):
        res = requests.get(url+str(i)+'.js')
        video_list = json.loads(res.text[2:-1])
        result += video_list
        
    return result

def get_video_info(url):
    res = requests.get(url)

    # populateThumbnails('https:\/\/storage.googleapis.com\/audioset_website_data\/youtube_corpus\/v1\/balanced_train\/', 'chainsaw',  60 );
    inform = re.search('populateThumbnails\((.+?)\)', res.text)
    inform = '['+inform[1]+']'
    inform = inform.replace('\'', '\"')
    [base_url, end_point, count] = json.loads(inform)
    return base_url+end_point+'/', count

def main():
    target_url = 'http://research.google.com/audioset//unbalanced_train/chainsaw.html'
    base_url, count = get_video_info(target_url)
    video_list = get_video_list(base_url, count)
    print(video_list[:20])
    print(len(video_list))

if __name__=='__main__':
    main()
