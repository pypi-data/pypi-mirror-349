# tools.py
from .common import app


import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk
from tkcalendar import Calendar
import warnings
import os

@app.tool()
def get_file_path():
    """
    获取用户输入的Excel文件路径
    返回:
        str: 文件路径
    """
    while True:
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)  # 强制窗口置顶
            file_path = filedialog.askopenfilename(title='选择缺陷数据Excel文件', filetypes=[('Excel文件', '*.xlsx')])
            if not file_path.lower().endswith('.xlsx'):
                print("错误: 请选择.xlsx格式的文件")
                continue
            print(f"您选择的文件是: {file_path}")
            return file_path
        except FileNotFoundError:
            print('文件未找到，请检查路径后重新输入')

@app.tool()
def get_release_date():
    """
    获取用户输入的上市日期
    返回:
        str: 上市日期字符串(YYYY-MM-DD格式)
    """
    def get_date():
        """从日历控件获取日期并关闭窗口"""
        nonlocal selected_date
        selected_date = cal.get_date()
        top.destroy()
    
    while True:
        try:
            # 创建日期选择窗口
            top = tk.Toplevel()
            top.title("选择上市日期")
            top.geometry("400x300+500+200")
            top.attributes('-topmost', True)  # 强制窗口置顶
            selected_date = None
            
            # 添加日历控件
            cal = Calendar(top, selectmode='day', date_pattern='y-mm-dd')
            cal.pack(pady=10)
            
            # 添加确认按钮
            ttk.Button(top, text="确认", command=get_date).pack(pady=5)
            
            # 等待用户选择日期
            top.wait_window()
            
            if selected_date:
                return selected_date  # 直接返回已格式化的日期字符串
            else:
                print('未选择日期，请重新输入')
                continue
                
        except ValueError:
            print('日期格式错误，请重新选择')

