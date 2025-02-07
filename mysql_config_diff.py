import pandas as pd
import pymysql
from datetime import date
import tkinter as tk
from tkinter import ttk
import argparse
import os
import sys
import openpyxl

variables_data=[]

def get_conn_info(excel_file):
    try:
        if not os.path.exists(excel_file):  # 파일이 존재하는지 확인
            raise FileNotFoundError(f" {excel_file}")

        df = pd.read_excel(excel_file, engine="openpyxl")
        global data_array
        data_array = df.values.tolist()
        print(data_array)

    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        sys.exit(1)
def get_mysql_connection(host,user,password,port):
    """MySQL 연결을 생성하는 함수"""
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database='information_schema',
        port=port,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
def fetch_data(host,user,password,port):
    conn = None
    try:
        conn=get_mysql_connection(host,user,password,port)
        with conn.cursor() as cursor:
            sql = "select variable_name,variable_value from performance_schema.global_variables"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print(f"MySQL 오류 발생: {e}")
    except Exception as e:
        print(f"일반 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

def show_table(dataframe):
    root = tk.Tk()
    root.title("MySQL Config Diff")
    root.geometry("1500x1000")

    dataframe = dataframe.reset_index()
    dataframe.rename(columns={"index": "Variable Name"}, inplace=True)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # 검색 기능
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side="left")

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)

    # false 색
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[("selected", "#ffcccb")])  # 선택된 행 색상

    # Treeview 위젯 생성
    tree = ttk.Treeview(frame, show="headings")

    # 스크롤
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)

    # 컬럼 설정
    tree["columns"] = list(dataframe.columns)
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")  # 컬럼 폭 설정

    dataframe["is_same"] = dataframe["is_same"].astype(bool)  # is_same
    dataframe = dataframe.sort_values(by="is_same", ascending=True)  # False가 위로 오게 정렬

    def insert_data(filtered_df):
        """Treeview에 데이터 추가하는 함수"""
        tree.delete(*tree.get_children())  # 기존 데이터 삭제
        for row in filtered_df.itertuples(index=False):
            values = row
            is_same = row[-1]  # 마지막 열이 is_same 여부
            tag = "pink" if not is_same else ""  # False면 'pink' 태그 적용
            tree.insert("", "end", values=values, tags=(tag,))
        tree.tag_configure("pink", background="#ffcccb")

    # 초기 데이터 삽입
    insert_data(dataframe)

    def search_variable():
        """검색 기능"""
        search_text = search_entry.get().strip().lower()
        if search_text:
            filtered_df = dataframe[dataframe["Variable Name"].str.lower().str.contains(search_text, na=False)]
        else:
            filtered_df = dataframe  # 검색어 없으면 전체 표시
        insert_data(filtered_df)

    search_button = tk.Button(search_frame, text="Find", command=search_variable)
    search_button.pack(side="left", padx=5)

    # 배치 설정
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(expand=True, fill="both")

    root.mainloop()

def parse_arguments():
    parser = argparse.ArgumentParser(description="MySQL Variables Exporter")
    ## CONNECTION INFO 파일 위치
    # parser.add_argument('--save_path', type=str, required=True,help='Connection Info 엑셀 파일 C:/Users/yunhyeonglee/Desktop/et/connection_info.xlsx')
    parser.add_argument('--save_path', type=str, default="C:/Users/user201203/Desktop/python/mysql_config_diff/connection_list.xlsx",help='저장할 경로 (기본값: C:/Users/username/Desktop/et)')

    return parser.parse_args()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 경로 지정
    variables_data_list = []
    servers = []
    df_list = []

    args = parse_arguments()
    save_path = args.save_path  ## connection_info 엑셀 파일 위치 받기

    conn_info_excel = f"{save_path}"
    get_conn_info(conn_info_excel)

    for i in data_array:
        ip=i[2]
        port=int(i[3])
        variables_data=fetch_data(ip,'lee','Dldbsgud12!',port)
        variables_data.insert(0,{'variable_name':'host_name','variable_value':i[1]})
        variables_data_list.append(variables_data)
        servers.append(i[1])


    for i, data in enumerate(variables_data_list):
        df = pd.DataFrame(data)
        df = df.set_index('variable_name').T  
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)
    final_df = final_df.T  
    first_server_values = final_df.iloc[:, 0]  

    # config 비교
    final_df["is_same"] = final_df.eq(first_server_values, axis=0).all(axis=1)

    today = date.today()
    output_file = f"{save_path}\\{today}_output.xlsx"

    show_table(final_df)