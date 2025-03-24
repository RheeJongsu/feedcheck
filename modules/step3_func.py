import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import numpy as np
from io import StringIO
import math
import plotly.graph_objects as go
from modules import userParam as param
    
def MYSQL_Connect():
    ## MYSQL Info [engine]
    host = "constantec-db1.cba0g2ca0291.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    username = "cons"
    password = 'Mdb9367027!!'
    db = 'cons'
    stringSQL = "mysql+pymysql" + "://" + username + ':' + password + '@' + host + "/" + db
    engine = create_engine(stringSQL)
    
    ## Connect MYSQL [MYSQLconnect]
    MYSQLconnect = engine.connect()
    return MYSQLconnect

def AuthenticateUser(MYSQLconnect, username, password):     
    sql_state = "select user_nm  from tb_user where user_id = '" + str(username) + "' and password = '" + str(password) + "';"
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetFarmNo(MYSQLconnect, username):
    sql_state = "select farm_seq, farm_nm   from  tb_farm  where use_yn = 'Y' "  
    
    if username != "constantec":    
       sql_state += " and user_seq = (select user_seq from tb_user where user_id = '" + str(username) + "');"    
       
    # print(" 쿼리11 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", sql_state)            
                
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetFeedcheckNo(MYSQLconnect, farm_seq):     
    sql_state = "select 0 as bin_seq, '선택안함' as bin_nm " \
                " union all " \
                " select T1.bin_seq, T1.bin_nm   from tb_feedbin T1  " \
                " where T1.use_yn = 'Y' "  \
                "   and T1.farm_seq = '" + farm_seq + "' " 
 
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetDepthDataShow(MYSQLconnect, date_start, date_end):
    sql_state = "select T1.chk_date, T1.std_volume, T1.std_amt, T1.stock_ratio, T1.desc" \
                "from tb_change_data T1 where T1.chg_x !='' and T1.create_time between '" + str(date_start) + "' and '" + str(date_end) + " 23:59:59';"
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetDepthDataold(MYSQLconnect, date_start, date_end):
    sql_state = "select T1.chk_date as date, T1.chg_volume as rawData, T1.chg_x as x, T1.chg_y as y, T1.chg_z as z, T1.std_volume, T1.std_amt, T1.stock_ratio, T1.desc " \
                "from tb_change_data T1 where T1.chg_x !='' and T1.chk_date between '" + str(date_start) + "' and '" + str(date_end) + " 23:59:59' order by T1.chk_date desc;"
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetDepthData(MYSQLconnect, date_start, date_end, farm_seq, bin_Seq):
    sql_state = "select T1.chk_date as date, LEFT(T1.chk_date, 10) as fistdt,  SUBSTR(T1.chk_date, 12, 5) as lastdt, " \
                " T1.chg_volume as rawData, T1.chg_x as x, T1.chg_y as y, T1.chg_z as z, T1.std_volume, " \
                " T1.std_amt, T1.stock_ratio, LPAD(CONCAT(FORMAT(ROUND(T1.stock_amt * 1000), 0), 'Kg'), 10, ' ') as stock_amt, " \
                " T1.desc, T2.farm_nm, T3.bin_nm, T1.center_x, T1.center_y " \
                " from tb_change_data T1, tb_farm T2, tb_feedbin T3 " \
                " where  T1.chg_x !='' and T1.chk_date between '" + str(date_start) + "' and '" + str(date_end) + " 23:59:59' " \
                " and T1.bin_seq = T3.bin_seq and T2.farm_seq = '" + farm_seq + "' "  
                
    if bin_Seq != "0":    
       sql_state += " and T3.bin_Seq = '" + bin_Seq + "' " \
                        
    sql_state += " and T3.farm_seq = T2.farm_seq  order by T1.chk_date desc  LIMIT 50;" 
    
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

