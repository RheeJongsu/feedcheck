import streamlit as st
import plotly.graph_objects as go
import numpy as np
import ctypes as cty
import math
from modules import userParam as param

######################################### Display ######################################### 
## Point로 출력    
def Display3DScatter(fig, df, pointSize=5, colormap='jet', scatterOpcity=1):
    size = pointSize * np.ones((df.shape[0], 1))        
    fig.add_trace(go.Scatter3d(
        x=df[:, 0],
        y=df[:, 1],
        z=df[:, 2],
        mode='markers',  # 점 모드
        marker=dict(    
            size=size,      # 점 크기    
            symbol='circle', # 채워진 원    
            color=df[:, 2],    
            colorscale=colormap,    
            opacity=scatterOpcity  # 불투명 (속이 찬 점)
        )        
    ))        
    fig.update_layout(        
        scene=dict(    
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
            zaxis_title="Z Axis"
        )
    )
    return fig

## Feed 
def Draw3DMeshGrid(fig, df):
    ## Analysis Data
    x = df[:, 0]
    y = df[:, 1]
    z = df[:, 2]
    
    fig.add_trace(go.Mesh3d(
        x=x,
        y=y,
        z=z,
        #colorbar_title='Color Scale',              # 컬러바 제목
        showscale=False,                            # 컬러바 제거
        intensity=z,                                # 색상을 결정하는 값 (intensity)
        colorscale=param.DISPLAY_MESH_COLORMAP,     # jet 컬러맵 적용
        opacity=param.DISPLAY_MESH_ALPHA/100        # 투명도
    ))        
    
    ## Draw MeshGrid
    MinY = int(min(y))
    MaxY = int(max(y))
    MinX = int(min(x))
    MaxX = int(max(x))
    
    for y_val in range(MinY, MaxY + 1):  # Y Direction
        x_curve = []
        y_curve = []
        z_curve = []
        num = 0
        for i in range(df.shape[0]):
            if(y[i] == y_val):
                x_curve.append(x[i])
                y_curve.append(y[i])
                z_curve.append(z[i])
                num = num + 1
        if(num < 3): continue
        fig.add_trace(go.Scatter3d(
            x=x_curve,
            y=y_curve,
            z=z_curve,
            mode='lines',
            line=dict(color=param.DISPLAY_GRID_COLOR, width=param.DISPLAY_GRID_WIDTH),
            opacity=param.DISPLAY_GRID_ALPHA/100,
            showlegend=False
        ))
        
    for x_val in range(MinX, MaxX + 1):   # X Direction
        x_curve = []
        y_curve = []
        z_curve = []
        num = 0
        for i in range(df.shape[0]):
            if(x[i] == x_val):
                x_curve.append(x[i])
                y_curve.append(y[i])
                z_curve.append(z[i])
                num = num + 1
        if(num < 3): continue
        fig.add_trace(go.Scatter3d(
            x=x_curve,
            y=y_curve,
            z=z_curve,
            mode='lines',
            line=dict(color=param.DISPLAY_GRID_COLOR, width=param.DISPLAY_GRID_WIDTH),
            opacity=param.DISPLAY_GRID_ALPHA/100,
            showlegend=False
        ))
    return fig

## Draw FeedBin
def Draw3DFeedBin(fig, FeedBinSizeR, FeedBinSizeH):        
    layer = len(FeedBinSizeR)
    ## Draw Circle Line
    for z_val in range(layer):
        x_curve = []
        y_curve = []
        z_curve = []
        L = FeedBinSizeR[z_val]
        for angle in range(0, 361, 1):
            x_curve.append(L * math.cos(angle * math.pi / 180) + param.VOXEL_SIZE / 2)
            y_curve.append(L * math.sin(angle * math.pi / 180) + param.VOXEL_SIZE / 2)
            z_curve.append(FeedBinSizeH[z_val])
        
        fig.add_trace(go.Scatter3d(
            x=x_curve,
            y=y_curve,
            z=z_curve,
            mode='lines',
            line=dict(color=param.DISPLAY_WALL_COLOR, width=param.DISPLAY_WALL_WIDTH),
            showlegend=False,
            opacity=param.DISPLAY_WALL_ALPHA/100
        ))
    return fig    

