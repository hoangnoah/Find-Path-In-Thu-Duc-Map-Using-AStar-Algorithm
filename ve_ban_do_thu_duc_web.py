from math import atan2, degrees
import streamlit as st
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import pandas as pd
from search import *

st.set_page_config(layout= 'centered', initial_sidebar_state='expanded')
st.sidebar.image('thuducmap_icon.png',width=230)
st.sidebar.header('Tìm kiếm đường đi')

thuduc_map = UndirectedGraph(dict(
    nga_tu_thu_duc = dict(itfix=530, dh_spkt=200, pvoil_binh_tho=1400),
    itfix = dict(nga_tu_thu_duc=530, tank_coffee=150),
    tank_coffee = dict(itfix=150, dh_spkt=460, sam_rest=163),
    dh_spkt = dict(nga_tu_thu_duc=200, tank_coffee=460, pvoil_4=453),
    sam_rest=dict(tank_coffee=163, pvoil_4=530, bcoffee=150),
    pvoil_4 = dict(dh_spkt=453, sam_rest=530, nha_thieu_nhi=110),
    bcoffee = dict(sam_rest=150, vincom=550, the_gioi_di_dong=1120),
    vincom = dict(bcoffee=550, nha_thieu_nhi=210, cao_dang_cong_nghe=780),
    the_gioi_di_dong = dict(bcoffee=1120, cho_thu_duc=1240),
    pvoil_binh_tho = dict(nga_tu_thu_duc=1400, chua_mot_cot=740),
    chua_mot_cot = dict(pvoil_binh_tho=740, nha_thieu_nhi=915, cao_dang_cong_nghe=920),
    nha_thieu_nhi = dict(pvoil_4=110, vincom=210, chua_mot_cot=915),
    cao_dang_cong_nghe = dict(vincom=780, chua_mot_cot=920, cho_thu_duc=400),
    cho_thu_duc = dict(the_gioi_di_dong=1240, cao_dang_cong_nghe=400)))

thuduc_map.locations = dict(
    nga_tu_thu_duc=(290, 500), itfix=(160, 467), tank_coffee=(168, 429), dh_spkt=(266, 425), 
    sam_rest=(162, 395), pvoil_4=(262, 344), bcoffee=(145, 365), vincom=(237, 275), 
    the_gioi_di_dong=(10, 220), pvoil_binh_tho=(490, 350), chua_mot_cot=(403, 207),  
    nha_thieu_nhi=(255, 315), cao_dang_cong_nghe=(226, 130), cho_thu_duc=(221, 28))

location_name = dict(
    nga_tu_thu_duc=(-25, -12), itfix=(-100, -15), tank_coffee=(-100, 10),
    dh_spkt=(3, 37), sam_rest=(-95, 0), pvoil_4=(10, 5),
    bcoffee=(-60, 0), vincom=(10, 20), the_gioi_di_dong=(10, 5),
    pvoil_binh_tho=(10, 0), chua_mot_cot=(10, 25), nha_thieu_nhi=(10, 5),
    cao_dang_cong_nghe=(10, 30), cho_thu_duc=(-40, 25))

respectively_name = {
    "nga_tu_thu_duc": "Ngã tư Thủ Đức",
    "itfix": "Sửa chữa laptop ITFIX",
    "tank_coffee": "Tank ice-cream \n    coffee",
    "dh_spkt": "Đại học Sư phạm \nKĩ thuật Tp HCM",
    "sam_rest": "Quán ốc Sam",
    "pvoil_4": "PVOIL số 4",
    "bcoffee": "BCoffee",
    "vincom": "Vincom \nThủ đức",
    "the_gioi_di_dong": "Thế giới di động",
    "pvoil_binh_tho": "PVOIL Bình Thọ",
    "chua_mot_cot": "Chùa một cột \nNam Thiên Nhất Trụ",
    "nha_thieu_nhi": "Nhà thiếu nhi Tp Thủ Đức",
    "cao_dang_cong_nghe": "Trường Cao đẳng Công nghệ \nThủ Đức",
    "cho_thu_duc": "Chợ Thủ Đức"
}

map_locations = thuduc_map.locations
graph_dict = thuduc_map.graph_dict

lst_locations = []
for location in location_name:
    lst_locations.append(location)

xmin, xmax, ymin, ymax = 10, 480, 28, 480

def street_name(location1, location2):
    street_name_dict = {
        ('itfix', 'nga_tu_thu_duc'): 'Đ. Lê Văn Chí',
        ('the_gioi_di_dong', 'bcoffee'): 'Đ. Hoàng Diệu 2',
        ('tank_coffee', 'dh_spkt'): 'Đường số 7',
        ('sam_rest', 'pvoil_4'): 'Đường số 6',
        ('bcoffee', 'vincom'): 'Tô Vĩnh Diện',
        ('the_gioi_di_dong', 'cho_thu_duc'): 'Đ. Kha Vạn Cân',
        ('vincom', 'cao_dang_cong_nghe'): 'Đ. Võ Văn Ngân',
        ('nga_tu_thu_duc', 'pvoil_binh_tho'): 'Đ. Nguyễn Văn Bá',
        ('chua_mot_cot', 'pvoil_binh_tho'): 'Đ. Đặng Văn Bi',
        ('nha_thieu_nhi', 'chua_mot_cot'): 'Đ. Dân Chủ'
    }
    if (location1, location2) in street_name_dict:
        return street_name_dict[(location1, location2)]