def MysqlGetSizeFeedBin(MYSQLconnect):
    sql_state = "SELECT bin_serial_no as FeedBinSerialNo,bin_volume, top_diameter1 as top1, top_diameter2 as top2, top_height as top_H, " \
                "mid_diameter1 as mid1, mid_diameter2 as mid2, mid_height as mid_H, " \
                "bot_diameter1 as bot1, bot_diameter2 as bot2, bot_height as bot_H, " \
                "lidar_height as lidar_h " \
                "FROM tb_feedbin WHERE bot_diameter1 != 'NaN';"
    return pd.read_sql_query(sql=text(sql_state), con=MYSQLconnect)

### DB    
def SelectDataFromMYSQL(df, index):
    ## 문자열을 파일처럼 처리하기 위해 StringIO 사용
    x = np.genfromtxt(StringIO(df['x'][index]), delimiter=",", encoding="utf-8")
    y = np.genfromtxt(StringIO(df['y'][index]), delimiter=",", encoding="utf-8")
    z = np.genfromtxt(StringIO(df['z'][index]), delimiter=",", encoding="utf-8")
    
    ## 의미 없는 값(측정값 0) 제거 후 데이터 생성
    dataTemp = []
    for i in range(x.size):
        if(math.isnan(x[i])): continue
        dist = math.sqrt(x[i]**2 + y[i]**2 + z[i]**2)
        if(dist < param.MIN_DETECTION_DISTANCE): continue  # 센서 측정값이 측정 최솟값을 넘는 경우 데이터 반영 (2024.11.27)
        if(dist > param.MAX_DETECTION_DISTANCE): continue  # 센서 측정값이 측정 최솟값을 넘는 경우 데이터 반영 (2024.11.27)
        dataTemp.append([x[i], y[i], z[i]])
    dataRaw = np.array(dataTemp)

    st.session_state.zRange[0] = np.min(dataRaw, axis=0)[2]
    st.session_state.zRange[1] = np.max(dataRaw, axis=0)[2]
    if(df['center_x'][index] != None):
        st.session_state.centerPos[0] = df['center_x'][index]
    else :
        st.session_state.centerPos[0] = 0

    if(df['center_y'][index] != None):
        st.session_state.centerPos[1] = df['center_y'][index]
    else : 
        st.session_state.centerPos[1] = 0
    
    ## 결과 출력        
    print(str(df['date'][index]) + "일 데이터를 선택하였습니다.")
    print("측정 데이터 " + str(x.size) + "개 중 " + str(dataRaw.shape[0]) + "개를 사용합니다.")
    if(dataRaw.shape[0] < param.MIN_NUM_SAMPLEDATA):
       print("데이터 수가 "+str(param.MIN_NUM_SAMPLEDATA)+"개 보다 작아 출력이 불가능합니다.")
       return None
    return dataRaw

def SelectSizeFeedBinFromSQL(dfFeedBin, FeedBinSize):
    #통의 용량으로 통을 선택함
    res = dfFeedBin.loc[dfFeedBin.bin_volume == FeedBinSize, ['FeedBinSerialNo','top1', 'top2', 'top_H', 'mid1', 'mid2', 'mid_H', 'bot1', 'bot2', 'bot_H', 'lidar_h']]        
    
    ## 결과 출력
    print("사료통의 크기 모델은 '" + dfFeedBin.FeedBinSerialNo[res.index[0]] + "'이며 크기는 다음과 같습니다.")        
    #print(res)
    return res

######################################### Compensation #########################################    
def GetRoIPointCloud(df,Center,Radius):
    if(st.session_state.Debug):print("[GetRoIPointCloud] 관련 영역의 데이터를 추출합니다.")
    # Check Validation
    if(df is None):
        return None

    # Data
    x = df[:,0]
    y = df[:,1]
    z = df[:,2]

    # Output
    dataTemp = []
    for i in range(df.shape[0]):
        if (math.sqrt((Center[0] - x[i]) ** 2 + (Center[1] - y[i]) ** 2) < Radius):
            #센서 위치에 따른 정보 보정 (가운데가 가운데로)
            tfX = x[i]-Center[0]
            tfY = y[i]-Center[1]
            tfZ = z[i]
            dataTemp.append([tfX,tfY,tfZ])
    return np.array(dataTemp)