@app.tool()
def calculate_defect_stats(file_path, release_date):
    """
    计算缺陷统计数据
    
    参数:
        file_path (str): Excel文件路径
        release_date (datetime/str): 上市日期(YYYY-MM-DD格式字符串或datetime对象)
    
    返回:
        dict: 包含所有统计结果的字典，包含以下键:
            - 文件路径: 输入文件路径
            - 上市日期: 格式化后的日期字符串
            - 总缺陷数: 所有缺陷数量
            - 上市前缺陷数: 上市前发现的缺陷数量
            - 上市前已关闭缺陷数: 上市前已关闭的缺陷数量
            - 上市前缺陷关闭率: 上市前缺陷关闭百分比
            - ... (其他统计指标)
    """
    # 如果release_date是字符串，转换为datetime对象
    if isinstance(release_date, str):
        try:
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
        except ValueError:
            print('错误: 日期格式错误，请使用YYYY-MM-DD格式')
            return None
    try:
        # 读取缺陷数据Excel文件
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            df = pd.read_excel(file_path, engine='openpyxl')
        
        # 新增必填字段检查
        required_columns = ['创建时间(createdDate)', '关闭日期(closedDate)', 
                           '缺陷来源(bugSource)', '代码提交链接(sourceSubmitLink)']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"错误: 缺少必要字段: {', '.join(missing_cols)}")
            return f"错误: 缺少必要字段: {', '.join(missing_cols)}"

        # 统计总缺陷数量
        # 计算DataFrame的行数作为总缺陷数
        defect_count = len(df)
        print(f"总缺陷数: {defect_count}")

        # 统计上市前发现的缺陷数量
        # 1. 将创建时间列转换为datetime格式
        # 2. 筛选创建时间早于上市日期的记录
        df['创建时间(createdDate)'] = pd.to_datetime(df['创建时间(createdDate)'])
        pre_release_defects = df[df['创建时间(createdDate)'] < release_date]
        print(f"上市前缺陷数: {len(pre_release_defects)}")

        # 计算上市前缺陷关闭率
        # 1. 将关闭日期列转换为datetime格式
        # 2. 筛选在上市前创建且关闭的缺陷
        # 3. 计算关闭率 = (已关闭缺陷数 / 上市前总缺陷数) * 100
        # 计算上市前缺陷关闭率
        df['关闭日期(closedDate)'] = pd.to_datetime(df['关闭日期(closedDate)'])
        closed_pre_release_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                                    (df['关闭日期(closedDate)'] < release_date)]
        print(f"上市前已关闭缺陷数: {len(closed_pre_release_defects)}")
        # 新增除零检查
        closure_rate = 0 if len(pre_release_defects) == 0 else \
            len(closed_pre_release_defects) / len(pre_release_defects) * 100
        print(f"上市前缺陷关闭率: {closure_rate:.2f}%")

        # 统计上市前已解决缺陷数量
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 代码提交链接不为空
        resolved_pre_release_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                                        (df['代码提交链接(sourceSubmitLink)'].notna())]
        print(f"上市前已解决缺陷数: {len(resolved_pre_release_defects)}")

        # 计算上市前缺陷解决率
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 代码提交链接不为空
        resolved_pre_release_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                                        (df['代码提交链接(sourceSubmitLink)'].notna())]
        resolution_rate = len(resolved_pre_release_defects) / len(pre_release_defects) * 100
        print(f"上市前缺陷解决率: {resolution_rate:.2f}%")

        # 统计上市前试用阶段发现的缺陷数量
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 缺陷来源为外部试用或内部试用
        trial_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                        ((df['缺陷来源(bugSource)'] == '外部试用（During outside user trail）') | 
                        (df['缺陷来源(bugSource)'] == '内部试用（During internal test team user trail）'))]
        print(f"上市前试用缺陷数: {len(trial_defects)}")

        # 统计上市前已关闭试用缺陷数量
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 缺陷来源为试用类型
        # 3. 关闭日期早于上市日期
        closed_trial_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                                ((df['缺陷来源(bugSource)'] == '外部试用（During outside user trail）') | 
                                (df['缺陷来源(bugSource)'] == '内部试用（During internal test team user trail）')) &
                                (df['关闭日期(closedDate)'] < release_date)]
        print(f"上市前已关闭试用缺陷数: {len(closed_trial_defects)}")

        # 计算上市前试用缺陷关闭率
        # 1. 筛选在上市前创建且关闭的试用缺陷
        # 2. 计算关闭率 = (已关闭试用缺陷数 / 上市前试用总缺陷数) * 100
        trial_closure_rate = len(closed_trial_defects) / len(trial_defects) * 100
        print(f"上市前试用缺陷关闭率: {trial_closure_rate:.2f}%")

        # 统计上市前已解决试用缺陷数量
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 缺陷来源为试用类型
        # 3. 代码提交链接不为空
        resolved_trial_defects = df[(df['创建时间(createdDate)'] < release_date) & 
                                ((df['缺陷来源(bugSource)'] == '外部试用（During outside user trail）') | 
                                (df['缺陷来源(bugSource)'] == '内部试用（During internal test team user trail）')) &
                                (df['代码提交链接(sourceSubmitLink)'].notna())]
        print(f"上市前已解决试用缺陷数: {len(resolved_trial_defects)}")

        # 计算上市前试用缺陷解决率
        # 筛选条件:
        # 1. 创建时间早于上市日期
        # 2. 缺陷来源为试用类型
        # 3. 代码提交链接不为空
        trial_resolution_rate = len(resolved_trial_defects) / len(trial_defects) * 100
        print(f"上市前试用缺陷解决率: {trial_resolution_rate:.2f}%")

        # 返回统计结果
        return {
            "文件路径": file_path,
            "上市日期": release_date.strftime('%Y-%m-%d'),
            "总缺陷数": defect_count,
            "上市前缺陷数": len(pre_release_defects),
            "上市前已关闭缺陷数": len(closed_pre_release_defects),
            "上市前缺陷关闭率": closure_rate,
            "上市前已解决缺陷数": len(resolved_pre_release_defects),
            "上市前缺陷解决率": resolution_rate,
            "上市前试用缺陷数": len(trial_defects),
            "上市前已关闭试用缺陷数": len(closed_trial_defects),
            "上市前试用缺陷关闭率": trial_closure_rate,
            "上市前已解决试用缺陷数": len(resolved_trial_defects),
            "上市前试用缺陷解决率": trial_resolution_rate
        }
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到")
        return "错误: 文件未找到"
    except pd.errors.EmptyDataError:
        print(f"错误: 文件 {file_path} 是空的")
        return "错误: 文件为空"
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")
        return f"错误: {str(e)}"