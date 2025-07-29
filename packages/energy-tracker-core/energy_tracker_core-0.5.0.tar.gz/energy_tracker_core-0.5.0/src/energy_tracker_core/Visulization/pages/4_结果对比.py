import streamlit as st
import pandas as pd
import numpy as np
from energy_tracker_core.Visulization.workspace_task import WorkSpace, Task
from scipy import interpolate


st.session_state.language = st.session_state.get("language", "中文")
if st.session_state.language == "中文":
    # 页面配置
    st.set_page_config(
        page_title="结果对比",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 任务结果对比")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    # 辅助函数：对数据进行插值处理
    def interpolate_data(data_series, target_length):
        """
        对数据序列进行插值，使其长度达到目标长度
        """
        # 原始数据的索引
        orig_indices = np.arange(len(data_series))
        # 目标索引
        target_indices = np.linspace(0, len(data_series) - 1, target_length)
        # 创建插值函数
        if len(data_series) > 1:
            f = interpolate.interp1d(orig_indices, data_series, kind='linear')
            # 执行插值
            interpolated_data = f(target_indices)
            return interpolated_data
        else:
            # 如果只有一个数据点，无法进行插值，则复制该值
            return np.full(target_length, data_series.iloc[0])

    # 修复零值的函数
    def fix_zero_values(data_series):
        """
        修复数据序列中的零值，使用临近非零点的平均值进行填充
        
        参数:
            data_series (pd.Series): 待处理的数据序列
        
        返回:
            pd.Series: 处理后的数据序列
        """
        # 创建数据副本
        fixed_data = data_series.copy()
        zero_indices = np.where(fixed_data == 0)[0]
        
        if len(zero_indices) == 0:
            return fixed_data  # 没有零值
        
        # 如果全为零，返回一个很小的值
        if len(zero_indices) == len(fixed_data):
            return pd.Series([1e-6] * len(fixed_data))
        
        for idx in zero_indices:
            # 向前找最近的非零值
            prev_non_zero = None
            for i in range(idx-1, -1, -1):
                if fixed_data.iloc[i] != 0:
                    prev_non_zero = fixed_data.iloc[i]
                    break
            
            # 向后找最近的非零值
            next_non_zero = None
            for i in range(idx+1, len(fixed_data)):
                if fixed_data.iloc[i] != 0:
                    next_non_zero = fixed_data.iloc[i]
                    break
            
            # 使用临近的非零值估计当前零值
            if prev_non_zero is not None and next_non_zero is not None:
                fixed_data.iloc[idx] = (prev_non_zero + next_non_zero) / 2
            elif prev_non_zero is not None:
                fixed_data.iloc[idx] = prev_non_zero
            elif next_non_zero is not None:
                fixed_data.iloc[idx] = next_non_zero
            else:
                # 不应该执行到这里，因为我们已经检查了是否全为零的情况
                fixed_data.iloc[idx] = 1e-6  # 兜底，使用一个很小的非零值
        
        return fixed_data

    # 检查前序工作
    if 'workspace' not in st.session_state:
        st.warning("请先在 CSV 管理页面初始化工作目录。")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("请先在 CSV 管理页面至少选择两个要对比的csv文件。")
        else:
            # 获取所有选中的任务名称
            selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
            selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
            
            if len(selected_names) < 2:
                st.warning("请至少选择两个任务进行对比。")
            else:
                # 获取对应的任务对象
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
                
                # 确保所有任务都分析过
                for task in selected_tasks:
                    if not hasattr(task, 'statistics') or not task.statistics:
                        task.analyse()
                
                # 创建对比数据
                comparison_data = {}
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    
                    # 收集基本统计数据用于对比
                    comparison_data[task_name] = {
                        '问答总数': task.statistics['问答总数'],
                        '总持续时间(秒)': task.statistics['总持续时间(秒)'],
                        '正确率': task.statistics['正确率'],
                        '有效率': task.statistics['有效率'],
                        '平均每次问答时间(秒)': task.statistics['平均每次问答时间(秒)'],
                        'CPU总能耗(Wh)': task.statistics['CPU总能耗(Wh)'],
                        'GPU总能耗(Wh)': task.statistics['GPU总能耗(Wh)'],
                        '总能耗(Wh)': task.statistics['总能耗(Wh)'],
                        'CPU平均每次问答能耗(Wh)': task.statistics['CPU平均每次问答能耗(Wh)'],
                        'GPU平均每次问答能耗(Wh)': task.statistics['GPU平均每次问答能耗(Wh)'],
                        '平均每次问答总能耗(Wh)': task.statistics['平均每次问答总能耗(Wh)'],
                        'CPU平均功率(W)': task.statistics['CPU平均功率(W)'],
                        'GPU平均功率(W)': task.statistics['GPU平均功率(W)'],
                        '总平均功率(W)': task.statistics['总平均功率(W)'],
                    }

                # 转换为DataFrame便于绘图
                comparison_df = pd.DataFrame(comparison_data).T
                
                # 提供不同对比维度的选择
                st.markdown("### 选择对比维度")
                comparison_tabs = st.tabs(["基本指标", "能耗对比", "功率对比", "组合对比"])
                
                with comparison_tabs[0]:
                    st.markdown("#### 基本指标对比")
                    basic_metrics = ['问答总数', '总持续时间(秒)', '正确率', '有效率', '平均每次问答时间(秒)']
                    selected_basic_metrics = st.multiselect(
                        "选择要对比的基本指标", 
                        basic_metrics,
                        default=['问答总数', '正确率']
                    )
                    
                    if selected_basic_metrics:
                        st.bar_chart(comparison_df[selected_basic_metrics])
                
                with comparison_tabs[1]:
                    st.markdown("#### 能耗对比")
                    energy_metrics = ['CPU总能耗(Wh)', 'GPU总能耗(Wh)', '总能耗(Wh)', 
                                'CPU平均每次问答能耗(Wh)', 'GPU平均每次问答能耗(Wh)', '平均每次问答总能耗(Wh)']
                    selected_energy_metrics = st.multiselect(
                        "选择要对比的能耗指标", 
                        energy_metrics,
                        default=['总能耗(Wh)', 'CPU总能耗(Wh)', 'GPU总能耗(Wh)']
                    )
                    
                    if selected_energy_metrics:
                        # 绘制能耗对比图
                        st.bar_chart(comparison_df[selected_energy_metrics])
                        
                        # 提供数据表格查看
                        with st.expander("查看详细数据"):
                            st.dataframe(comparison_df[selected_energy_metrics])
                
                with comparison_tabs[2]:
                    st.markdown("#### 功率对比")
                    power_metrics = ['CPU平均功率(W)', 'GPU平均功率(W)', '总平均功率(W)']
                    selected_power_metrics = st.multiselect(
                        "选择要对比的功率指标", 
                        power_metrics,
                        default=power_metrics
                    )
                    
                    if selected_power_metrics:
                        # 绘制功率对比图
                        st.bar_chart(comparison_df[selected_power_metrics])
                        
                        # 提供数据表格查看
                        with st.expander("查看详细数据"):
                            st.dataframe(comparison_df[selected_power_metrics])
                
                with comparison_tabs[3]:
                    st.markdown("#### 自定义组合对比")
                    all_metrics = basic_metrics + energy_metrics + power_metrics
                    custom_metrics = st.multiselect(
                        "选择要对比的指标", 
                        all_metrics,
                        default=['总能耗(Wh)', '总平均功率(W)', '正确率']
                    )
                    
                    chart_type = st.radio("选择图表类型", ["柱状图", "折线图"], horizontal=True)
                    
                    if custom_metrics:
                        if chart_type == "柱状图":
                            st.bar_chart(comparison_df[custom_metrics])
                        else:
                            st.line_chart(comparison_df[custom_metrics])
                        
                        # 提供数据表格查看
                        with st.expander("查看详细数据"):
                            st.dataframe(comparison_df[custom_metrics])
                
                # 高级对比：时间序列叠加对比
                st.markdown("### 能耗趋势对比")
                trend_tabs = st.tabs(["累计能耗趋势", "单次能耗分布", "实时功率变化"])
                
                with trend_tabs[0]:
                    st.markdown("#### 累计能耗趋势对比")
                    
                    # 设置所有任务统一的标准化点数（100点足够展示趋势）
                    standard_points = 100
                    normalize_method = st.radio(
                        "标准化方法",
                        ["百分比进度", "插值到相同点数"],
                        horizontal=True,
                        help="百分比进度：按任务进度百分比对齐；插值到相同点数：将所有任务重采样到相同点数"
                    )
                    
                    # 是否修复零值
                    fix_zeros = st.checkbox("修复能耗数据中的零值", value=True, 
                                            help="有些问答的时间消耗短于能耗测量的更新周期，导致能耗数据为0。勾选此选项可用临近非零值修复这些数据点")
                    
                    # 创建一个DataFrame存储所有任务的累计能耗
                    energy_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # 获取能耗数据并修复零值
                        total_energy = task.data['total_incremental_energy']
                        cpu_energy = task.data['cpu_incremental_energy']
                        gpu_energy = task.data['gpu_incremental_energy']
                        
                        if fix_zeros:
                            total_energy = fix_zero_values(total_energy)
                            cpu_energy = fix_zero_values(cpu_energy)
                            gpu_energy = fix_zero_values(gpu_energy)
                        
                        # 计算累计能耗
                        total_cumsum = total_energy.cumsum()
                        
                        if normalize_method == "百分比进度":
                            # 创建百分比进度索引
                            progress_pct = np.linspace(0, 100, len(total_cumsum))
                            # 添加到DataFrame
                            task_df = pd.DataFrame({task_name: total_cumsum.values}, index=progress_pct)
                            energy_trend_data = pd.concat([energy_trend_data, task_df], axis=1)
                        else:
                            # 对累计能耗数据进行插值，使所有任务具有相同点数
                            interpolated_cumsum = interpolate_data(total_cumsum, standard_points)
                            # 使用统一的索引添加到DataFrame
                            if energy_trend_data.empty:
                                energy_trend_data = pd.DataFrame(index=range(standard_points))
                            energy_trend_data[task_name] = interpolated_cumsum
                    
                    # 绘制累计能耗对比图
                    st.line_chart(energy_trend_data)
                    
                    with st.expander("查看图表说明"):
                        if normalize_method == "百分比进度":
                            st.markdown("""
                            **累计能耗趋势对比说明：**
                            - X轴代表任务进度百分比，从0%到100%
                            - Y轴代表累计能耗，单位为Wh
                            - 每条线代表一个选中的任务
                            - 斜率越大的部分，表示该阶段能耗增长越快
                            """)
                        else:
                            st.markdown("""
                            **累计能耗趋势对比说明：**
                            - X轴代表标准化的数据点序号（通过插值将不同长度的任务调整为相同点数）
                            - Y轴代表累计能耗，单位为Wh
                            - 每条线代表一个选中的任务
                            - 斜率越大的部分，表示该阶段能耗增长越快
                            - 通过插值处理，可以直接比较不同长度任务的趋势
                            """)
                
                with trend_tabs[1]:
                    st.markdown("#### 单次能耗分布对比")
                    
                    # 单次能耗分布的标准化设置
                    st.write("##### 数据标准化设置")
                    energy_normalize_method = st.radio(
                        "选择标准化方法",
                        ["保持原始点数", "插值到最大点数", "插值到固定点数"],
                        horizontal=True
                    )
                    
                    if energy_normalize_method == "插值到固定点数":
                        fixed_points = st.slider("设置标准化点数", min_value=10, max_value=500, value=100, step=10)
                    
                    # 是否修复零值
                    fix_zeros_dist = st.checkbox("修复能耗数据中的零值", value=True, 
                                            help="有些问答的时间消耗短于能耗测量的更新周期，导致能耗数据为0。勾选此选项可用临近非零值修复这些数据点",
                                            key="fix_zeros_dist")
                    
                    # 为每个任务准备单次能耗数据
                    energy_distribution_data = pd.DataFrame()
                    
                    # 确定目标点数
                    if energy_normalize_method == "插值到最大点数":
                        target_points = max([len(task.data) for task in selected_tasks])
                    elif energy_normalize_method == "插值到固定点数":
                        target_points = fixed_points
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # 获取单次能耗数据并修复零值
                        single_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_dist:
                            single_energy = fix_zero_values(single_energy)
                        
                        if energy_normalize_method == "保持原始点数":
                            # 重置索引为问答序号
                            single_energy = single_energy.reset_index(drop=True)
                            # 添加到DataFrame
                            energy_distribution_data[task_name] = single_energy
                        else:
                            # 对单次能耗数据进行插值
                            interpolated_energy = interpolate_data(single_energy, target_points)
                            # 使用统一的索引添加到DataFrame
                            if energy_distribution_data.empty:
                                energy_distribution_data = pd.DataFrame(index=range(target_points))
                            energy_distribution_data[task_name] = interpolated_energy
                    
                    # 使用折线图展示分布趋势
                    st.line_chart(energy_distribution_data)
                    
                    # 创建分布摘要数据
                    distribution_summary = pd.DataFrame({
                        '任务': [],
                        '最小值': [],
                        '25%分位数': [],
                        '中位数': [],
                        '75%分位数': [],
                        '最大值': [],
                        '平均值': [],
                        '标准差': []
                    })
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        energy_stats = task.data['total_incremental_energy'].describe()
                        
                        new_row = pd.DataFrame({
                            '任务': [task_name],
                            '最小值': [energy_stats['min']],
                            '25%分位数': [energy_stats['25%']],
                            '中位数': [energy_stats['50%']],
                            '75%分位数': [energy_stats['75%']],
                            '最大值': [energy_stats['max']],
                            '平均值': [energy_stats['mean']],
                            '标准差': [energy_stats['std']]
                        })
                        
                        distribution_summary = pd.concat([distribution_summary, new_row])
                    
                    # 显示分布统计摘要
                    st.markdown("##### 能耗分布统计摘要")
                    st.dataframe(distribution_summary)
                    
                    with st.expander("查看图表说明"):
                        if energy_normalize_method == "保持原始点数":
                            st.markdown("""
                            **单次能耗分布对比说明：**
                            - X轴代表问答序号
                            - Y轴代表单次能耗，单位为Wh
                            - 每条线代表一个选中的任务
                            - 注意：各任务行数不同，直接比较时要考虑这一点
                            - 统计摘要表格提供了各任务能耗分布的关键统计指标
                            """)
                        else:
                            st.markdown("""
                            **单次能耗分布对比说明：**
                            - X轴代表标准化后的问答序号
                            - Y轴代表单次能耗，单位为Wh
                            - 每条线代表一个选中的任务
                            - 通过插值处理，所有任务具有相同的点数，便于直接比较
                            - 统计摘要表格提供了各任务能耗分布的关键统计指标（基于原始数据）
                            """)
                        
                with trend_tabs[2]:
                    st.markdown("#### 实时功率变化对比")
                    
                    # 功率变化的标准化设置
                    power_normalize_method = st.radio(
                        "功率对比标准化方法",
                        ["百分比进度", "插值到相同点数"],
                        horizontal=True
                    )
                    
                    if power_normalize_method == "插值到相同点数":
                        power_points = st.slider("功率对比标准化点数", min_value=10, max_value=500, value=100, step=10)
                    
                    # 是否修复零值
                    fix_zeros_power = st.checkbox("修复能耗数据中的零值", value=True, 
                                                help="有些问答的时间消耗短于能耗测量的更新周期，导致能耗数据为0。勾选此选项可用临近非零值修复这些数据点",
                                                key="fix_zeros_power")
                    
                    # 计算并绘制实时功率变化
                    power_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # 计算时间间隔（秒）
                        task.data['start_time'] = pd.to_datetime(task.data['start_time'])
                        task.data['end_time'] = pd.to_datetime(task.data['end_time'])
                        task.data['duration'] = (task.data['end_time'] - task.data['start_time']).dt.total_seconds()
                        
                        # 获取能耗数据并修复零值
                        total_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_power:
                            total_energy = fix_zero_values(total_energy)
                        
                        # 计算实时功率 (W = J/s, 能耗单位为Wh，需要转换为W)
                        # 功率 = 能耗(Wh) * 3600 / 持续时间(s)
                        power_series = total_energy * 3600 / task.data['duration']
                        
                        # 处理零值或inf值（当持续时间接近0时可能出现）
                        power_series = power_series.replace([np.inf, -np.inf], np.nan).fillna(power_series.mean())
                        
                        if power_normalize_method == "百分比进度":
                            # 创建百分比进度索引
                            progress_pct = np.linspace(0, 100, len(power_series))
                            # 添加到DataFrame
                            task_df = pd.DataFrame({task_name: power_series.values}, index=progress_pct)
                            power_trend_data = pd.concat([power_trend_data, task_df], axis=1)
                        else:
                            # 对功率数据进行插值
                            interpolated_power = interpolate_data(power_series, power_points)
                            # 使用统一的索引添加到DataFrame
                            if power_trend_data.empty:
                                power_trend_data = pd.DataFrame(index=range(power_points))
                            power_trend_data[task_name] = interpolated_power
                    
                    # 绘制实时功率对比图
                    st.line_chart(power_trend_data)
                    
                    with st.expander("查看图表说明"):
                        if power_normalize_method == "百分比进度":
                            st.markdown("""
                            **实时功率变化对比说明：**
                            - X轴代表任务进度百分比，从0%到100%
                            - Y轴代表实时功率，单位为W (瓦特)
                            - 每条线代表一个选中的任务
                            - 峰值表示该时刻能耗强度最高
                            """)
                        else:
                            st.markdown("""
                            **实时功率变化对比说明：**
                            - X轴代表标准化后的数据点序号
                            - Y轴代表实时功率，单位为W (瓦特)
                            - 每条线代表一个选中的任务
                            - 通过插值处理，所有任务具有相同的点数，便于直接比较
                            - 峰值表示该时刻能耗强度最高
                            """)

                            
elif st.session_state.language == "English":
    # Page configuration
    st.set_page_config(
        page_title="Result Comparison",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Task Result Comparison")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    # Helper function: Interpolate data
    def interpolate_data(data_series, target_length):
        """
        Interpolate data series to reach target length
        """
        # Original data indices
        orig_indices = np.arange(len(data_series))
        # Target indices
        target_indices = np.linspace(0, len(data_series) - 1, target_length)
        # Create interpolation function
        if len(data_series) > 1:
            f = interpolate.interp1d(orig_indices, data_series, kind='linear')
            # Perform interpolation
            interpolated_data = f(target_indices)
            return interpolated_data
        else:
            # If only one data point, cannot interpolate, so duplicate the value
            return np.full(target_length, data_series.iloc[0])

    # Function to fix zero values
    def fix_zero_values(data_series):
        """
        Fix zero values in data series by filling with average of nearby non-zero points
        
        Parameters:
            data_series (pd.Series): Data series to process
        
        Returns:
            pd.Series: Processed data series
        """
        # Create data copy
        fixed_data = data_series.copy()
        zero_indices = np.where(fixed_data == 0)[0]
        
        if len(zero_indices) == 0:
            return fixed_data  # No zero values
        
        # If all values are zero, return a small value
        if len(zero_indices) == len(fixed_data):
            return pd.Series([1e-6] * len(fixed_data))
        
        for idx in zero_indices:
            # Find the nearest non-zero value going backwards
            prev_non_zero = None
            for i in range(idx-1, -1, -1):
                if fixed_data.iloc[i] != 0:
                    prev_non_zero = fixed_data.iloc[i]
                    break
            
            # Find the nearest non-zero value going forwards
            next_non_zero = None
            for i in range(idx+1, len(fixed_data)):
                if fixed_data.iloc[i] != 0:
                    next_non_zero = fixed_data.iloc[i]
                    break
            
            # Estimate current zero value using nearby non-zero values
            if prev_non_zero is not None and next_non_zero is not None:
                fixed_data.iloc[idx] = (prev_non_zero + next_non_zero) / 2
            elif prev_non_zero is not None:
                fixed_data.iloc[idx] = prev_non_zero
            elif next_non_zero is not None:
                fixed_data.iloc[idx] = next_non_zero
            else:
                # Shouldn't execute here as we've already checked if all values are zero
                fixed_data.iloc[idx] = 1e-6  # Fallback, use a small non-zero value
        
        return fixed_data

    # Check prerequisites
    if 'workspace' not in st.session_state:
        st.warning("Please initialize the workspace directory in the CSV Management page first.")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("Please select at least two CSV files to compare in the CSV Management page.")
        else:
            # Get all selected task names
            selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
            selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
            
            if len(selected_names) < 2:
                st.warning("Please select at least two tasks to compare.")
            else:
                # Get corresponding task objects
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
                
                # Ensure all tasks have been analyzed
                for task in selected_tasks:
                    if not hasattr(task, 'statistics') or not task.statistics:
                        task.analyse()
                
                # Create comparison data
                comparison_data = {}
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    
                    # Collect basic statistics for comparison
                    comparison_data[task_name] = {
                        'Total Q&A Count': task.statistics['问答总数'],
                        'Total Duration (sec)': task.statistics['总持续时间(秒)'],
                        'Accuracy Rate': task.statistics['正确率'],
                        'Effectiveness Rate': task.statistics['有效率'],
                        'Average Q&A Time (sec)': task.statistics['平均每次问答时间(秒)'],
                        'CPU Total Energy (Wh)': task.statistics['CPU总能耗(Wh)'],
                        'GPU Total Energy (Wh)': task.statistics['GPU总能耗(Wh)'],
                        'Total Energy (Wh)': task.statistics['总能耗(Wh)'],
                        'CPU Avg Energy per Q&A (Wh)': task.statistics['CPU平均每次问答能耗(Wh)'],
                        'GPU Avg Energy per Q&A (Wh)': task.statistics['GPU平均每次问答能耗(Wh)'],
                        'Total Avg Energy per Q&A (Wh)': task.statistics['平均每次问答总能耗(Wh)'],
                        'CPU Avg Power (W)': task.statistics['CPU平均功率(W)'],
                        'GPU Avg Power (W)': task.statistics['GPU平均功率(W)'],
                        'Total Avg Power (W)': task.statistics['总平均功率(W)'],
                    }

                # Convert to DataFrame for plotting
                comparison_df = pd.DataFrame(comparison_data).T
                
                # Provide selection for different comparison dimensions
                st.markdown("### Select Comparison Dimension")
                comparison_tabs = st.tabs(["Basic Metrics", "Energy Comparison", "Power Comparison", "Combined Comparison"])
                
                with comparison_tabs[0]:
                    st.markdown("#### Basic Metrics Comparison")
                    basic_metrics = ['Total Q&A Count', 'Total Duration (sec)', 'Accuracy Rate', 'Effectiveness Rate', 'Average Q&A Time (sec)']
                    selected_basic_metrics = st.multiselect(
                        "Select basic metrics to compare", 
                        basic_metrics,
                        default=['Total Q&A Count', 'Accuracy Rate']
                    )
                    
                    if selected_basic_metrics:
                        st.bar_chart(comparison_df[selected_basic_metrics])
                
                with comparison_tabs[1]:
                    st.markdown("#### Energy Comparison")
                    energy_metrics = ['CPU Total Energy (Wh)', 'GPU Total Energy (Wh)', 'Total Energy (Wh)', 
                                'CPU Avg Energy per Q&A (Wh)', 'GPU Avg Energy per Q&A (Wh)', 'Total Avg Energy per Q&A (Wh)']
                    selected_energy_metrics = st.multiselect(
                        "Select energy metrics to compare", 
                        energy_metrics,
                        default=['Total Energy (Wh)', 'CPU Total Energy (Wh)', 'GPU Total Energy (Wh)']
                    )
                    
                    if selected_energy_metrics:
                        # Draw energy comparison chart
                        st.bar_chart(comparison_df[selected_energy_metrics])
                        
                        # Provide data table view
                        with st.expander("View Detailed Data"):
                            st.dataframe(comparison_df[selected_energy_metrics])
                
                with comparison_tabs[2]:
                    st.markdown("#### Power Comparison")
                    power_metrics = ['CPU Avg Power (W)', 'GPU Avg Power (W)', 'Total Avg Power (W)']
                    selected_power_metrics = st.multiselect(
                        "Select power metrics to compare", 
                        power_metrics,
                        default=power_metrics
                    )
                    
                    if selected_power_metrics:
                        # Draw power comparison chart
                        st.bar_chart(comparison_df[selected_power_metrics])
                        
                        # Provide data table view
                        with st.expander("View Detailed Data"):
                            st.dataframe(comparison_df[selected_power_metrics])
                
                with comparison_tabs[3]:
                    st.markdown("#### Custom Combined Comparison")
                    all_metrics = basic_metrics + energy_metrics + power_metrics
                    custom_metrics = st.multiselect(
                        "Select metrics to compare", 
                        all_metrics,
                        default=['Total Energy (Wh)', 'Total Avg Power (W)', 'Accuracy Rate']
                    )
                    
                    chart_type = st.radio("Select chart type", ["Bar Chart", "Line Chart"], horizontal=True)
                    
                    if custom_metrics:
                        if chart_type == "Bar Chart":
                            st.bar_chart(comparison_df[custom_metrics])
                        else:
                            st.line_chart(comparison_df[custom_metrics])
                        
                        # Provide data table view
                        with st.expander("View Detailed Data"):
                            st.dataframe(comparison_df[custom_metrics])
                
                # Advanced comparison: Time series overlay comparison
                st.markdown("### Energy Trend Comparison")
                trend_tabs = st.tabs(["Cumulative Energy Trend", "Single Q&A Energy Distribution", "Real-time Power Change"])
                
                with trend_tabs[0]:
                    st.markdown("#### Cumulative Energy Trend Comparison")
                    
                    # Set a unified standard number of points for all tasks (100 points is enough to show the trend)
                    standard_points = 100
                    normalize_method = st.radio(
                        "Normalization Method",
                        ["Percentage Progress", "Interpolate to Same Points"],
                        horizontal=True,
                        help="Percentage Progress: align by task progress percentage; Interpolate to Same Points: resample all tasks to the same number of points"
                    )
                    
                    # Whether to fix zero values
                    fix_zeros = st.checkbox("Fix zero values in energy data", value=True, 
                                            help="Some Q&As take less time than the energy measurement update cycle, resulting in zero energy data. Check this option to fix these data points using nearby non-zero values")
                    
                    # Create a DataFrame to store cumulative energy for all tasks
                    energy_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Get energy data and fix zero values
                        total_energy = task.data['total_incremental_energy']
                        cpu_energy = task.data['cpu_incremental_energy']
                        gpu_energy = task.data['gpu_incremental_energy']
                        
                        if fix_zeros:
                            total_energy = fix_zero_values(total_energy)
                            cpu_energy = fix_zero_values(cpu_energy)
                            gpu_energy = fix_zero_values(gpu_energy)
                        
                        # Calculate cumulative energy
                        total_cumsum = total_energy.cumsum()
                        
                        if normalize_method == "Percentage Progress":
                            # Create percentage progress index
                            progress_pct = np.linspace(0, 100, len(total_cumsum))
                            # Add to DataFrame
                            task_df = pd.DataFrame({task_name: total_cumsum.values}, index=progress_pct)
                            energy_trend_data = pd.concat([energy_trend_data, task_df], axis=1)
                        else:
                            # Interpolate cumulative energy data to have the same number of points for all tasks
                            interpolated_cumsum = interpolate_data(total_cumsum, standard_points)
                            # Add to DataFrame with unified index
                            if energy_trend_data.empty:
                                energy_trend_data = pd.DataFrame(index=range(standard_points))
                            energy_trend_data[task_name] = interpolated_cumsum
                    
                    # Draw cumulative energy comparison chart
                    st.line_chart(energy_trend_data)
                    
                    with st.expander("View Chart Explanation"):
                        if normalize_method == "Percentage Progress":
                            st.markdown("""
                            **Cumulative Energy Trend Comparison Explanation:**
                            - X-axis represents task progress percentage, from 0% to 100%
                            - Y-axis represents cumulative energy, in Wh
                            - Each line represents a selected task
                            - Sections with steeper slope indicate faster energy consumption during that stage
                            """)
                        else:
                            st.markdown("""
                            **Cumulative Energy Trend Comparison Explanation:**
                            - X-axis represents standardized data point number (adjusted through interpolation to make tasks of different lengths have the same number of points)
                            - Y-axis represents cumulative energy, in Wh
                            - Each line represents a selected task
                            - Sections with steeper slope indicate faster energy consumption during that stage
                            - Through interpolation processing, the trends of tasks with different lengths can be directly compared
                            """)
                
                with trend_tabs[1]:
                    st.markdown("#### Single Q&A Energy Distribution Comparison")
                    
                    # Single energy distribution normalization settings
                    st.write("##### Data Normalization Settings")
                    energy_normalize_method = st.radio(
                        "Select normalization method",
                        ["Keep Original Points", "Interpolate to Maximum Points", "Interpolate to Fixed Points"],
                        horizontal=True
                    )
                    
                    if energy_normalize_method == "Interpolate to Fixed Points":
                        fixed_points = st.slider("Set normalization points", min_value=10, max_value=500, value=100, step=10)
                    
                    # Whether to fix zero values
                    fix_zeros_dist = st.checkbox("Fix zero values in energy data", value=True, 
                                            help="Some Q&As take less time than the energy measurement update cycle, resulting in zero energy data. Check this option to fix these data points using nearby non-zero values",
                                            key="fix_zeros_dist")
                    
                    # Prepare single energy data for each task
                    energy_distribution_data = pd.DataFrame()
                    
                    # Determine target points
                    if energy_normalize_method == "Interpolate to Maximum Points":
                        target_points = max([len(task.data) for task in selected_tasks])
                    elif energy_normalize_method == "Interpolate to Fixed Points":
                        target_points = fixed_points
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Get single energy data and fix zero values
                        single_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_dist:
                            single_energy = fix_zero_values(single_energy)
                        
                        if energy_normalize_method == "Keep Original Points":
                            # Reset index to Q&A number
                            single_energy = single_energy.reset_index(drop=True)
                            # Add to DataFrame
                            energy_distribution_data[task_name] = single_energy
                        else:
                            # Interpolate single energy data
                            interpolated_energy = interpolate_data(single_energy, target_points)
                            # Add to DataFrame with unified index
                            if energy_distribution_data.empty:
                                energy_distribution_data = pd.DataFrame(index=range(target_points))
                            energy_distribution_data[task_name] = interpolated_energy
                    
                    # Use line chart to show distribution trends
                    st.line_chart(energy_distribution_data)
                    
                    # Create distribution summary data
                    distribution_summary = pd.DataFrame({
                        'Task': [],
                        'Minimum': [],
                        '25th Percentile': [],
                        'Median': [],
                        '75th Percentile': [],
                        'Maximum': [],
                        'Mean': [],
                        'Standard Deviation': []
                    })
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        energy_stats = task.data['total_incremental_energy'].describe()
                        
                        new_row = pd.DataFrame({
                            'Task': [task_name],
                            'Minimum': [energy_stats['min']],
                            '25th Percentile': [energy_stats['25%']],
                            'Median': [energy_stats['50%']],
                            '75th Percentile': [energy_stats['75%']],
                            'Maximum': [energy_stats['max']],
                            'Mean': [energy_stats['mean']],
                            'Standard Deviation': [energy_stats['std']]
                        })
                        
                        distribution_summary = pd.concat([distribution_summary, new_row])
                    
                    # Display distribution statistics summary
                    st.markdown("##### Energy Distribution Statistics Summary")
                    st.dataframe(distribution_summary)
                    
                    with st.expander("View Chart Explanation"):
                        if energy_normalize_method == "Keep Original Points":
                            st.markdown("""
                            **Single Q&A Energy Distribution Comparison Explanation:**
                            - X-axis represents Q&A number
                            - Y-axis represents single Q&A energy, in Wh
                            - Each line represents a selected task
                            - Note: Tasks have different number of rows, consider this when making direct comparisons
                            - The statistics summary table provides key statistical indicators of energy distribution for each task
                            """)
                        else:
                            st.markdown("""
                            **Single Q&A Energy Distribution Comparison Explanation:**
                            - X-axis represents normalized Q&A number
                            - Y-axis represents single Q&A energy, in Wh
                            - Each line represents a selected task
                            - Through interpolation processing, all tasks have the same number of points, facilitating direct comparison
                            - The statistics summary table provides key statistical indicators of energy distribution for each task (based on original data)
                            """)
                        
                with trend_tabs[2]:
                    st.markdown("#### Real-time Power Change Comparison")
                    
                    # Power change normalization settings
                    power_normalize_method = st.radio(
                        "Power comparison normalization method",
                        ["Percentage Progress", "Interpolate to Same Points"],
                        horizontal=True
                    )
                    
                    if power_normalize_method == "Interpolate to Same Points":
                        power_points = st.slider("Power comparison normalization points", min_value=10, max_value=500, value=100, step=10)
                    
                    # Whether to fix zero values
                    fix_zeros_power = st.checkbox("Fix zero values in energy data", value=True, 
                                                help="Some Q&As take less time than the energy measurement update cycle, resulting in zero energy data. Check this option to fix these data points using nearby non-zero values",
                                                key="fix_zeros_power")
                    
                    # Calculate and draw real-time power changes
                    power_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Calculate time interval (seconds)
                        task.data['start_time'] = pd.to_datetime(task.data['start_time'])
                        task.data['end_time'] = pd.to_datetime(task.data['end_time'])
                        task.data['duration'] = (task.data['end_time'] - task.data['start_time']).dt.total_seconds()
                        
                        # Get energy data and fix zero values
                        total_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_power:
                            total_energy = fix_zero_values(total_energy)
                        
                        # Calculate real-time power (W = J/s, energy unit is Wh, need to convert to W)
                        # Power = Energy(Wh) * 3600 / Duration(s)
                        power_series = total_energy * 3600 / task.data['duration']
                        
                        # Handle zero values or inf values (may occur when duration is close to 0)
                        power_series = power_series.replace([np.inf, -np.inf], np.nan).fillna(power_series.mean())
                        
                        if power_normalize_method == "Percentage Progress":
                            # Create percentage progress index
                            progress_pct = np.linspace(0, 100, len(power_series))
                            # Add to DataFrame
                            task_df = pd.DataFrame({task_name: power_series.values}, index=progress_pct)
                            power_trend_data = pd.concat([power_trend_data, task_df], axis=1)
                        else:
                            # Interpolate power data
                            interpolated_power = interpolate_data(power_series, power_points)
                            # Add to DataFrame with unified index
                            if power_trend_data.empty:
                                power_trend_data = pd.DataFrame(index=range(power_points))
                            power_trend_data[task_name] = interpolated_power
                    
                    # Draw real-time power comparison chart
                    st.line_chart(power_trend_data)
                    
                    with st.expander("View Chart Explanation"):
                        if power_normalize_method == "Percentage Progress":
                            st.markdown("""
                            **Real-time Power Change Comparison Explanation:**
                            - X-axis represents task progress percentage, from 0% to 100%
                            - Y-axis represents real-time power, in W (Watts)
                            - Each line represents a selected task
                            - Peaks indicate highest energy intensity at that moment
                            """)
                        else:
                            st.markdown("""
                            **Real-time Power Change Comparison Explanation:**
                            - X-axis represents standardized data point number
                            - Y-axis represents real-time power, in W (Watts)
                            - Each line represents a selected task
                            - Through interpolation processing, all tasks have the same number of points, facilitating direct comparison
                            - Peaks indicate highest energy intensity at that moment
                            """)

elif st.session_state.language == "Français":
    # Configuration de la page
    st.set_page_config(
        page_title="Comparaison des Résultats",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Comparaison des Résultats des Tâches")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    # Fonction auxiliaire: Traitement d'interpolation des données
    def interpolate_data(data_series, target_length):
        """
        Interpoler une série de données pour atteindre une longueur cible
        """
        # Indices de données originales
        orig_indices = np.arange(len(data_series))
        # Indices cibles
        target_indices = np.linspace(0, len(data_series) - 1, target_length)
        # Créer une fonction d'interpolation
        if len(data_series) > 1:
            f = interpolate.interp1d(orig_indices, data_series, kind='linear')
            # Exécuter l'interpolation
            interpolated_data = f(target_indices)
            return interpolated_data
        else:
            # Si un seul point de données, impossible d'interpoler, donc copier la valeur
            return np.full(target_length, data_series.iloc[0])

    # Fonction pour corriger les valeurs nulles
    def fix_zero_values(data_series):
        """
        Corriger les valeurs nulles dans une série de données en utilisant la moyenne des points non nuls voisins
        
        Paramètres:
            data_series (pd.Series): Série de données à traiter
        
        Retourne:
            pd.Series: Série de données traitée
        """
        # Créer une copie des données
        fixed_data = data_series.copy()
        zero_indices = np.where(fixed_data == 0)[0]
        
        if len(zero_indices) == 0:
            return fixed_data  # Pas de valeurs nulles
        
        # Si toutes les valeurs sont nulles, retourner une petite valeur
        if len(zero_indices) == len(fixed_data):
            return pd.Series([1e-6] * len(fixed_data))
        
        for idx in zero_indices:
            # Rechercher en arrière la valeur non nulle la plus proche
            prev_non_zero = None
            for i in range(idx-1, -1, -1):
                if fixed_data.iloc[i] != 0:
                    prev_non_zero = fixed_data.iloc[i]
                    break
            
            # Rechercher en avant la valeur non nulle la plus proche
            next_non_zero = None
            for i in range(idx+1, len(fixed_data)):
                if fixed_data.iloc[i] != 0:
                    next_non_zero = fixed_data.iloc[i]
                    break
            
            # Estimer la valeur nulle actuelle en utilisant les valeurs non nulles voisines
            if prev_non_zero is not None and next_non_zero is not None:
                fixed_data.iloc[idx] = (prev_non_zero + next_non_zero) / 2
            elif prev_non_zero is not None:
                fixed_data.iloc[idx] = prev_non_zero
            elif next_non_zero is not None:
                fixed_data.iloc[idx] = next_non_zero
            else:
                # Ne devrait pas s'exécuter ici, car nous avons déjà vérifié si toutes les valeurs sont nulles
                fixed_data.iloc[idx] = 1e-6  # Solution de secours, utiliser une petite valeur non nulle
        
        return fixed_data

    # Vérifier les travaux préliminaires
    if 'workspace' not in st.session_state:
        st.warning("Veuillez d'abord initialiser le répertoire de travail dans la page de gestion CSV.")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("Veuillez d'abord sélectionner au moins deux fichiers CSV à comparer dans la page de gestion CSV.")
        else:
            # Obtenir tous les noms de tâches sélectionnés
            selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
            selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
            
            if len(selected_names) < 2:
                st.warning("Veuillez sélectionner au moins deux tâches à comparer.")
            else:
                # Obtenir les objets de tâche correspondants
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
                
                # S'assurer que toutes les tâches ont été analysées
                for task in selected_tasks:
                    if not hasattr(task, 'statistics') or not task.statistics:
                        task.analyse()
                
                # Créer des données de comparaison
                comparison_data = {}
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    
                    # Collecter des statistiques de base pour la comparaison
                    comparison_data[task_name] = {
                        'Nombre total de Q&R': task.statistics['问答总数'],
                        'Durée totale (sec)': task.statistics['总持续时间(秒)'],
                        'Taux de précision': task.statistics['正确率'],
                        'Taux d\'efficacité': task.statistics['有效率'],
                        'Temps moyen par Q&R (sec)': task.statistics['平均每次问答时间(秒)'],
                        'Consommation CPU totale (Wh)': task.statistics['CPU总能耗(Wh)'],
                        'Consommation GPU totale (Wh)': task.statistics['GPU总能耗(Wh)'],
                        'Consommation totale (Wh)': task.statistics['总能耗(Wh)'],
                        'Consommation CPU moyenne par Q&R (Wh)': task.statistics['CPU平均每次问答能耗(Wh)'],
                        'Consommation GPU moyenne par Q&R (Wh)': task.statistics['GPU平均每次问答能耗(Wh)'],
                        'Consommation totale moyenne par Q&R (Wh)': task.statistics['平均每次问答总能耗(Wh)'],
                        'Puissance CPU moyenne (W)': task.statistics['CPU平均功率(W)'],
                        'Puissance GPU moyenne (W)': task.statistics['GPU平均功率(W)'],
                        'Puissance totale moyenne (W)': task.statistics['总平均功率(W)'],
                    }

                # Convertir en DataFrame pour faciliter le traçage
                comparison_df = pd.DataFrame(comparison_data).T
                
                # Fournir différentes dimensions de comparaison au choix
                st.markdown("### Choisir la dimension de comparaison")
                comparison_tabs = st.tabs(["Indicateurs de base", "Comparaison de consommation", "Comparaison de puissance", "Comparaison combinée"])
                
                with comparison_tabs[0]:
                    st.markdown("#### Comparaison des indicateurs de base")
                    basic_metrics = ['Nombre total de Q&R', 'Durée totale (sec)', 'Taux de précision', 'Taux d\'efficacité', 'Temps moyen par Q&R (sec)']
                    selected_basic_metrics = st.multiselect(
                        "Sélectionner les indicateurs de base à comparer", 
                        basic_metrics,
                        default=['Nombre total de Q&R', 'Taux de précision']
                    )
                    
                    if selected_basic_metrics:
                        st.bar_chart(comparison_df[selected_basic_metrics])
                
                with comparison_tabs[1]:
                    st.markdown("#### Comparaison de consommation d'énergie")
                    energy_metrics = ['Consommation CPU totale (Wh)', 'Consommation GPU totale (Wh)', 'Consommation totale (Wh)', 
                                'Consommation CPU moyenne par Q&R (Wh)', 'Consommation GPU moyenne par Q&R (Wh)', 'Consommation totale moyenne par Q&R (Wh)']
                    selected_energy_metrics = st.multiselect(
                        "Sélectionner les indicateurs de consommation à comparer", 
                        energy_metrics,
                        default=['Consommation totale (Wh)', 'Consommation CPU totale (Wh)', 'Consommation GPU totale (Wh)']
                    )
                    
                    if selected_energy_metrics:
                        # Tracer le graphique de comparaison de consommation
                        st.bar_chart(comparison_df[selected_energy_metrics])
                        
                        # Fournir une vue tableau de données
                        with st.expander("Voir les données détaillées"):
                            st.dataframe(comparison_df[selected_energy_metrics])
                
                with comparison_tabs[2]:
                    st.markdown("#### Comparaison de puissance")
                    power_metrics = ['Puissance CPU moyenne (W)', 'Puissance GPU moyenne (W)', 'Puissance totale moyenne (W)']
                    selected_power_metrics = st.multiselect(
                        "Sélectionner les indicateurs de puissance à comparer", 
                        power_metrics,
                        default=power_metrics
                    )
                    
                    if selected_power_metrics:
                        # Tracer le graphique de comparaison de puissance
                        st.bar_chart(comparison_df[selected_power_metrics])
                        
                        # Fournir une vue tableau de données
                        with st.expander("Voir les données détaillées"):
                            st.dataframe(comparison_df[selected_power_metrics])
                
                with comparison_tabs[3]:
                    st.markdown("#### Comparaison combinée personnalisée")
                    all_metrics = basic_metrics + energy_metrics + power_metrics
                    custom_metrics = st.multiselect(
                        "Sélectionner les indicateurs à comparer", 
                        all_metrics,
                        default=['Consommation totale (Wh)', 'Puissance totale moyenne (W)', 'Taux de précision']
                    )
                    
                    chart_type = st.radio("Choisir le type de graphique", ["Diagramme à barres", "Graphique linéaire"], horizontal=True)
                    
                    if custom_metrics:
                        if chart_type == "Diagramme à barres":
                            st.bar_chart(comparison_df[custom_metrics])
                        else:
                            st.line_chart(comparison_df[custom_metrics])
                        
                        # Fournir une vue tableau de données
                        with st.expander("Voir les données détaillées"):
                            st.dataframe(comparison_df[custom_metrics])
                
                # Comparaison avancée: superposition de séries chronologiques
                st.markdown("### Comparaison des tendances de consommation")
                trend_tabs = st.tabs(["Tendance de consommation cumulée", "Distribution de consommation par Q&R", "Variation de puissance en temps réel"])
                
                with trend_tabs[0]:
                    st.markdown("#### Comparaison des tendances de consommation cumulée")
                    
                    # Définir un nombre standardisé de points pour toutes les tâches (100 points suffisent pour montrer la tendance)
                    standard_points = 100
                    normalize_method = st.radio(
                        "Méthode de normalisation",
                        ["Pourcentage de progression", "Interpolation à nombre égal de points"],
                        horizontal=True,
                        help="Pourcentage de progression: aligner selon le pourcentage de progression de la tâche; Interpolation à nombre égal de points: rééchantillonner toutes les tâches au même nombre de points"
                    )
                    
                    # Réparer ou non les valeurs nulles
                    fix_zeros = st.checkbox("Corriger les valeurs nulles dans les données de consommation", value=True, 
                                            help="Certaines Q&R prennent moins de temps que le cycle de mise à jour de la mesure d'énergie, ce qui entraîne des données d'énergie nulles. Cochez cette option pour corriger ces points de données à l'aide de valeurs non nulles voisines")
                    
                    # Créer un DataFrame pour stocker la consommation cumulée de toutes les tâches
                    energy_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Obtenir les données de consommation et corriger les valeurs nulles
                        total_energy = task.data['total_incremental_energy']
                        cpu_energy = task.data['cpu_incremental_energy']
                        gpu_energy = task.data['gpu_incremental_energy']
                        
                        if fix_zeros:
                            total_energy = fix_zero_values(total_energy)
                            cpu_energy = fix_zero_values(cpu_energy)
                            gpu_energy = fix_zero_values(gpu_energy)
                        
                        # Calculer la consommation cumulée
                        total_cumsum = total_energy.cumsum()
                        
                        if normalize_method == "Pourcentage de progression":
                            # Créer un index de pourcentage de progression
                            progress_pct = np.linspace(0, 100, len(total_cumsum))
                            # Ajouter au DataFrame
                            task_df = pd.DataFrame({task_name: total_cumsum.values}, index=progress_pct)
                            energy_trend_data = pd.concat([energy_trend_data, task_df], axis=1)
                        else:
                            # Interpoler les données de consommation cumulée pour que toutes les tâches aient le même nombre de points
                            interpolated_cumsum = interpolate_data(total_cumsum, standard_points)
                            # Ajouter au DataFrame avec un index unifié
                            if energy_trend_data.empty:
                                energy_trend_data = pd.DataFrame(index=range(standard_points))
                            energy_trend_data[task_name] = interpolated_cumsum
                    
                    # Tracer le graphique de comparaison de consommation cumulée
                    st.line_chart(energy_trend_data)
                    
                    with st.expander("Voir l'explication du graphique"):
                        if normalize_method == "Pourcentage de progression":
                            st.markdown("""
                            **Explication de la comparaison des tendances de consommation cumulée:**
                            - L'axe X représente le pourcentage de progression de la tâche, de 0% à 100%
                            - L'axe Y représente la consommation cumulée, en Wh
                            - Chaque ligne représente une tâche sélectionnée
                            - Les parties avec une pente plus raide indiquent une croissance plus rapide de la consommation d'énergie à ce stade
                            """)
                        else:
                            st.markdown("""
                            **Explication de la comparaison des tendances de consommation cumulée:**
                            - L'axe X représente le numéro de point de données standardisé (ajusté par interpolation pour que les tâches de différentes longueurs aient le même nombre de points)
                            - L'axe Y représente la consommation cumulée, en Wh
                            - Chaque ligne représente une tâche sélectionnée
                            - Les parties avec une pente plus raide indiquent une croissance plus rapide de la consommation d'énergie à ce stade
                            - Grâce au traitement d'interpolation, on peut comparer directement les tendances des tâches de différentes longueurs
                            """)
                
                with trend_tabs[1]:
                    st.markdown("#### Comparaison de la distribution de consommation par Q&R")
                    
                    # Paramètres de normalisation de la distribution de consommation par Q&R
                    st.write("##### Paramètres de normalisation des données")
                    energy_normalize_method = st.radio(
                        "Choisir la méthode de normalisation",
                        ["Conserver les points d'origine", "Interpoler au nombre maximal de points", "Interpoler à un nombre fixe de points"],
                        horizontal=True
                    )
                    
                    if energy_normalize_method == "Interpoler à un nombre fixe de points":
                        fixed_points = st.slider("Définir le nombre de points de normalisation", min_value=10, max_value=500, value=100, step=10)
                    
                    # Réparer ou non les valeurs nulles
                    fix_zeros_dist = st.checkbox("Corriger les valeurs nulles dans les données de consommation", value=True, 
                                            help="Certaines Q&R prennent moins de temps que le cycle de mise à jour de la mesure d'énergie, ce qui entraîne des données d'énergie nulles. Cochez cette option pour corriger ces points de données à l'aide de valeurs non nulles voisines",
                                            key="fix_zeros_dist")
                    
                    # Préparer les données de consommation par Q&R pour chaque tâche
                    energy_distribution_data = pd.DataFrame()
                    
                    # Déterminer le nombre de points cible
                    if energy_normalize_method == "Interpoler au nombre maximal de points":
                        target_points = max([len(task.data) for task in selected_tasks])
                    elif energy_normalize_method == "Interpoler à un nombre fixe de points":
                        target_points = fixed_points
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Obtenir les données de consommation par Q&R et corriger les valeurs nulles
                        single_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_dist:
                            single_energy = fix_zero_values(single_energy)
                        
                        if energy_normalize_method == "Conserver les points d'origine":
                            # Réinitialiser l'index au numéro de Q&R
                            single_energy = single_energy.reset_index(drop=True)
                            # Ajouter au DataFrame
                            energy_distribution_data[task_name] = single_energy
                        else:
                            # Interpoler les données de consommation par Q&R
                            interpolated_energy = interpolate_data(single_energy, target_points)
                            # Ajouter au DataFrame avec un index unifié
                            if energy_distribution_data.empty:
                                energy_distribution_data = pd.DataFrame(index=range(target_points))
                            energy_distribution_data[task_name] = interpolated_energy
                    
                    # Utiliser un graphique linéaire pour montrer les tendances de distribution
                    st.line_chart(energy_distribution_data)
                    
                    # Créer des données résumant la distribution
                    distribution_summary = pd.DataFrame({
                        'Tâche': [],
                        'Minimum': [],
                        '25e centile': [],
                        'Médiane': [],
                        '75e centile': [],
                        'Maximum': [],
                        'Moyenne': [],
                        'Écart-type': []
                    })
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        energy_stats = task.data['total_incremental_energy'].describe()
                        
                        new_row = pd.DataFrame({
                            'Tâche': [task_name],
                            'Minimum': [energy_stats['min']],
                            '25e centile': [energy_stats['25%']],
                            'Médiane': [energy_stats['50%']],
                            '75e centile': [energy_stats['75%']],
                            'Maximum': [energy_stats['max']],
                            'Moyenne': [energy_stats['mean']],
                            'Écart-type': [energy_stats['std']]
                        })
                        
                        distribution_summary = pd.concat([distribution_summary, new_row])
                    
                    # Afficher le résumé statistique de la distribution
                    st.markdown("##### Résumé statistique de la distribution de consommation")
                    st.dataframe(distribution_summary)
                    
                    with st.expander("Voir l'explication du graphique"):
                        if energy_normalize_method == "Conserver les points d'origine":
                            st.markdown("""
                            **Explication de la comparaison de la distribution de consommation par Q&R:**
                            - L'axe X représente le numéro de Q&R
                            - L'axe Y représente la consommation par Q&R, en Wh
                            - Chaque ligne représente une tâche sélectionnée
                            - Remarque: Les tâches ont un nombre de lignes différent, il faut en tenir compte lors de la comparaison directe
                            - Le tableau de résumé statistique fournit des indicateurs statistiques clés de la distribution de consommation pour chaque tâche
                            """)
                        else:
                            st.markdown("""
                            **Explication de la comparaison de la distribution de consommation par Q&R:**
                            - L'axe X représente le numéro de Q&R normalisé
                            - L'axe Y représente la consommation par Q&R, en Wh
                            - Chaque ligne représente une tâche sélectionnée
                            - Grâce au traitement d'interpolation, toutes les tâches ont le même nombre de points, facilitant la comparaison directe
                            - Le tableau de résumé statistique fournit des indicateurs statistiques clés de la distribution de consommation pour chaque tâche (basé sur les données d'origine)
                            """)
                        
                with trend_tabs[2]:
                    st.markdown("#### Comparaison des variations de puissance en temps réel")
                    
                    # Paramètres de normalisation des variations de puissance
                    power_normalize_method = st.radio(
                        "Méthode de normalisation pour la comparaison de puissance",
                        ["Pourcentage de progression", "Interpolation à nombre égal de points"],
                        horizontal=True
                    )
                    
                    if power_normalize_method == "Interpolation à nombre égal de points":
                        power_points = st.slider("Points de normalisation pour la comparaison de puissance", min_value=10, max_value=500, value=100, step=10)
                    
                    # Réparer ou non les valeurs nulles
                    fix_zeros_power = st.checkbox("Corriger les valeurs nulles dans les données de consommation", value=True, 
                                                help="Certaines Q&R prennent moins de temps que le cycle de mise à jour de la mesure d'énergie, ce qui entraîne des données d'énergie nulles. Cochez cette option pour corriger ces points de données à l'aide de valeurs non nulles voisines",
                                                key="fix_zeros_power")
                    
                    # Calculer et tracer les variations de puissance en temps réel
                    power_trend_data = pd.DataFrame()
                    
                    for task in selected_tasks:
                        task_name = task.basic_info['name']
                        # Calculer l'intervalle de temps (secondes)
                        task.data['start_time'] = pd.to_datetime(task.data['start_time'])
                        task.data['end_time'] = pd.to_datetime(task.data['end_time'])
                        task.data['duration'] = (task.data['end_time'] - task.data['start_time']).dt.total_seconds()
                        
                        # Obtenir les données de consommation et corriger les valeurs nulles
                        total_energy = task.data['total_incremental_energy']
                        
                        if fix_zeros_power:
                            total_energy = fix_zero_values(total_energy)
                        
                        # Calculer la puissance en temps réel (W = J/s, unité d'énergie est Wh, nécessite conversion en W)
                        # Puissance = Énergie(Wh) * 3600 / Durée(s)
                        power_series = total_energy * 3600 / task.data['duration']
                        
                        # Traiter les valeurs nulles ou inf (peut se produire lorsque la durée est proche de 0)
                        power_series = power_series.replace([np.inf, -np.inf], np.nan).fillna(power_series.mean())
                        
                        if power_normalize_method == "Pourcentage de progression":
                            # Créer un index de pourcentage de progression
                            progress_pct = np.linspace(0, 100, len(power_series))
                            # Ajouter au DataFrame
                            task_df = pd.DataFrame({task_name: power_series.values}, index=progress_pct)
                            power_trend_data = pd.concat([power_trend_data, task_df], axis=1)
                        else:
                            # Interpoler les données de puissance
                            interpolated_power = interpolate_data(power_series, power_points)
                            # Ajouter au DataFrame avec un index unifié
                            if power_trend_data.empty:
                                power_trend_data = pd.DataFrame(index=range(power_points))
                            power_trend_data[task_name] = interpolated_power
                    
                    # Tracer le graphique de comparaison de puissance en temps réel
                    st.line_chart(power_trend_data)
                    
                    with st.expander("Voir l'explication du graphique"):
                        if power_normalize_method == "Pourcentage de progression":
                            st.markdown("""
                            **Explication de la comparaison des variations de puissance en temps réel:**
                            - L'axe X représente le pourcentage de progression de la tâche, de 0% à 100%
                            - L'axe Y représente la puissance en temps réel, en W (Watts)
                            - Chaque ligne représente une tâche sélectionnée
                            - Les pics indiquent l'intensité énergétique la plus élevée à ce moment
                            """)
                        else:
                            st.markdown("""
                            **Explication de la comparaison des variations de puissance en temps réel:**
                            - L'axe X représente le numéro de point de données standardisé
                            - L'axe Y représente la puissance en temps réel, en W (Watts)
                            - Chaque ligne représente une tâche sélectionnée
                            - Grâce au traitement d'interpolation, toutes les tâches ont le même nombre de points, facilitant la comparaison directe
                            - Les pics indiquent l'intensité énergétique la plus élevée à ce moment
                            """)

# Reset activated page
st.session_state.current_page_index = 4