def gaussian_kernel(size, sigma):
    kernel = np.fromfunction(
        lambda x, y: (1 / (2 * np.pi * sigma**2)) * np.exp(-((x - (size - 1) / 2)**2 + (y - (size - 1) / 2)**2) / (2 * sigma**2)), (size, size))        
    return kernel / np.sum(kernel)

def convolve2DExcept(data, kernel, exceptValue):
    kernel_size = kernel.shape[0]
    pad_width = kernel_size // 2
    padded_data = np.pad(data, pad_width, mode='constant', constant_values=0) # 경계 처리        
    result = np.zeros_like(data)
    
    # Convolution 연산
    for r in range(result.shape[0]):
        for c in range(result.shape[1]):
            replaceValue = padded_data[r + pad_width, c + pad_width]    
            if(replaceValue == exceptValue):
                result[r, c] = replaceValue
                continue    
            region = padded_data[r:r + kernel_size, c:c + kernel_size]    

            # 제외 값이 있는 경우 해당 위치를 무시하고 계산
            mask = region != exceptValue
            valid_region = region * mask  # 제외 값 무시한 유효한 값만 남김    
            valid_kernel = kernel * mask  # 커널도 동일하게 마스킹   

# 정규화: 커널 값의 합이 1이 되도록 조정 (제외 값이 있을 때)
            kernel_sum = np.sum(valid_kernel)
            if kernel_sum != 0:
                valid_kernel = valid_kernel / kernel_sum
            result[r, c] = np.sum(valid_region * valid_kernel)
    return result