def display_path(thuduc_map, lst_path):
    # Tạo list chứa dữ liệu cho DataFrame
    data = []
    total_distance = 0
    for i in range(len(lst_path) - 1):
        current_location = lst_path[i].state
        next_location = lst_path[i + 1].state
        distance = thuduc_map.get(current_location, next_location)
        total_distance += distance
        start = ' '.join(respectively_name[current_location].split())
        dest = ' '.join(respectively_name[next_location].split())
        data.append({
            "STT": i+1,
            "Chặng": f"{start} - {dest}",
            "Khoảng cách": f"{distance}m",
        })
    data.append({
        "STT" : "",
        "Chặng": "Tổng quãng đường",
        "Khoảng cách": f"{total_distance}m",
    })
    st.sidebar.subheader("Danh sách các chặng ")
    df = pd.DataFrame(data)
    pd.set_option('display.max_colwidth', None)
    st.sidebar.data_editor(df, width=None, hide_index=True)
    print(df)

def ve_mui_ten(b, a, tx, ty):
    p_mui_ten = [(0,0,1), (-20,10,1), (-15,0,1), (-20,-10,1)]
    p_mui_ten_ma_tran = [np.array([[0],[0],[1]],np.float32),
                            np.array([[-20],[10],[1]],np.float32),
                            np.array([[-15],[0],[1]],np.float32),
                            np.array([[-20],[-10],[1]],np.float32)]

    # Tạo ma trận dời (tịnh tiến) - translate
    M1 = np.array([[1, 0, tx], 
                    [0, 1, ty], 
                    [0, 0, 1]], np.float32)

    # Tạo ma trận quay - rotation
    theta = np.arctan2(b, a)
    M2 = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta),  np.cos(theta), 0],
                    [     0,             0,        1]], np.float32)

    M = np.matmul(M1, M2)

    q_mui_ten = []

    for p in p_mui_ten_ma_tran:
        q = np.matmul(M, p)
        q_mui_ten.append([q[0,0], q[1,0]])
    return q_mui_ten 

def ve_ban_do():
    fig, ax = plt.subplots()
    ax.axis([xmin-70, xmax+180, ymin-70, ymax+70])

    for key in graph_dict:
        location = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        diem, = ax.plot(x0, y0, 'rs')

        dx = location_name[key][0]
        dy = location_name[key][1]
        ten = ax.text(x0+dx, y0-dy, respectively_name[key], fontsize=6)

        for neighbor in location:
            x1 = map_locations[neighbor][0]
            y1 = map_locations[neighbor][1]
            doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')

            angle = degrees(atan2(y1 - y0, x1 - x0))
            mid_x = (x0 + x1) / 2 + 12
            mid_y = (y0 + y1) / 2 + 6
            street_name_key_neighbor = street_name(key, neighbor)
            plt.text(mid_x, mid_y, street_name_key_neighbor, fontsize=5,
                     rotation=angle, rotation_mode='anchor', ha='center', va='center')

    return fig

if 'lst_path' not in st.session_state:
    st.session_state['lst_path'] = []
if "flag_anim" not in st.session_state:
    st.session_state["flag_anim"] = False
