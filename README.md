# chainsaw_classification

### Data Crawling
- 2_1_sound_scrapping.py : 구글 오디오셋 주소에서 전기톱 영상에 해당하는 ID를 뽑아오는 코드.
이런 식으로 파싱하여 chainsaw_data.csv와 같은 형태로 저장한다.
- 2_2_pymytube.py : 유튜브 동영상을 wav로 바꾸려고 내가 예전에 짜놨던 오픈소스. 유튜브 영상이 잘못된 경우가 많기 때문에 직접 다운받아서 chainsaw_data.csv와 비교해본 후 arranged_chainsaw_data.csv로 만든다.
약 400여개의 링크가 없어졌다는 것을 알 수 있다.

### Data Cleaning
- 3_1_make_timetable.py : Audio Activity Detection을 위해서 AudiTok라는 오픈소스 갖다 씀. 이걸로 소리가 커지는 구간을 디텍팅해서 저장함.
- AudiTok/ : AAD 오픈소스인데, Mean Squere 값을 기준으로 Activity Detection을 하는 원리.
- 3_2_make_chainsaw_data.py : 3_1에서 뽑은 구간을 기준으로 wav파일과 csv파일 생성. 해당 결과는 ESC-50-master/wav_chainsaw_5sec에 저장되며, 약 2200여개의 전기톱 데이터가 구축됨.
- ESC-50-master/ : 자연적으로 날 수 있는 소리(ex. cat, tree, wind, rain, etc)를 쓰기 위해서 캐글에서 받은 데이터.
- 3_3_split_data.ipynb : 학습을 위해서 Train과 Validation, Test 셋을 나누는 코드. ESC 데이터가 총 1200개이기 때문에, 전기톱 데이터도 1200개만 사용함.

### Modeling
- chainsaw_classification_machine_learning_1200.ipynb : 최적의 인풋과 최적의 머신러닝 모델을 찾아내는 과정이 담겨있는 코드. 
- chainsaw_classification_AlexNet_base.ipynb : 딥러닝 성능을 테스트하기 위해, 알렉스넷 기반의 1D CNN 을 만들어서 테스트 해 본 코드.
- chainsaw_classification_SampleCNN.ipynb : 딥러닝이 성능이 괜찮게 뽑히자, 좀 유명한 1D-CNN 모델을 가져다 써 본 코드.
- presentation_demo.ipynb : 시연을 위한 데모