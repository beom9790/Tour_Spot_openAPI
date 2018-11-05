import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from Tour_Data import *

## matplotlib 그래프에 한글 폰트 적용 코드
path = './malgun.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()

plt.rc('font', family=font_name)

def Make_Graph():
    tour_spot = Combination_Tourist()   ## {관광지:방문객수} 딕셔너리 반환
    spots = []                          ## 그래프에 사용할 관광지명을 담을 리스트
    number_tourist = []                 ## 그래프에 사용할 방문객수를 담을 리스트
    for per_spot, per_tourist in tour_spot.items():
        spots.append(per_spot)
        number_tourist.append(per_tourist)

    spot_index = range(len(spots))

    ## ggplot 스타일시트를 사용하여 R용 시각화 패키지 ggplot2의 스타일을 재현
    plt.style.use('ggplot')

    fig = plt.figure()             ## 그림을 만들고
    ax1 = fig.add_subplot(1,1,1)   ## 하위 그래프를 추가 - 1,1,1 : ax1이 유일한(1행, 1열, 1개) 하위 그래프임을 의미

    ## Y축 : spot_index, X축 : number_tourist, 막대가 Y축 레이블의 중앙에 위치하도록 지정
    ax1.barh(spot_index, number_tourist, align='center', color='darkblue')  ## 수평 막대 그래프 생성
    ax1.xaxis.set_ticks_position('bottom')  ## X축 눈금 위치를 아래쪽에 xlabel 위치
    ax1.yaxis.set_ticks_position('left')    ## Y축 눈금 위치를 왼쪽에 ylabel 위치

    ## 막대의 눈금 레이블을 인덱스에서 실제 이름으로 변경, rotation=1은 눈금 레이블을 수평으로 지정
    plt.yticks(spot_index, spots, rotation=1, fontsize='small')

    ## X축 레이블, Y축 레이블, 그래프 제목 추가
    plt.xlabel('방문객 수')
    plt.ylabel('관광지')
    plt.title('서울특별시 관광지 방문객')

    plt.savefig('%s_관광지입장정보_%d_%d.png' % (sido, nStartYear, nEndYear - 1), dpi=400, bbox_inches='tight')
    plt.show()  ## 지금까지 만든 그림을 새 창에 출력

    print('%s_관광지입장정보_%d_%d.png SAVED' % (sido, nStartYear, nEndYear - 1))