# app.py
import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
from modules import step1_user_setup, step2_install_dependencies
from modules import step3_func
from modules import step4_data
from modules import userParam as param

st.set_page_config(page_title="SmartFeedBin", page_icon="🔔", layout="wide")
# Layout
empty1, Contents1, empty2 = st.columns([0.1,1,0.1])
article1, article2, article3= st.columns(3)
 

def login():
    with st.spinner("Check up user..."):
        pass #step1_user_setup.create_user(username=username, password=password)
    try:
        st.session_state.ConnDB = step3_func.MYSQL_Connect()
    except Exception as e:  #Login Failed
        print(f"An error occurred during user setup: {e}")
        st.session_state.ConnDB = None
        st.session_state.MessageShow = f"<span style='color:red'> {e}</span>"

    # Download DB
    if st.session_state.ConnDB is None :
        st.error("Database connection failed. Please check your credentials.")
        st.session_state.MessageShow = f"<span style='color:red'> Database connection failed. Please check your credentials. </span>"
    else:    
        st.session_state.isLogin = True
        st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
        st.success("Loading Feedbin Data......")
        st.session_state.MessageShow = None
    
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

    st.session_state.Debug = True

    ## Event Callback
    def updateSearchingDate():
        if(len(st.session_state.searchingDate) == 2):
            date_start = st.session_state.searchingDate[0]
            date_end = st.session_state.searchingDate[1]
            st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, str(date_start), str(date_end))
    
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
            
        choice = st.sidebar.radio(" ", ["측정 데이터","측정 데이터(원본)", "기타"])
        
        st.sidebar.text(" ") 
        st.sidebar.text(" ") 
        
        if st.sidebar.button("조회"):
            st.session_state.ConnDB = step3_func.MYSQL_Connect()
            st.session_state.mysqlFeedBinDataAll = step3_func.MysqlGetSizeFeedBin(st.session_state.ConnDB)
            st.cache_data.clear()
            st.cache_resource.clear()

    else:
        choice = st.sidebar.radio(" ", ["Login"])
    
    ## Main Contents
    with empty1:
        st.empty()
    with Contents1:
        ## Error Message
        if(st.session_state.MessageShow is not None):
            st.markdown(st.session_state.MessageShow, unsafe_allow_html=True)
        
        ## Login First Page
        if choice == "Login":
            st.subheader("Mobile Login")
            username = st.text_input("Username", value="Constantec")
            password = st.text_input("Password", value="root", type="password")
            st.session_state.userName = username
            if st.button("Login",on_click=login):
                st.rerun()

        ## 최근 정보를 열람        
        elif choice == "측정 데이터":      
            
            row1 = st.columns(1)  # 첫 번째 행
            row2 = st.columns(1)  # 두 번째 행
 
            # 30days Infomation
            if(st.session_state.IsLoad == False):           
                today = datetime.datetime.now()
                date_star = today - datetime.timedelta(days=40) # 1개월전
                date_end = today
                st.session_state.mysqlDepthDataAll = step3_func.MysqlGetDepthData(st.session_state.ConnDB, str(date_star), str(date_end))
                st.session_state.IsLoad = True
                print("[DataLoad] Complete")
                st.rerun()
            # Display Info
            
            # Left Side
            #with article1:
            with row1[0]:
                st.markdown("📊 피드빈 측정 리스트")                
                # Data Table
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['date','stock_ratio','desc','std_volume','std_amt']],
                            column_config={
                                "date": st.column_config.Column(
                                    label="측정일자",
                                ),
                                 "stock_ratio": st.column_config.Column(
                                    label="재고율(%)",
                                ),
                                "desc": st.column_config.Column(
                                    label="비고",
                                    width=200
                                ),
                                "std_volume": st.column_config.Column(
                                    label="전체규격(㎥)",
                                ),                               
                                "std_amt": st.column_config.Column(
                                    label="전체무게(ton)",
                                )},
                            use_container_width=True,  # 전체 너비 확장
                            height=250,  # 표의 높이 조절 (픽셀 단위)                            
                            on_select='rerun',
                            selection_mode='single-row'
                            )
                 
                
                # HTML/CSS 스타일이 적용된 구분선 추가
                # st.markdown("<hr style='border:1px solid #76a; margin:1px 0; padding: 0;'>", unsafe_allow_html=True)
                
                # 상단 행 (초기 공백 생성)
                placeholder = st.empty()
                with placeholder:  # placeholder에 콘텐츠를 추가
                   st.markdown(
                        '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #1C3F10, #2B631A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">농장명  &nbsp &nbsp  측정일시 </p> '
                        + '<p style="font-size: 15px; color: #ababab; font-weight: bold; background: linear-gradient(to right, #1C3F10, #2B631A); padding: 1px; border-radius: 3px; text-align: left; margin: 5px 0;">사료 재고율(%) &nbsp &nbsp  재고량 (ton)</p>', 
                        unsafe_allow_html=True
                    )
                
                # HTML/CSS 스타일이 적용된 구분선 추가
                st.markdown("<hr style='border:1px solid #a26; margin:1px 0; padding: 0;'> <br>", unsafe_allow_html=True)

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
                        st.markdown(
                            '<p style="font-size: 15px; color: #a0a0ea; font-weight: bold; background: linear-gradient(to right, #1C3F10, #2B631A); padding: 1px; border-radius: 3px; text-align: left; margin: 1px 0;">' + selected_row['farm_nm'] + '&nbsp &nbsp ' + str(selected_row['date']) + '</p> '
                            + '<p style="font-size: 15px; color: #eba0a0; font-weight: bold; background: linear-gradient(to right, #1C3F10, #2B631A); padding: 1px; border-radius: 3px; text-align: left; margin: 5px 0">' + '사료양 &nbsp ' + str(selected_row['stock_ratio'])
                            + ' (%) &nbsp &nbsp' +  str(selected_row['stock_amt']) + ' (ton)</p>', 
                            unsafe_allow_html=True
                        )
 
            # Right Side
            #with article2:
            with row2[0]:
                 
                if(st.session_state.dataRaw is not None):   
                    st.markdown("⏳ 측정 데이터")                
                    step4_data.Show3DFeedBin(st.session_state.dataRaw, st.session_state.dataFeedBin)
 
        # 사료통 없는 사료 정보를 확대해서 보여주는 요소
        elif choice == "측정 데이터(원본)":
             
            row1 = st.columns(1)  # 첫 번째 행
            row2 = st.columns(1)  # 두 번째 행
  
            # Left Side
            with row1[0]: 
                st.markdown("📊 피드빈 측정 리스트")                
                ## Title
                # st.title("CONSTANTEC FEED CHECK \n 3D LiDAR 측정 시스템 (3D Bin Manager 1.0)") 
                # st.markdown("*측정 데이터 조회 선택")
                # 검색일 선택 (위와 동일한 형태로 중복성 방지 필요)
                today = datetime.datetime.now()
                one_month_ago = today - relativedelta(months=1)
                d = st.date_input("측정일을 선택하세요.",
                                (one_month_ago,today),
                                max_value=today,
                                format="YYYY-MM-DD",
                                key='searchingDate',
                                on_change=updateSearchingDate)
                  
                # Data Table (위와 동일한 형태로 중복성 방지 필요)
                event = st.dataframe(st.session_state.mysqlDepthDataAll.loc[:,['date','stock_ratio','desc','std_volume','std_amt']],
                        column_config={
                            "date": st.column_config.Column(
                                label="측정일자",
                            ),
                              "stock_ratio": st.column_config.Column(
                                label="재고율(%)",
                            ),
                            "desc": st.column_config.Column(
                                label="비고",
                                width=200 
                            ),
                            "std_volume": st.column_config.Column(
                                label="전체규격(㎥)",
                            ),
                            "std_amt": st.column_config.Column(
                                label="전체무게(ton)",
                            )},
                        on_select='rerun',
                        selection_mode='single-row'
                        )
             
                # 선택한 행의 정보를 추출
                selected_index = None  # 초기화 추가
                # Select Data (유사하나 출력 방식이 다름)                 
                if len(event.selection['rows']):
                    st.session_state.dataIndex = int(event.selection['rows'][0])
                    dataRaw = step3_func.SelectDataFromMYSQL(st.session_state.mysqlDepthDataAll, st.session_state.dataIndex)  # 거리 데이터 추출 
                    st.session_state.dataRaw = dataRaw
                    
            # Right Side
            with row2[0]:
                if st.session_state.dataRaw is not None: 
                    st.markdown("⏳ 측정 데이터")      
                    dataRaw = st.session_state.dataRaw
                    step4_data.Show3DRawData(dataRaw)
                    #print("Select Row", st.session_state.dataIndex)
        
        
        
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

    #Debug용
    #print("Done", step3_func.DISPLAY_MESH_COLORMAP)

if __name__ == "__main__":
    main()
