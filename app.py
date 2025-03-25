# app.py
import streamlit as st
import datetime
import pytz
import time
import pandas as pd
from dateutil.relativedelta import relativedelta
from modules import step1_user_setup, step2_install_dependencies
from modules import step3_func
from modules import step4_data
from modules import userParam as param

st.set_page_config(page_title="SmartFeedBin", page_icon="🔔", layout="wide")
# Layout
empty1, Contents1, empty2 = st.columns([0.1,1,0.1])
article1, article2= st.columns(2)

# Constants
DefaultDeltaDate = 25

def initSearchingDate():
    today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()
    date_start = today - datetime.timedelta(days=DefaultDeltaDate) # 25일전
    date_end = today
    st.session_state.searchingDate[0] = date_start
    st.session_state.searchingDate[1] = date_end

def login():
    with st.spinner("Connecting Database..."):
        time.sleep(1)  # 로딩 시뮬레이션
       
    try:        
        # DB 연결 시도
        st.session_state.ConnDB = step3_func.MYSQL_Connect()

    except Exception as e:  #Login Failed
        print(f"An error occurred during user setup: {e}")
        st.session_state.ConnDB = None
        st.session_state.MessageShow = f"<span style='color:red'> {e}</span>"
        
    
    # Download DB
    if st.session_state.ConnDB is None :
        st.error("Database connection failed. Please check your credentials.")
        st.session_state.MessageShow = f"<span style='color:red'> Database connection failed. Please check your credentials. </span>"
        return  # DB 연결 실패 → 로그인 시도 중지
    else:  
        st.session_state.isLogin = True
        st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
        #st.success("Loading Feedbin Data......") 
        st.session_state.MessageShow = None
        initSearchingDate()
        userCheck()


def userCheck():     
    # 입력된 사용자 ID와 비밀번호 가져오기  
    username = st.session_state.userName
    password = st.session_state.password
     
    # 사용자 인증 (DB에서 ID, PW 확인)
    is_valid_user = step3_func.AuthenticateUser(st.session_state.ConnDB, username, password)
        
    if is_valid_user.empty:
            
        st.error("❌ Invalid user ID or password. Please try again.")
        #st.session_state.MessageShow = "<span style='color:red'>Invalid user ID or password.</span>" 
        time.sleep(2)  # 🔹 1초 대기 후 리다이렉트 (UX 개선)
        
        st.session_state.isLogin = False
        st.session_state.userName = None
        if(st.session_state.ConnDB is not None):
            st.session_state.ConnDB.close()
        st.session_state.IsLoad = False
        st.rerun()
            
            
        #st.experimental_rerun()  # 🔹 현재 페이지를 리로드  
        #st.markdown("""
        #    <meta http-equiv="refresh" content="0; url=http://localhost:8501">
        #    """, unsafe_allow_html=True)
            
 
             
