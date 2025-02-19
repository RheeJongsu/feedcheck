import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import numpy as np
from io import StringIO
import math
import plotly.graph_objects as go
from modules import step3_func
from modules import func_display as display
from modules import userParam as param

### Main function to integrate everything
def connect_data(ConnDB):
    # 사용자 입력: 날짜 범위 설정
    index = 1
    date_start = '2025-01-01'
    date_end = '2025-02-03'

    # 사용자 입력: FeedBin Serial 입력
    SerialFeedBin = st.text_input("Enter Serial Feed Bin", value="BIN100070")

    # MYSQL 연결
    if ConnDB is None:
        st.error("Database connection failed. Please check your credentials.")
        return

    # 데이터 가져오기
    try:
        dfAll = step3_func.MysqlGetDepthData(ConnDB, str(date_start), str(date_end))
        sizeFeedBinAll = step3_func.MysqlGetSizeFeedBin(ConnDB)

        # 입력한 SerialFeedBin에 해당하는 FeedBin 정보만 필터링
        selected_feedbin = sizeFeedBinAll[sizeFeedBinAll['FeedBinSerialNo'] == SerialFeedBin]

        if not selected_feedbin.empty:
            st.subheader("Selected FeedBin Size Information")
            st.dataframe(selected_feedbin)

            dataRaw = step3_func.SelectDataFromMYSQL(dfAll, index)  # 거리 데이터 추출
            dataSize = step3_func.SelectSizeFeedBinFromSQL(sizeFeedBinAll, SerialFeedBin)  # 사료통 크기 정보

            ## Result
            [dataModified, dataBound] = step3_func.GetFilteredData(dataRaw, dataSize)

            ## Save
            st.session_state.dataRaw = dataRaw
            st.session_state.dataFiltered = dataModified
            st.session_state.dataBound = dataBound

            #Draw
            fig = go.Figure()
            fig = step3_func.Draw3DFeedBinAll(fig,dataModified, dataBound, dataSize)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning(f"No data found for Serial Feed Bin: {SerialFeedBin}")

        st.sidebar.success("Data fetched successfully!")

    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
    finally:
        ConnDB.close()

@st.cache_resource
def Show3DFeedBin(dataRaw, dataSize):
    ## Result
    [dataModified, dataBound] = step3_func.GetFilteredData(dataRaw, dataSize)
    
    #Draw
    fig = go.Figure()

    ## Draw MeshGrid
    fig = display.Draw3DMeshGrid(fig, dataModified) 
     
    ## Draw FeedBin
    FeedBinSizeR = [dataSize.bot2.iloc[0]/param.VOXEL_GAP/2, dataSize.mid2.iloc[0]/param.VOXEL_GAP/2,  dataSize.top2.iloc[0]/param.VOXEL_GAP/2,  dataSize.top1.iloc[0]/param.VOXEL_GAP/2]
    FeedBinSizeH = [0, dataSize.bot_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0]+dataSize.top_H.iloc[0]]
    fig = display.Draw3DFeedBin(fig, FeedBinSizeR, FeedBinSizeH)
    fig = display.Draw3DFeedBinBoundUp(fig, dataBound, FeedBinSizeR, FeedBinSizeH)
    fig = display.Draw3DFeedBinBoundDown(fig, dataBound, FeedBinSizeR, FeedBinSizeH)

    ## Draw Option
    z = dataModified[:,2]
    XYdrawRange = [20, 80]  ## 잘보이는 값을 수동으로 찾음 24.12.24
    ZdrawRange = [0, FeedBinSizeH[3]] 
    figureHeight = 500  
    
    display.Draw3DLayout(fig, "3D Mesh with Gridlines", XYdrawRange, ZdrawRange, figureHeight)  #관심영역 확대하여 출력
     
    st.plotly_chart(fig, use_container_width=True)     
    if(st.session_state.Debug):print("[Show3DFeedBin] 출력 데이터를 생성했습니다. 렌더링을 시작합니다")
    

def Show3DFeed(dataRaw, dataSize):
    ## Result
    [dataModified, ] = step3_func.GetFilteredData(dataRaw, dataSize)

    #Draw
    fig = go.Figure()

    ## Draw MeshGrid
    fig = display.Draw3DMeshGrid(fig,dataModified)

    ## Draw Option
    z = dataModified[:,2]
    MaxZ = int(max(z))
    MinZ = int(min(z))
    ZdrawRange = [1.5*MinZ - 0.5 * MaxZ, 1.5 * MaxZ - 0.5 * MinZ]
    XYdrawRange = None
    figureHeight = 800 #1000px

    display.Draw3DLayout(fig, "3D Mesh with Gridlines", XYdrawRange, ZdrawRange, figureHeight)  #관심영역 확대하여 출력
    fig = step3_func.Draw3DFeedAll(fig,dataModified,dataSize)
    
    st.plotly_chart(fig, use_container_width=True)

def Show3DRawData(dataRaw):
    #Draw
    fig = go.Figure()
    fig = display.Display3DScatter(fig,dataRaw)
    fig.update_layout(
        height=800  # 높이를 1000px로 설정
    )
    st.plotly_chart(fig, use_container_width=True)