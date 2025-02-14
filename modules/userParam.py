import streamlit as st

# 전역 설정 변수 지정 (Initialize 에서 초기값으로 변경함)
# 사용자 정의 값
DISPLAY_SCATTER_POINT_SIZE = 5
DISPLAY_SCATTER_POINT_OPACITY = 1
DISPLAY_SCATTER_COLORMAP = 'jet'

#사료 표면
DISPLAY_MESH_COLORMAP = 'jet'           # Mesh의 면 색 (jet, bgr, turbo, rainbow, gist_rainbow, terrain)
DISPLAY_MESH_ALPHA = 100                # Mesh의 면 투명도   (0-100)

#사표 표면에 격자선
DISPLAY_GRID_COLOR = '#A9A9A9'          # Grid의 선에 대한 색
DISPLAY_GRID_ALPHA = 80                 # Grid의 선의 투명도 (0-100)
DISPLAY_GRID_WIDTH = 10                 # Grid의 선의 두께

#사료통의 가로 원
DISPLAY_WALL_COLOR = '#5B9BD5'
DISPLAY_WALL_ALPHA = 100
DISPLAY_WALL_WIDTH = 2

#사료통 상단 영역
DISPLAY_TOPWALL_COLOR = '#888888'
DISPLAY_TOPWALL_ALPHA = 100             # 통 상단 선 투명도   (0-100)
DISPLAY_TOPWALL_DENSITY = 5             # Wall Dencity 10% - 200%
DISPLAY_TOPWALL_WIDTH = 2               # 통 상단 선 두께
DISPLAY_TOPWALL_MODE = 0                #0: Full Wall, 1: Half wall, 2: None

#사료통 하단 영역
DISPLAY_BOTTOMWALL_COLOR = "#FFD966"
DISPLAY_BOTTOMWALL_ALPHA = 100          # 통 하단 선 투명도   (0-100)
DISPLAY_BOTTOMWALL_DENSITY = 10         # Wall Dencity 10% - 200%
DISPLAY_BOTTOMWALL_WIDTH = 2            # 통 하단 선 두께
DISPLAY_BOTTOMWALL_MODE = 0             #0: Full Wall, 1: Half wall, 2: None

#센서 데이터 관련 변수
MIN_DETECTION_DISTANCE = 1              # 센서 값 중 삭제 할 최소 거리
MAX_DETECTION_DISTANCE = 100000         # 센서 값 중 삭제 할 최대 거리 (측정 불가능 거리) 
MAX_SEARCH_EMPTYDATA = 10               # 데이터 중 빈 값을 채우는 횟수
MIN_NUM_SAMPLEDATA = 100                # 최소 데이터 수

#사료 표면 표현 함수관련 변수
SMOOTH_KERNAL_SIZE = 11                 # Gaussian 커널 크기 (홀수)
SMOOTH_KERNAL_SIGMA = 1                 # 표준 편차

#사료 격자 계산 관련 변수
VOXEL_SIZE = 100                        # 사료 격자의 가로 세로 갯수
VOXEL_GAP = 50                          # 격자 사이의 거리