def PointCloudToVoxel(df,maxDist,roiRadius,FeedBinSizeR, FeedBinSizeH):
    if(st.session_state.Debug):print("[PointCloudToVoxel] 영역 데이터에 대해 사료 정보 변환을 완료하였습니다.")
    #Check Valid
    if(df is None):
        if(st.session_state.Debug):print("[PointCloudToVoxel] Error No Data")
        return [None, None]
    
    # Data
    print(df.shape)

    x = df[:,0]
    y = df[:,1]
    z = df[:,2]

    # Voxel Map
    map         = maxDist * np.ones([param.VOXEL_SIZE,param.VOXEL_SIZE],dtype = float)
    map_update  = np.zeros([param.VOXEL_SIZE,param.VOXEL_SIZE],dtype = float)

    for index in range(len(x)):
        indexX = int(round(((x[index]) / param.VOXEL_GAP) + param.VOXEL_SIZE/2,0))
        indexY = int(round(((y[index]) / param.VOXEL_GAP) + param.VOXEL_SIZE/2,0))

        # Check Bound
        if(indexX > param.VOXEL_SIZE or indexX < 1): continue
        if(indexY > param.VOXEL_SIZE or indexY < 1): continue

        if (map[indexX,indexY] > z[index] or map[indexX,indexY] != maxDist):
            map[indexX,indexY] = z[index]

    ## 출력을 위해서 정보를 뒤집어서 보여줌 (센서 거리 -> 사료의 높이)
    map = maxDist - map

    ## Map 정보 기록 (관심영역 밖 0, 관심영역 중 값 없음 1, 관심영역 중 값 있음 2)
    radius = roiRadius
    for y in range(param.VOXEL_SIZE):
        for x in range(param.VOXEL_SIZE):
            r = math.sqrt(((x - param.VOXEL_SIZE/2)*param.VOXEL_GAP)**2 + ((y - param.VOXEL_SIZE/2)*param.VOXEL_GAP)**2)
            if(r < radius):  # 복구가 필요한 영역 확인
                if(map[x,y] ==0):
                    map_update[x,y] = 1
                else:
                    map_update[x,y] = 2
            else:
                    map_update[x,y] = 0

    ## Map의 빈 값을 보정
    #Step 1 단순 평균값 사용함  추후 보정할 수 있음
    DistSum = 0
    num = 0
    for y in range(param.VOXEL_SIZE):
        for x in range(param.VOXEL_SIZE):
            if(map_update[x,y] == 2):
                DistSum = DistSum+ map[x,y]
                num = num+1
    DistAvg = DistSum/num

    num = 0
    #Step 2 90도 회전으로 빈 값을 찾음
    for y in range(param.VOXEL_SIZE):
        for x in range(param.VOXEL_SIZE):
            if(map_update[x,y] == 1):
                indexX = param.VOXEL_SIZE - y
                indexY = param.VOXEL_SIZE - x
                if(map_update[indexX,indexY] == 2) : #xy선대칭
                    map_update[x,y] = 2
                    map[x,y] = map[indexX,indexY]
                    num = num+1

    #Step 3 빈값이 있는 경우 주변 값으로 대처 (N회 순환)
    kernel_size = param.SMOOTH_KERNAL_SIZE  # Gaussian 커널 크기 (홀수)
    for j in range(3):
        flagCheck = 0
        for y in range(param.VOXEL_SIZE):
            for x in range(param.VOXEL_SIZE):
                if(map_update[x,y] == 1):
                    DistSum = 0
                    num = 0
                    flagCheck = flagCheck + 1
                    for yk in range(kernel_size):
                        indexYTemp = y - yk + (kernel_size+1)//2
                        if((indexYTemp < 0) or (indexYTemp > param.VOXEL_SIZE)):continue
                        for xk in range(kernel_size):
                            indexXTemp = x - xk + (kernel_size+1)//2
                            if((indexXTemp < 0) or (indexXTemp > param.VOXEL_SIZE)):continue
                            if((map_update[indexXTemp,indexYTemp] > 1) and (map_update[indexXTemp,indexYTemp] < 3+j)):
                                DistSum = DistSum + map[indexXTemp,indexYTemp]
                                num = num + 1
                    if(num > 4):
                        map[x,y] = DistSum / num
                        map_update[x,y] = 3+j
        if(flagCheck == 0): 
            break

    ## 조건에 맞는 빈 값을 찾음  (마지막 작업 !!!)
    radius = roiRadius
    num = 0
    for y in range(param.VOXEL_SIZE):
        for x in range(param.VOXEL_SIZE):
            if(map_update[x,y] == 1):
                map[x,y] = DistAvg
                num = num +1

    ## Map의 정보를 완만하게 변경함
    gaussian_k = gaussian_kernel(param.SMOOTH_KERNAL_SIZE  , param.SMOOTH_KERNAL_SIGMA )
    blurredmap = convolve2DExcept(map, gaussian_k, 0)

    ## 관심 영역 출력을 위해 Voxel -> Point Cloud
    #경계 면에 대한 값은 통의 크기를 기준으로 함
    #통의 경계와 만나면 값을 없애는 방향으로
    dataTemp = []
    num = 0
    dataBound = np.zeros([360,2],dtype = float)

    for y in range(param.VOXEL_SIZE):
        for x in range(param.VOXEL_SIZE):
            if(blurredmap[x][y] != 0):
                r = math.sqrt(((x - param.VOXEL_SIZE/2))**2 + ((y - param.VOXEL_SIZE/2))**2) # 중심으로 부터의 거리
                angle = round(math.atan2((y - param.VOXEL_SIZE/2),(x - param.VOXEL_SIZE/2))*180/math.pi)
                if(angle < 0):
                    angle = angle + 360

                MaxZ = blurredmap[x][y]
                flagSave = False
                if(MaxZ < FeedBinSizeH[1]):
                    rate = MaxZ / FeedBinSizeH[1]
                    SurfR = (1-rate)*FeedBinSizeR[0] + rate*FeedBinSizeR[1]
                elif(MaxZ < FeedBinSizeH[2]):
                    rate = (MaxZ - FeedBinSizeH[1]) / (FeedBinSizeH[2] - FeedBinSizeH[1])
                    SurfR = (1-rate)*FeedBinSizeR[1] + rate*FeedBinSizeR[2]
                elif(MaxZ < FeedBinSizeH[3]):
                    rate = (MaxZ - FeedBinSizeH[2]) / (FeedBinSizeH[3] - FeedBinSizeH[2])
                    SurfR = (1-rate)*FeedBinSizeR[2] + rate*FeedBinSizeR[3]
                if(r < SurfR):
                    flagSave = True
                if(flagSave):
                    dataTemp.append([x,y,blurredmap[x][y]])
                    if(r > SurfR-5):
                        dataBound[angle,0] = MaxZ
                        dataBound[angle,1] = r
                num = num + 1

    for j in range(3):
        flagCheck = 0
        for i in range(360):
            if(dataBound[i,0] == 0):
                sumZ = 0
                sumR = 0
                num = 0
                flagCheck = flagCheck + 1
                for k in range(5):
                    indexAngle = i - k + 3
                    if(indexAngle < 0):
                        indexAngle = indexAngle + 360
                    elif(indexAngle >= 360):
                        indexAngle = indexAngle - 360
                    if(dataBound[indexAngle,0] != 0):
                        sumZ = sumZ + dataBound[indexAngle,0]
                        sumR = sumR + dataBound[indexAngle,1]
                        num = num + 1
                    if(num != 0):
                        dataBound[i,0] = sumZ / num
                        dataBound[i,1] = sumR / num
        if(flagCheck == 0): break

    #Boundary Smooding
    dataBoundModified = np.zeros([360,2],dtype = float)
    for i in range(360):
        sumZ = 0
        sumR = 0
        num = 0
        for k in range(7):
            indexAngle = i - k + 5
            if(indexAngle < 0):
                indexAngle = indexAngle + 360
            elif(indexAngle >= 360):
                indexAngle = indexAngle - 360
            sumZ = sumZ + dataBound[indexAngle,0]
            sumR = sumR + dataBound[indexAngle,1]
            num = num + 1
        dataBoundModified[i,0] = sumZ / num
        dataBoundModified[i,1] = sumR / num

    for i in range(360):
        MaxZ = dataBoundModified[i,0]
        if(MaxZ < FeedBinSizeH[1]):
            rate = MaxZ / FeedBinSizeH[1]
            SurfR = (1-rate)*FeedBinSizeR[0] + rate*FeedBinSizeR[1]
        elif(MaxZ < FeedBinSizeH[2]):
            rate = (MaxZ - FeedBinSizeH[1]) / (FeedBinSizeH[2] - FeedBinSizeH[1])
            SurfR = (1-rate)*FeedBinSizeR[1] + rate*FeedBinSizeR[2]
        elif(MaxZ < FeedBinSizeH[3]):
            rate = (MaxZ - FeedBinSizeH[2]) / (FeedBinSizeH[3] - FeedBinSizeH[2])
            SurfR = (1-rate)*FeedBinSizeR[2] + rate*FeedBinSizeR[3]
        dataBoundModified[i,1] = SurfR
    return [np.array(dataTemp), np.array(dataBoundModified)]