if st.session_state["flag_anim"] == False:
    if "flag_ve_ban_do" not in st.session_state:
        st.session_state["flag_ve_ban_do"] = True
        fig = ve_ban_do()
        st.session_state['fig'] = fig
        st.pyplot(fig)
        print(st.session_state["flag_ve_ban_do"])
        print('Vẽ bản đồ lần đầu')
    else:
        if st.session_state["flag_ve_ban_do"] == False:
            st.session_state["flag_ve_ban_do"] = True
            fig = ve_ban_do()
            st.session_state['fig'] = fig
            st.pyplot(fig)
        else:
            print('Đã vẽ bản đồ')
            st.pyplot(st.session_state['fig'])

    lst_location = []
    for location in location_name:
        lst_location.append(respectively_name[location])

    start_location_name = st.sidebar.selectbox('Chọn địa điểm bắt đầu:', lst_location)
    start_location = next(key for key, value in respectively_name.items() if value == start_location_name)
    dest_location_name = st.sidebar.selectbox('Chọn địa điểm đích:', lst_location)
    dest_location = next(key for key, value in respectively_name.items() if value == dest_location_name)

    st.session_state['start_location'] = start_location
    st.session_state['dest_location'] = dest_location

    col3, col4= st.sidebar.columns(2)

    if col3.button('Đường đi'):
        thuduc_problem = GraphProblem(start_location, dest_location, thuduc_map)
        c = astar_search(thuduc_problem)
        lst_path = c.path()
        st.session_state['lst_path'] = lst_path

        path_locations = {}
        for data in lst_path:
            location = data.state
            path_locations[location] = map_locations[location]

        lst_path_location_x = []
        lst_path_location_y = []

        for location in path_locations:
            lst_path_location_x.append(path_locations[location][0])
            lst_path_location_y.append(path_locations[location][1])

        fig, ax = plt.subplots()
        ax.axis([xmin-70, xmax+180, ymin-70, ymax+70])

        for key in graph_dict:
            # Vẽ lại
            location = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 'rs')

            dx = location_name[key][0]
            dy = location_name[key][1]
            ten = ax.text(x0+dx, y0-dy, respectively_name[key], fontsize=6)

            for neighbor in location:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')

                angle = degrees(atan2(y1 - y0, x1 - x0))
                mid_x = (x0 + x1) / 2 + 12
                mid_y = (y0 + y1) / 2 + 7
                street_name_key_neighbor = street_name(key, neighbor)

                plt.text(mid_x, mid_y, street_name_key_neighbor, fontsize=5,
                        rotation=angle, rotation_mode='anchor', ha='center', va='center')

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'g')
            
        st.session_state['fig'] = fig
        st.rerun()

    if col4.button('Bắt đầu'):
        start_location = st.session_state['start_location']
        dest_location = st.session_state['dest_location']

        thuduc_problem = GraphProblem(start_location, dest_location, thuduc_map)
        c = astar_search(thuduc_problem)
        lst_path = c.path()

        for data in lst_path:
            location = data.state
            print(location, end=' ')
        print()

        path_locations = {}
        for data in lst_path:
            location = data.state
            path_locations[location] = map_locations[location]
        print(path_locations)

        lst_path_location_x = []
        lst_path_location_y = []

        for location in path_locations:
            # Lấy tọa độ x của các điểm tìm được trên đường đi
            lst_path_location_x.append(path_locations[location][0])
            lst_path_location_y.append(path_locations[location][1])

        print(lst_path_location_x)
        print(lst_path_location_y)

        fig, ax = plt.subplots()

        dem = 0

        lst_doan_thang = []
        for key in graph_dict:
            location = graph_dict[key]
            x0 = map_locations[key][0]
            y0 = map_locations[key][1]

            diem, = ax.plot(x0, y0, 'rs')
            lst_doan_thang.append(diem)

            dx = location_name[key][0]
            dy = location_name[key][1]
            ten = ax.text(x0+dx, y0-dy, respectively_name[key], fontsize=6)
            lst_doan_thang.append(ten)

            for neighbor in location:
                x1 = map_locations[neighbor][0]
                y1 = map_locations[neighbor][1]
                doan_thang, = ax.plot([x0, x1], [y0, y1], 'b')
                lst_doan_thang.append(doan_thang)
                dem = dem + 1

                angle = degrees(atan2(y1 - y0, x1 - x0))
                mid_x = (x0 + x1) / 2 + 12
                mid_y = (y0 + y1) / 2 + 7
                street_name_key_neighbor = street_name(key, neighbor)

                plt.text(mid_x, mid_y, street_name_key_neighbor, fontsize=5,
                        rotation=angle, rotation_mode='anchor', ha='center', va='center')

            path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'g')
            lst_doan_thang.append(path_tim_thay)

        N = 11
        d = 100
        lst_vi_tri = []

        L = len(lst_path_location_x)
        for i in range(0, L-1):
            x1 = lst_path_location_x[i]
            y1 = lst_path_location_y[i]
            x2 = lst_path_location_x[i+1]
            y2 = lst_path_location_y[i+1]

            b = y2-y1
            a = x2-x1

            d0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            N0 = int(N*d0/d)
            dt = 1/(N0-1)
            for j in range(0, N0):
                t = j*dt
                x = x1 + (x2-x1)*t
                y = y1 + (y2-y1)*t
                q = ve_mui_ten(b, a, x, y)
                lst_vi_tri.append(q)

        red_polygon, = ax.fill([], [], color='red')

        FRAME = len(lst_vi_tri)

        # Khởi tạo animation và 2 tham số là 2 func init và animate giúp khởi tạo và cập nhật mỗi khung hình (frame)
        def init():
            ax.axis([xmin-70, xmax+180, ymin-70, ymax+70])
            # Trả về nhiều đoạn thẳng và đoạn thẳng tìm được
            return lst_doan_thang, red_polygon

        def animate(i):
            red_polygon.set_xy(lst_vi_tri[i])
            return lst_doan_thang, red_polygon

        anim = FuncAnimation(fig, animate, frames=FRAME,
                             interval=100, init_func=init, repeat=False)

        st.session_state["flag_anim"] = True
        st.session_state['anim'] = anim
        st.rerun()

    display_path(thuduc_map, st.session_state['lst_path'])
        
else:
    if st.session_state["flag_anim"] == True:
        components.html(st.session_state["anim"].to_jshtml(), height=550)
        _, _, col3, _, _ = st.columns(5)
        if col3.button('Reset'):
            st.session_state["flag_anim"] = False
            st.session_state["flag_ve_ban_do"] = False
            st.session_state['lst_path'] = []
            st.rerun()