def main():
    ## Grobal Variable
    if 'isLogin' not in st.session_state :
        st.session_state.isLogin = False
    if 'MessageShow' not in st.session_state :
        st.session_state.MessageShow = None
    if 'ConnDB' not in st.session_state:
        st.session_state.ConnDB = None
    if 'userName' not in st.session_state:
        st.session_state.userName = None
    if 'mysqlDepthDataAll' not in st.session_state:
        st.session_state.mysqlDepthDataAll = None
    if 'mysqlFeedBinDataAll' not in st.session_state:
        st.session_state.mysqlFeedBinDataAll = None
    if 'dataIndex' not in st.session_state:
        st.session_state.dataIndex = 0
    if 'dataRaw' not in st.session_state:
        st.session_state.dataRaw = None
    if 'dataFiltered' not in st.session_state:
        st.session_state.dataFiltered = None
    if 'dataBound' not in st.session_state:
        st.session_state.dataBound = None
    if 'dataFeedBin' not in st.session_state:
        st.session_state.dataFeedBin = None        
    if 'Option' not in st.session_state:
        st.session_state.Option = None
    if 'IsLoad' not in st.session_state:
        st.session_state.IsLoad = False
    if "selected_code" not in st.session_state:
        st.session_state.selected_code = None
    if 'searchingDate' not in st.session_state:
        st.session_state.searchingDate = [' ']*2
    if 'searchingDateNew' not in st.session_state:
        st.session_state.searchingDateNew = [' ']*2
    if 'centerPos' not in st.session_state:
        st.session_state.centerPos = [0,0]
    if 'zRange' not in st.session_state:
        st.session_state.zRange = [0,10000]

    st.session_state.Debug = True
    strfarm_seq = ""

    ## Event Callback
    def updateSearchingDate(farm_seq, bin_seq):
         
        if 'searchingDateNew' not in st.session_state:
            return
        if 'searchingDate' not in st.session_state:
            return
        print(len(st.session_state.searchingDateNew))
 
        if(len(st.session_state.searchingDateNew) == 2):
            if(st.session_state.searchingDateNew[0] == ' ') : return
            if(st.session_state.searchingDateNew[1] == ' ') : return
            if(st.session_state.searchingDateNew[1] < st.session_state.searchingDateNew[0]):
                dateTemp = st.session_state.searchingDateNew[0]
                st.session_state.searchingDateNew[0] = st.session_state.searchingDateNew[1]
                st.session_state.searchingDateNew[1] = dateTemp

            if((st.session_state.searchingDateNew[0] == st.session_state.searchingDate[0]) and (st.session_state.searchingDateNew[1] == st.session_state.searchingDate[1])):
                return
            else :
                print(st.session_state.searchingDateNew)
                print(st.session_state.searchingDate)
                st.session_state.searchingDate[0] = st.session_state.searchingDateNew[0]
                st.session_state.searchingDate[1] = st.session_state.searchingDateNew[1]
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], farm_seq, bin_seq)
                st.session_state.IsLoad = True
                
         
    def updateCenterPos():
        st.session_state.centerPos[0] = st.session_state.dataCenterX
        st.session_state.centerPos[1] = st.session_state.dataCenterY
        print(st.session_state.centerPos)
        
    
    def on_select_change(): 
        # st.session_state.selected_bin에는 현재 선택된 값이 저장됩니다.
        st.session_state.IsLoad = False  

    ## Side Bar
    st.sidebar.title("CONSTANTEC FEED CHECK \n 3D LiDAR 측정 시스템")
    st.sidebar.text(" ") 
    st.sidebar.text(" ") 


    if(st.session_state.isLogin):
        st.sidebar.text("{}님 안녕하세요.".format(st.session_state.userName))  
        if st.sidebar.button("Logout"):
            st.session_state.isLogin = False
            st.session_state.userName = None
            if(st.session_state.ConnDB is not None):
                st.session_state.ConnDB.close()
            st.session_state.IsLoad = False
            st.rerun()
            
        choice = st.sidebar.radio(" ", ["측정 데이터","측정 데이터(수직)","측정 데이터(무보정)", "기타"])
        
        st.sidebar.text(" ") 
        st.sidebar.text(" ") 
        
        if st.sidebar.button("조회"): 
            initSearchingDate()
            #st.session_state.ConnDB = step3_func.MYSQL_Connect()
            #st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], strfarm_seq)
            #st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
            st.cache_data.clear()
            st.cache_resource.clear()
             
    else:
        choice = st.sidebar.radio(" ", ["Login"])
    
    ## Main Contents
    with empty1:
        st.empty()
    with Contents1:
        
        
        selected_farm = None
        selected_bin = None 
        selected_farm_seq = None
        selected_bin_seq = None
        farm_seq = None
        bin_seq = None
            
        ## Error Message
        if(st.session_state.MessageShow is not None):
            st.markdown(st.session_state.MessageShow, unsafe_allow_html=True)
         
        ## Login First Page
        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("User ID", value="constantec")
            password = st.text_input("Password", value="", type="password", key="password")
            st.session_state.userName = username   
            if st.button("Login", on_click=login):   
                st.rerun()
             
        
        ## 최근 정보를 열람        
        elif choice == "측정 데이터":
              
            
            # 임시 코드 값 설정
            if "selected_code" not in st.session_state:
                st.session_state.selected_code = ""
            
            username = st.session_state.userName
            farm_df = step3_func.MysqlGetFarmNo(st.session_state.ConnDB, username)  #로그인 유저에게 허용된 농장 List를 조회
            bin_df = pd.DataFrame()
                
               
            # Left Side
            with article1:
                
                
                # 농가 선택
                if not farm_df.empty:
                    farm_names = farm_df['farm_nm'].tolist()
                    selected_farm = st.selectbox("농가 선택", farm_names, on_change=on_select_change)  
                    
                if not farm_df.empty and selected_farm:
                    selected_farm_seq = farm_df[farm_df['farm_nm'] == selected_farm]['farm_seq'].iloc[0]
                
                if selected_farm_seq is not None:
                    farm_seq = str(selected_farm_seq)
                else:
                    farm_seq = None
                 
                # 피드빈 선택 
                bin_df = step3_func.MysqlGetFeedcheckNo(st.session_state.ConnDB, farm_seq)  #로그인 유저에게 허용된 농장 List를 조회
                 
                # 피드빈 선택
                if not bin_df.empty:
                    bin_names = bin_df['bin_nm'].tolist()
                    selected_bin = st.selectbox("피드빈 선택", bin_names, on_change=on_select_change)
                 
                if not bin_df.empty and selected_bin:
                    selected_bin_seq = bin_df[bin_df['bin_nm'] == selected_bin]['bin_seq'].iloc[0]
                else:
                    selected_bin_seq = None    
            
                if selected_bin_seq is not None:
                    bin_seq = str(selected_bin_seq)
                else:
                    bin_seq = None
                         
                # 검색일 선택
                st.date_input("측정일을 선택하세요.",
                            value=st.session_state.searchingDate,
                            max_value=datetime.datetime.now(pytz.timezone('Asia/Seoul')).date(),
                            format="YYYY-MM-DD",
                            key="searchingDateNew",
                            on_change=updateSearchingDate(farm_seq, bin_seq))
                
                st.markdown("<br>", unsafe_allow_html=True)  # 🔹 공백 추가

                if st.button(" 조 회 "):   
                    initSearchingDate()
                    #st.session_state.ConnDB = step3_func.MYSQL_Connect()
                    #st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], farm_seq)
                    #st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
                    st.cache_data.clear()
                    st.cache_resource.clear()

                # 상단 행 (초기 공백 생성)
                placeholder = st.empty()
                with placeholder:  # placeholder에 콘텐츠를 추가
                   st.markdown(
                        '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; font-weight: bold; margin: 2;">농장명 : <p> '
                        + '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; font-weight: bold; margin: 2;">측정일시 : <p> '
                        + '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; font-weight: bold; margin: 2;">사료양 : 재고율(%) &nbsp &nbsp  재고량 (Kg)</p> <br>', 
                        unsafe_allow_html=True
                    )
                    
                # Data Table 
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], farm_seq, bin_seq)
                 
          
            # Left Side
            with article2:
                 
                # 초기 탭 상태 설정
                if 'active_tab' not in st.session_state:
                    st.session_state.active_tab = '측정 내역'

                
                tabs = st.tabs(["측정 내역", "3D 피드빈"])
                
                with tabs[0]:
                        
                    st.subheader("측정 내역") 
                    
                    #if not st.session_state.mysqlDepthDataAll.empty:
                    event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['fistdt','lastdt','bin_nm','stock_ratio','stock_amt', 'desc']],
                                column_config={
                                    "fistdt": st.column_config.Column(
                                        label="측정일자",
                                    ),
                                    "lastdt": st.column_config.Column(
                                        label="측정시간",
                                    ),
                                    "bin_nm": st.column_config.Column(
                                        label="장비번호",
                                    ),
                                    "stock_ratio": st.column_config.NumberColumn(
                                        label="재고율",  
                                        format="%.0f%%"  # 백분율(%) 변환 
                                    ),
                                    "stock_amt": st.column_config.Column(
                                        label="재고량",
                                    ), 
                                    "desc": st.column_config.Column(
                                        label="비고",
                                        width=200
                                    )},
                                on_select='rerun',
                                selection_mode='single-row'
                                )
                    
                    # Select Data
                    if len(event.selection['rows']):
                        st.session_state.dataIndex = int(event.selection['rows'][0])
                        dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)  # 거리 데이터 추출
                        # 사료통 크기 정보를 이용한 선택(동일 용량이 있는 경우 변경해야함) 
                        dataSize = step3_func.SelectSizeFeedBinFromSQL(st.session_state.mysqlFeedBinDataAll, st.session_state.mysqlDepthDataAll.std_volume[st.session_state.dataIndex])
                        
                        st.session_state.dataRaw = dataRaw
                        st.session_state.dataFeedBin = dataSize
                        
                        # 체크된 행의 정보를 한줄로 보여줌.
                        selected_index = int(event.selection['rows'][0])
                        selected_row = st.session_state.mysqlDepthDataAll.loc[selected_index]
                        
                    with placeholder:  # placeholder에 콘텐츠를 추가 
                    
                        strFarmNm = ""; strFistdt = ""; strLastdt = ""; strStockRatio = ""; strStockAmt = ""
                                            
                        if len(event.selection['rows']):
                            strFarmNm = selected_row['farm_nm']
                            strFistdt = str(selected_row['fistdt'])
                            strLastdt = str(selected_row['lastdt'])
                            strStockRatio = str(round(selected_row['stock_ratio']))
                            strStockAmt = str(selected_row['stock_amt']) 
                            
                        st.markdown(
                            '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; margin: 2;">' + '농가명 : &nbsp ' +  strFarmNm + '&nbsp</p> '
                            + '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; margin: 2;">' + '측정일 : &nbsp ' +  strFistdt + '&nbsp ' + strLastdt + '</p> '
                            + '<p style="font-size: 18px; color: #fbcbfa; background-color: #3b3b5a; margin: 2;">' + '사료양 : &nbsp ' + strStockRatio
                            + '% &nbsp &nbsp' + strStockAmt + ' </p> <br> ',
                            unsafe_allow_html=True
                        )
                        
                        
                            
                    # event = st.data_editor(...) 또는 st.dataframe(...)

                with tabs[1]:
                    
                    st.subheader("3D 피드빈")
                    with st.container():  # 컨텐츠 추가
                        if(st.session_state.dataRaw is not None):
                            step4_data.Show3DFeedBin(st.session_state.dataRaw, st.session_state.dataFeedBin)
                    
                      

            
        ## 특정 일의 데이터를 열람
        elif choice == "측정 데이터(수직)":
            
            # 임시 코드 값 설정
            if "selected_code" not in st.session_state:
                st.session_state.selected_code = ""
                 
            username = st.session_state.userName
            farm_df = step3_func.MysqlGetFarmNo(st.session_state.ConnDB, username)  #로그인 유저에게 허용된 농장 List를 조회
            
            # Left Side
            with article1:
                
                 
                # 농가 선택
                if not farm_df.empty:
                    farm_names = farm_df['farm_nm'].tolist()
                    selected_farm = st.selectbox("농가 선택", farm_names, on_change=on_select_change)  
                    
                if not farm_df.empty and selected_farm:
                    selected_farm_seq = farm_df[farm_df['farm_nm'] == selected_farm]['farm_seq'].iloc[0]
                
                if selected_farm_seq is not None:
                    farm_seq = str(selected_farm_seq)
                else:
                    farm_seq = None
                   
                      
                # 피드빈 선택 
                bin_df = step3_func.MysqlGetFeedcheckNo(st.session_state.ConnDB, farm_seq)  #로그인 유저에게 허용된 농장 List를 조회
                 
                # 피드빈 선택
                if not bin_df.empty:
                    bin_names = bin_df['bin_nm'].tolist()
                    selected_bin = st.selectbox("피드빈 선택", bin_names, on_change=on_select_change)
                 
                if not bin_df.empty and selected_bin:
                    selected_bin_seq = bin_df[bin_df['bin_nm'] == selected_bin]['bin_seq'].iloc[0]
                else:
                    selected_bin_seq = None    
            
                if selected_bin_seq is not None:
                    bin_seq = str(selected_bin_seq)
                else:
                    bin_seq = None
                    
                    
                # 검색일 선택
                st.date_input("측정일을 선택하세요.",
                            value=st.session_state.searchingDate,
                            max_value=datetime.datetime.now(pytz.timezone('Asia/Seoul')).date(),
                            format="YYYY-MM-DD",
                            key="searchingDateNew",
                            on_change=updateSearchingDate(farm_seq, bin_seq))
                
                # Data Table 
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], farm_seq, bin_seq)
                  
                # Data Table (위와 동일한 형태로 중복성 방지 필요)
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['fistdt','lastdt','bin_nm','stock_ratio','stock_amt','desc']],
                            column_config={
                                "fistdt": st.column_config.Column(
                                    label="측정일자",
                                ),
                                "lastdt": st.column_config.Column(
                                    label="측정시간",
                                ),
                                "bin_nm": st.column_config.Column(
                                    label="장비번호",
                                ),
                                "stock_ratio": st.column_config.NumberColumn(
                                    label="재고율",  
                                    format="%.0f%%"  # 백분율(%) 변환 
                                ),
                                "stock_amt": st.column_config.Column(
                                    label="재고량",
                                ), 
                                "desc": st.column_config.Column(
                                    label="비고",
                                    width=200
                                )},
                            on_select='rerun',
                            selection_mode='single-row'
                            )
                # Select Data (위와 동일한 형태로 중복성 방지 필요)
                if len(event.selection['rows']):
                    st.session_state.dataIndex = int(event.selection['rows'][0])
                    if(st.button("[Show] {}".format(st.session_state.mysqlDepthDataAll.loc[st.session_state.dataIndex,['date']].iloc[0]))):
                        dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)  # 거리 데이터 추출
                        # 사료통 크기 정보를 이용한 선택(동일 용량이 있는 경우 변경해야함)
                        dataSize = step3_func.SelectSizeFeedBinFromSQL(st.session_state.mysqlFeedBinDataAll, st.session_state.mysqlDepthDataAll.std_volume[st.session_state.dataIndex])
                        selected_feedbin = st.session_state.mysqlFeedBinDataAll[st.session_state.mysqlFeedBinDataAll['FeedBinSerialNo'] == dataSize.FeedBinSerialNo.iloc[0]]
                        st.dataframe(selected_feedbin)
                        if(dataRaw is not None):
                            step4_data.Show3DFeedBin(dataRaw, dataSize)
                        print("Select Row",st.session_state.dataIndex)

        # 사료통 없는 사료 정보를 확대해서 보여주는 요소
        elif choice == "측정 데이터(무보정)":
            
            
            username = st.session_state.userName
            farm_df = step3_func.MysqlGetFarmNo(st.session_state.ConnDB, username)  #로그인 유저에게 허용된 농장 List를 조회
            
            # Left Side
            with article1:
                ## Title
                 
                # 농가 선택
                if not farm_df.empty:
                    farm_names = farm_df['farm_nm'].tolist()
                    selected_farm = st.selectbox("농가 선택", farm_names, on_change=on_select_change)  
                    
                if not farm_df.empty and selected_farm:
                    selected_farm_seq = farm_df[farm_df['farm_nm'] == selected_farm]['farm_seq'].iloc[0]
                
                if selected_farm_seq is not None:
                    farm_seq = str(selected_farm_seq)
                else:
                    farm_seq = None
                   
                      
                # 피드빈 선택 
                bin_df = step3_func.MysqlGetFeedcheckNo(st.session_state.ConnDB, farm_seq)  #로그인 유저에게 허용된 농장 List를 조회
                 
                # 피드빈 선택
                if not bin_df.empty:
                    bin_names = bin_df['bin_nm'].tolist()
                    selected_bin = st.selectbox("피드빈 선택", bin_names, on_change=on_select_change)
                 
                if not bin_df.empty and selected_bin:
                    selected_bin_seq = bin_df[bin_df['bin_nm'] == selected_bin]['bin_seq'].iloc[0]
                else:
                    selected_bin_seq = None    
            
                if selected_bin_seq is not None:
                    bin_seq = str(selected_bin_seq)
                else:
                    bin_seq = None
                     
                # st.title("CONSTANTEC FEED CHECK \n 3D LiDAR 측정 시스템 (3D Bin Manager 1.0)") 
                # st.markdown("*측정 데이터 조회 선택")
                # 검색일 선택 (위와 동일한 형태로 중복성 방지 필요)
                st.date_input("측정일을 선택하세요.",
                        value=st.session_state.searchingDate,
                        max_value=datetime.datetime.now(pytz.timezone('Asia/Seoul')).date(),
                        format="YYYY-MM-DD",
                        key="searchingDateNew",
                        on_change=updateSearchingDate(farm_seq, bin_seq))

                # Data Table 
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, st.session_state.searchingDate[0], st.session_state.searchingDate[1], farm_seq, bin_seq)
                  
                  
                # Data Table (위와 동일한 형태로 중복성 방지 필요)
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['fistdt','lastdt','bin_nm','stock_ratio','stock_amt','desc']],
                        column_config={
                            "fistdt": st.column_config.Column(
                               label="측정일자",
                            ),
                            "lastdt": st.column_config.Column(
                                label="측정시간",
                            ),
                            "bin_nm": st.column_config.Column(
                                label="장비번호",
                            ),
                            "stock_ratio": st.column_config.NumberColumn(
                                label="재고율",  
                                format="%.0f%%"  # 백분율(%) 변환 
                            ),
                            "stock_amt": st.column_config.Column(
                                label="재고량",
                            ), 
                            "desc": st.column_config.Column(
                                label="비고",
                                width=200
                            )},
                        on_select='rerun',
                        selection_mode='single-row'
                        )
                # Select Data (유사하나 출력 방식이 다름)
                articleL, articleR = st.columns([1,1])
                with articleL:
                    st.number_input("x 중심", key="dataCenterX", on_change=updateCenterPos, value=float(st.session_state.centerPos[0]))
                with articleR:
                    st.number_input("Y 중심", key="dataCenterY", on_change=updateCenterPos, value=float(st.session_state.centerPos[1]))
            
                if len(event.selection['rows']):
                    st.session_state.dataIndex = int(event.selection['rows'][0])
                    if(st.button("[Show] {}".format(st.session_state.mysqlDepthDataAll.loc[st.session_state.dataIndex,['date']].iloc[0]))):
                        dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)   # 거리 데이터 추출
                        step4_data.Show3DRawData(dataRaw)
                        print("Select Row", st.session_state.dataIndex)
        
        
        
        # 프로그램 Option 변경으로 Python의 변수를 활용함 (정리 혹은 변경 필요)
        elif choice == "기타":
            st.subheader("데이터 화면 옵션") 

            # Layout
            col1, col2 , col3= st.columns(3)

            optionFeedbinMode = ['모두', '절반', '벽 없음']
            with col1:
                st.markdown("Mesh")
                st.slider("사료 투명도",0,100,value=param.DISPLAY_MESH_ALPHA,key="newMeshAlpha" , on_change=param.ChageMeshAlpha)
                DISPLAY_MESH_COLORMAP = st.selectbox("Color Map",param.DISPLAY_COLORMAP_LIST,index=39) 
            with col2:
                st.markdown("Grid")
                DISPLAY_GRID_ALPHA = st.slider("선 투명도",0,100,value=param.DISPLAY_GRID_ALPHA)
                DISPLAY_GRID_COLOR = st.color_picker("Grid Color",param.DISPLAY_GRID_COLOR)
            with col3:
                st.markdown("Feedbin")
                DISPLAY_TOPWALL_ALPHA = st.slider("통 투명도",0,100,value=param.DISPLAY_WALL_ALPHA)
                DISPLAY_TOPWALL_COLOR = st.color_picker("통 상단 Color",param.DISPLAY_WALL_COLOR)
                DISPLAY_TOPWALL_DENSITY = st.slider("통 밀도",10,100,value=param.DISPLAY_TOPWALL_DENSITY)
                DISPLAY_BOTTOMWALL_COLOR = st.color_picker("통 하단 Color",param.DISPLAY_BOTTOMWALL_COLOR)
                DISPLAY_BOTTOMWALL_DENSITY = st.slider("사료 밀도",10,100,value=param.DISPLAY_BOTTOMWALL_DENSITY)
                selectionWallMode = st.selectbox(
                    "사료통 출력 모드",
                    optionFeedbinMode,
                    index=param.DISPLAY_TOPWALL_MODE,
                )
                DISPLAY_TOPWALL_MODE = optionFeedbinMode.index(selectionWallMode)
            
            st.markdown("3D LiDAR PointCloud")
            DISPLAY_SCATTER_POINT_SIZE = st.slider("점 크기",3,20,value=param.DISPLAY_SCATTER_POINT_SIZE)

            if(st.button("reset")):
                param.Initialize()
                st.rerun()
    with empty2:
        st.empty()

if __name__ == "__main__":
    main()