def Draw3DFeedBinBoundUp(fig, dataBound, FeedBinSizeR, FeedBinSizeH):
    dAngle = 100 / param.DISPLAY_TOPWALL_DENSITY
    if(param.DISPLAY_TOPWALL_MODE % 10 == 1):
        startAngle = 180
    elif(param.DISPLAY_TOPWALL_MODE % 10 == 2):
        startAngle = 360
    else:
        startAngle = 0

    ## Draw Vertical Line
    NumAngle = int(360 / dAngle)
    for i in range(NumAngle):
        angle = startAngle + i * dAngle
        if((angle > 360) or (angle < 0)): continue # 경계확인
        x_curve = []
        y_curve = []
        z_curve = []
        if(dataBound[int(angle),0] < FeedBinSizeH[1]):
            Larray = [dataBound[int(angle),1], FeedBinSizeR[1], FeedBinSizeR[2], FeedBinSizeR[3]]
            Harray = [dataBound[int(angle),0], FeedBinSizeH[1], FeedBinSizeH[2], FeedBinSizeH[3]]
        elif(dataBound[int(angle),0] < FeedBinSizeH[2]):
            Larray = [dataBound[int(angle),1], FeedBinSizeR[2], FeedBinSizeR[3]]
            Harray = [dataBound[int(angle),0], FeedBinSizeH[2], FeedBinSizeH[3]]
        elif(dataBound[int(angle),0] < FeedBinSizeH[3]):
            Larray = [dataBound[int(angle),1], FeedBinSizeR[3]]
            Harray = [dataBound[int(angle),0], FeedBinSizeH[3]]

        for z_val in range(len(Larray)):
            L = Larray[z_val]
            z_curve.append(Harray[z_val])
            x_curve.append(L * math.cos(angle * math.pi / 180) + param.VOXEL_SIZE / 2)    
            y_curve.append(L * math.sin(angle * math.pi / 180) + param.VOXEL_SIZE / 2)

        fig.add_trace(go.Scatter3d(
            x=x_curve,
            y=y_curve,
            z=z_curve,
            mode='lines',
            line=dict(color=param.DISPLAY_TOPWALL_COLOR, width=param.DISPLAY_TOPWALL_WIDTH),        
            showlegend=False,
            opacity=param.DISPLAY_TOPWALL_ALPHA/100
        ))
    return fig

def Draw3DFeedBinBoundDown(fig, dataBound, FeedBinSizeR, FeedBinSizeH):
    dAngle = 100 / param.DISPLAY_BOTTOMWALL_DENSITY
    if(param.DISPLAY_BOTTOMWALL_MODE % 10 == 1):
        startAngle = 180
    elif(param.DISPLAY_BOTTOMWALL_MODE % 10 == 2):
        startAngle = 360
    else:
        startAngle = 0
    
    ## Draw Vertical Line
    NumAngle = int(360 / dAngle)
    for i in range(NumAngle):
        angle = startAngle + i * dAngle
        if((angle > 360)or(angle < 0)): continue # 경계확인
        x_curve = []
        y_curve = []
        z_curve = []
        if(dataBound[int(angle),0] < FeedBinSizeH[1]):
            Larray = [FeedBinSizeR[0], dataBound[int(angle),1]]
            Harray = [FeedBinSizeH[0], dataBound[int(angle),0]]
        elif(dataBound[int(angle),0] < FeedBinSizeH[2]):
            Larray = [FeedBinSizeR[0], FeedBinSizeR[1], dataBound[int(angle),1]]
            Harray = [FeedBinSizeH[0], FeedBinSizeH[1], dataBound[int(angle),0]]
        elif(dataBound[int(angle),0] < FeedBinSizeH[3]):
            Larray = [FeedBinSizeR[0], FeedBinSizeR[1], FeedBinSizeR[2], dataBound[int(angle),1]]
            Harray = [FeedBinSizeH[0], FeedBinSizeH[1], FeedBinSizeH[2], dataBound[int(angle),0]]

        for z_val in range(len(Larray)):
            L = Larray[z_val]
            z_curve.append(Harray[z_val])
            x_curve.append(L * math.cos(angle * math.pi / 180) + param.VOXEL_SIZE / 2)
            y_curve.append(L * math.sin(angle * math.pi / 180) + param.VOXEL_SIZE / 2)
        fig.add_trace(go.Scatter3d(
            x=x_curve,
            y=y_curve,
            z=z_curve,
            mode='lines',
            line=dict(color=param.DISPLAY_BOTTOMWALL_COLOR, width=param.DISPLAY_BOTTOMWALL_WIDTH),
            showlegend=False,
            opacity=param.DISPLAY_BOTTOMWALL_ALPHA/100
        ))
    return fig

# Graph Option1
def Draw3DLayout(fig, title, XYRange, ZRange, figureHeight = 1000):
     
    if(XYRange is None):
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="X Axis",
                yaxis_title="Y Axis",
                zaxis=dict(
                    title="Z Axis",
                    range=ZRange
                ),
            ),
            height = figureHeight,
            width = 1000
        )
    else: 
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis=dict(
                    title="X Axis",
                    range=XYRange
                ),
                yaxis=dict(
                    title="Y Axis",
                    range=XYRange
                ),
                zaxis=dict(
                    title="Z Axis",
                    range=ZRange
                ),
            ),
            height = figureHeight,
            width = 800
        )
    return fig