def GetFilteredData(dataRaw, dataSize):
    if(st.session_state.Debug):print("[GetFilteredData] 데이터 정제를 시작합니다.")
    # Calculate the Region of Interest (ROI)
    Center = [0, 0]  # 현재는 사용자 변수, 추후 벽 인식 알고리즘 후 변경 예정
    Center[0] = st.session_state.centerPos[0]
    Center[1] = st.session_state.centerPos[1]
    print("Center : ",Center)
    
    Radius = dataSize.mid2.iloc[0] / 2  # 사료통 중 위쪽 통 크기로 관심 영역 결정 (가장 넓은 영역으로 변경 필요)
    dataROI = GetRoIPointCloud(dataRaw, Center, Radius)
    lidar_heights = dataSize.lidar_h.iloc[0]
    # Modified Data
    max_dist = dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0]+dataSize.top_H.iloc[0] - lidar_heights
    Radius = dataSize.mid2.iloc[0]/2
    FeedBinSizeR = [dataSize.bot2.iloc[0]/param.VOXEL_GAP/2, dataSize.mid2.iloc[0]/param.VOXEL_GAP/2,  dataSize.top2.iloc[0]/param.VOXEL_GAP/2,  dataSize.top1.iloc[0]/param.VOXEL_GAP/2]
    FeedBinSizeH = [0, dataSize.bot_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0]+dataSize.top_H.iloc[0]]
    [dataModified, dataBound]  = PointCloudToVoxel(dataROI,max_dist, Radius, FeedBinSizeR, FeedBinSizeH)
    
    return [dataModified, dataBound]