def Initialize():
    global DISPLAY_SCATTER_POINT_SIZE, DISPLAY_SCATTER_POINT_OPACITY, DISPLAY_SCATTER_COLORMAP
    global DISPLAY_MESH_COLORMAP, DISPLAY_MESH_ALPHA
    global DISPLAY_GRID_COLOR, DISPLAY_GRID_ALPHA, DISPLAY_GRID_WIDTH
    global DISPLAY_WALL_COLOR, DISPLAY_WALL_ALPHA, DISPLAY_WALL_WIDTH
    global DISPLAY_TOPWALL_COLOR, DISPLAY_TOPWALL_ALPHA, DISPLAY_TOPWALL_DENSITY, DISPLAY_TOPWALL_WIDTH, DISPLAY_TOPWALL_MODE
    global DISPLAY_BOTTOMWALL_COLOR, DISPLAY_BOTTOMWALL_ALPHA, DISPLAY_BOTTOMWALL_DENSITY, DISPLAY_BOTTOMWALL_WIDTH, DISPLAY_BOTTOMWALL_MODE
    global MIN_DETECTION_DISTANCE, MAX_DETECTION_DISTANCE, MAX_SEARCH_EMPTYDATA, MIN_NUM_SAMPLEDATA
    global SMOOTH_KERNAL_SIZE, SMOOTH_KERNAL_SIGMA
    global VOXEL_SIZE, VOXEL_GAP

    # 사용자 정의 값
    DISPLAY_SCATTER_POINT_SIZE = 5
    DISPLAY_SCATTER_POINT_OPACITY = 1
    DISPLAY_SCATTER_COLORMAP = 'jet'

    #사료 표면
    DISPLAY_MESH_COLORMAP = 'jet'           # Mesh의 면 색 (jet, bgr, turbo, rainbow, gist_rainbow, terrain)
    DISPLAY_MESH_ALPHA = 100                # Mesh의 면 투명도   (0-100)

    #사표 표면에 격자선
    DISPLAY_GRID_COLOR = '#A9A9A9'          # Grid의 선에 대한 색
    DISPLAY_GRID_ALPHA = 80                 # Grid의 선의 투명도 (0-100)
    DISPLAY_GRID_WIDTH = 10                 # Grid의 선의 두께

    #사료통의 가로 원
    DISPLAY_WALL_COLOR = '#5B9BD5'
    DISPLAY_WALL_ALPHA = 100
    DISPLAY_WALL_WIDTH = 2

    #사료통 상단 영역
    DISPLAY_TOPWALL_COLOR = '#888888'
    DISPLAY_TOPWALL_ALPHA = 100             # 통 상단 선 투명도   (0-100)
    DISPLAY_TOPWALL_DENSITY = 5             # Wall Dencity 10% - 200%
    DISPLAY_TOPWALL_WIDTH = 2               # 통 상단 선 두께
    DISPLAY_TOPWALL_MODE = 0                #0: Full Wall, 1: Half wall, 2: None

    #사료통 하단 영역
    DISPLAY_BOTTOMWALL_COLOR = "#FFD966"
    DISPLAY_BOTTOMWALL_ALPHA = 100          # 통 하단 선 투명도   (0-100)
    DISPLAY_BOTTOMWALL_DENSITY = 10         # Wall Dencity 10% - 200%
    DISPLAY_BOTTOMWALL_WIDTH = 2            # 통 하단 선 두께
    DISPLAY_BOTTOMWALL_MODE = 0             #0: Full Wall, 1: Half wall, 2: None

    #센서 데이터 관련 변수
    MIN_DETECTION_DISTANCE = 1              # 센서 값 중 삭제 할 최소 거리
    MAX_DETECTION_DISTANCE = 100000         # 센서 값 중 삭제 할 최대 거리 (측정 불가능 거리) 
    MAX_SEARCH_EMPTYDATA = 10               # 데이터 중 빈 값을 채우는 횟수
    MIN_NUM_SAMPLEDATA = 100                # 최소 데이터 수

    #사료 표면 표현 함수관련 변수
    SMOOTH_KERNAL_SIZE = 11                 # Gaussian 커널 크기 (홀수)
    SMOOTH_KERNAL_SIGMA = 1                 # 표준 편차

    #사료 격자 계산 관련 변수
    VOXEL_SIZE = 100                        # 사료 격자의 가로 세로 갯수
    VOXEL_GAP = 50                          # 격자 사이의 거리


############# 상수 값 ##############
DISPLAY_COLORMAP_LIST = ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
                    'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
                    'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
                    'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
                    'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
                    'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
                    'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
                    'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
                    'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
                    'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
                    'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
                    'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
                    'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
                    'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
                    'ylorrd']


############# Set ################
def ChageMeshAlpha():
    global DISPLAY_MESH_ALPHA
    value = st.session_state["newMeshAlpha"]
    DISPLAY_MESH_ALPHA = value