# Graph Option2
def Draw3DLayout(fig, title, XYRange, ZRange, height = 600):
     
    if(XYRange is None):
         
        fig.update_layout(            
            title=title,            
            scene=dict(                
                xaxis_title="X Axis",
                yaxis_title="Y Axis",
                zaxis=dict(                    
                    title="Z Axis",                    
                    range=ZRange                
                ),            
            ),
            height = height,
            width = 600
        )
    else:
         
        fig.update_layout(            
            title=title,            
            scene=dict(                
                xaxis=dict(                    
                    title="X Axis",                    
                    range=XYRange                
                ),                
                yaxis=dict(                    
                    title="Y Axis",                    
                    range=XYRange                
                ),               
                zaxis=dict(                    
                    title="Z Axis",                    
                    range=ZRange                
                ),            
            ),
            height = height,
            width = 600  
        )   
        
    return fig


def Draw3DFeedBinAll(fig, dataModified, dataBound, dataSize, VoxelSize, VoxelGap):        
    ## Draw MeshGrid
    meshColorMap = DISPLAY_MESH_COLORMAP   # Mesh의 면 색 (jet, bgr, turbo, rainbow, gist_rainbow, terrain)
    meshOpacity = DISPLAY_MESH_ALPHA/100   # Mesh의 면 투명도
    gridColor = DISPLAY_GRID_COLOR         # Grid의 선에 대한 색
    gridOpacity = DISPLAY_GRID_ALPHA/100   # Grid의 선의 투명도
    fig = Draw3DMeshGrid(fig,dataModified,meshColorMap,meshOpacity,gridColor,gridOpacity)

    ## Draw FeedBin
    FeedBinSizeR = [dataSize.bot2.iloc[0]/VoxelGap[0]/2, dataSize.mid2.iloc[0]/VoxelGap[0]/2,  dataSize.top2.iloc[0]/VoxelGap[0]/2,  dataSize.top1.iloc[0]/VoxelGap[0]/2]
    FeedBinSizeH = [0, dataSize.bot_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0], dataSize.bot_H.iloc[0]+dataSize.mid_H.iloc[0]+dataSize.top_H.iloc[0]] #Height
    FeedBinWallColor = DISPLAY_WALL_COLOR # Wall Color
    FeedBinWallOpacity = DISPLAY_WALL_ALPHA/100     # Wall Opacity
    FeedBinWallDencity = DISPLAY_WALL_DENSITY        # Wall Dencity 10% - 200%
    FeedBinWallLineWidth = 10
    FeedBinTopWallLineWidth = 1
    FeedBinFeedDencity = DISPLAY_FEED_DENSITY        # Wall Dencity 10% - 200%
    mode = 0                        #0: Full Wall, 1: Half wall, 2: None
    fig = Draw3DFeedBin(fig, FeedBinSizeR, FeedBinSizeH, FeedBinWallColor, FeedBinWallOpacity, VoxelSize, FeedBinWallLineWidth)
    fig = Draw3DFeedBinBoundUp(fig, dataBound, FeedBinSizeR, FeedBinSizeH, FeedBinWallColor, FeedBinWallOpacity, FeedBinWallDencity, VoxelSize, FeedBinTopWallLineWidth, mode)
    FeedBinWallColor = DISPLAY_FEED_COLOR
    fig = Draw3DFeedBinBoundDown(fig, dataBound, FeedBinSizeR, FeedBinSizeH, FeedBinWallColor, FeedBinWallOpacity, FeedBinFeedDencity, VoxelSize, FeedBinWallLineWidth, mode)
    ## Draw Option
    z = dataModified[:,2]
    XYdrawRange = [20, 80]  ## 잘보이는 값을 수동으로 찾음 24.12.24
    ZdrawRange = [0, FeedBinSizeH[3]]
    Draw3DLayout(fig, "3D Mesh with Gridlines", XYdrawRange, ZdrawRange, 1000)  #관심영역 확대하여 출력
    return fig

def Draw3DFeedAll(fig, dataModified):        
    ## Draw MeshGrid
    meshColorMap = DISPLAY_MESH_COLORMAP   # Mesh의 면 색 (jet, bgr, turbo, rainbow, gist_rainbow, terrain)
    meshOpacity = DISPLAY_MESH_ALPHA/100   # Mesh의 면 투명도
    gridColor = DISPLAY_GRID_COLOR         # Grid의 선에 대한 색
    gridOpacity = DISPLAY_GRID_ALPHA/100   # Grid의 선의 투명도
    fig = Draw3DMeshGrid(fig,dataModified,meshColorMap,meshOpacity,gridColor,gridOpacity)

    ## Draw Option
    z = dataModified[:,2]
    MaxZ = int(max(z))
    MinZ = int(min(z))
    ZdrawRange = [1.5*MinZ - 0.5 * MaxZ, 1.5 * MaxZ - 0.5 * MinZ]
    XYdrawRange = None
    figureHeight = 1000 #1000px
    Draw3DLayout(fig, "3D Mesh with Gridlines", XYdrawRange, ZdrawRange, figureHeight)  #관심영역 확대하여 출력
    return fig