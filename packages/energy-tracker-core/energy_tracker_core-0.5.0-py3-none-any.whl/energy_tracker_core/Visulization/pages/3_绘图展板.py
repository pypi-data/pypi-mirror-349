import streamlit as st
from energy_tracker_core.Visulization.workspace_task import WorkSpace, Task
import pandas as pd
import numpy as np

st.session_state.language = st.session_state.get("language", "中文")
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


if st.session_state.language == "中文":
    # 页面配置
    st.set_page_config(
        page_title="绘图展板",
        page_icon=":material/palette:",
        layout="wide"
    )

    st.title("🎨 绘图展板")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    def button_callback(task:Task):
        """
        点击按钮后触发回调，设置当前绘图任务
        """

        st.session_state.task_to_plot = task


    # 检查前序工作
    if 'workspace' not in st.session_state:
        st.warning("请先在 CSV 管理页面初始化工作目录。")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("请先在 CSV 管理页面至少选择一个要分析的csv文件。")
        else:
            # 遍历sw.task_showframe，获取所有选中的任务名称
            selected_task_name = st.session_state.edited_task_showframe.query("is_selected == True")["name"]
            
            # 根据选中的任务名称，获取对应的任务对象,并添加到列表中
            selected_tasks = []
            for task_name in selected_task_name:
                selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
                selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
            
            # 构造侧边栏切换
            st.sidebar.title("选择任务视图")
            with st.sidebar:
                current_index = None
                for task in selected_tasks:
                    st.sidebar.button(task.basic_info["name"], 
                                        key=task.basic_info["name"],
                                        on_click=button_callback,
                                        args=(task,))
            
            if "task_to_plot" not in st.session_state:
                st.markdown("### 请在左侧点击要可视化的任务")
            else:
                task:Task
                task = st.session_state.task_to_plot
                task.analyse()
                st.markdown(f"### 任务名称: {task.basic_info['name']}")
                st.markdown(f"#### 任务路径: {task.csv_filepath}")
                # 创建三列布局
                col1, col2, col3 = st.columns(3)
                
                # 第一列显示基本统计信息
                with col1:
                    st.markdown("#### 基本统计")
                    col11, col12 = st.columns(2)
                    with col11:
                        st.metric("问答总数", f"{task.statistics['问答总数']}次")
                        st.metric("正确率", f"{task.statistics['正确率']:.2%}")
                    with col12:
                        st.metric("平均每次问答时间", f"{task.statistics['平均每次问答时间(秒)']:.2f}秒")
                        st.metric("有效率", f"{task.statistics['有效率']:.2%}")
                    st.metric("总持续时间", f"{task.statistics['总持续时间(秒)']:.2f}秒")
                    

                # 第二列显示能耗统计
                with col2:
                    st.markdown("#### 能耗统计 (Wh)")
                    st.metric("总能耗", f"{task.statistics['总能耗(Wh)']:.4f}")
                    st.metric("CPU总能耗", f"{task.statistics['CPU总能耗(Wh)']:.4f}")
                    st.metric("GPU总能耗", f"{task.statistics['GPU总能耗(Wh)']:.4f}")
                    

                # 第三列显示功率统计
                with col3:
                    st.markdown("#### 功率统计 (W)")
                    st.metric("总平均功率", f"{task.statistics['总平均功率(W)']:.4f}")
                    st.metric("CPU平均功率", f"{task.statistics['CPU平均功率(W)']:.4f}")
                    st.metric("GPU平均功率", f"{task.statistics['GPU平均功率(W)']:.4f}")
                    

                # 创建能耗趋势图
                st.markdown("#### 能耗趋势")
                
                # 添加零值修复选项
                fix_zeros = st.checkbox("修复能耗数据中的零值", value=True, 
                                      help="有些问答的时间消耗短于能耗测量的更新周期，导致能耗数据为0。勾选此选项可用临近非零值修复这些数据点",
                                      key="fix_zeros_zh")
                
                # 创建累计能耗趋势线图
                st.markdown("##### 累计能耗趋势")
                
                # 获取能耗数据并修复零值
                total_energy = task.data['total_incremental_energy']
                cpu_energy = task.data['cpu_incremental_energy']
                gpu_energy = task.data['gpu_incremental_energy']
                
                if fix_zeros:
                    total_energy = fix_zero_values(total_energy)
                    cpu_energy = fix_zero_values(cpu_energy)
                    gpu_energy = fix_zero_values(gpu_energy)
                
                trend_chart_data = pd.DataFrame({
                    'CPU累计能耗': cpu_energy.cumsum(),
                    'GPU累计能耗': gpu_energy.cumsum(), 
                    '总累计能耗': total_energy.cumsum()
                })
                st.line_chart(trend_chart_data)

                # 创建每次问答能耗柱状图
                st.markdown("##### 每次问答能耗")
                bar_chart_data = pd.DataFrame({
                    'CPU单次能耗': cpu_energy,
                    'GPU单次能耗': gpu_energy
                })
                st.bar_chart(bar_chart_data)

                # 显示能耗最高的问答记录
                st.markdown("#### 能耗最高的问答记录")
                high_energy_df = pd.DataFrame(task.statistics['能耗最高问答'])
                st.dataframe(high_energy_df[['question', 'total_incremental_energy', 'duration']])

                # 显示能耗最低的问答记录
                st.markdown("#### 能耗最低的问答记录") 
                low_energy_df = pd.DataFrame(task.statistics['能耗最低问答'])
                st.dataframe(low_energy_df[['question', 'total_incremental_energy', 'duration']])

elif st.session_state.language == "English":
    # 页面配置
    st.set_page_config(
        page_title="Visualization Dashboard",
        page_icon=":material/palette:",
        layout="wide"
    )

    st.title("🎨 Visualization Dashboard")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    def button_callback(task:Task):
        """
        Callback triggered after button click, sets the current plotting task
        """

        st.session_state.task_to_plot = task


    # 检查前序工作
    if 'workspace' not in st.session_state:
        st.warning("Please initialize the working directory in the CSV Management page first.")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("Please select at least one CSV file to analyze in the CSV Management page first.")
        else:
            # 遍历sw.task_showframe，获取所有选中的任务名称
            selected_task_name = st.session_state.edited_task_showframe.query("is_selected == True")["name"]
            
            # 根据选中的任务名称，获取对应的任务对象,并添加到列表中
            selected_tasks = []
            for task_name in selected_task_name:
                selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
                selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
            
            # 构造侧边栏切换
            st.sidebar.title("Select Task View")
            with st.sidebar:
                current_index = None
                for task in selected_tasks:
                    st.sidebar.button(task.basic_info["name"], 
                                        key=task.basic_info["name"],
                                        on_click=button_callback,
                                        args=(task,))
            
            if "task_to_plot" not in st.session_state:
                st.markdown("### Please click on a task to visualize in the sidebar")
            else:
                task:Task
                task = st.session_state.task_to_plot
                task.analyse()
                st.markdown(f"### Task Name: {task.basic_info['name']}")
                st.markdown(f"#### Task Path: {task.csv_filepath}")
                # 创建三列布局
                col1, col2, col3 = st.columns(3)
                
                # 第一列显示基本统计信息
                with col1:
                    st.markdown("#### Basic Statistics")
                    col11, col12 = st.columns(2)
                    with col11:
                        st.metric("Total Q&A", f"{task.statistics['问答总数']} times")
                        st.metric("Accuracy", f"{task.statistics['正确率']:.2%}")
                    with col12:
                        st.metric("Average Time per Q&A", f"{task.statistics['平均每次问答时间(秒)']:.2f} seconds")
                        st.metric("Validity", f"{task.statistics['有效率']:.2%}")
                    st.metric("Total Duration", f"{task.statistics['总持续时间(秒)']:.2f} seconds")
                    

                # 第二列显示能耗统计
                with col2:
                    st.markdown("#### Energy Consumption (Wh)")
                    st.metric("Total Energy", f"{task.statistics['总能耗(Wh)']:.4f}")
                    st.metric("CPU Total Energy", f"{task.statistics['CPU总能耗(Wh)']:.4f}")
                    st.metric("GPU Total Energy", f"{task.statistics['GPU总能耗(Wh)']:.4f}")
                    

                # 第三列显示功率统计
                with col3:
                    st.markdown("#### Power Statistics (W)")
                    st.metric("Total Average Power", f"{task.statistics['总平均功率(W)']:.4f}")
                    st.metric("CPU Average Power", f"{task.statistics['CPU平均功率(W)']:.4f}")
                    st.metric("GPU Average Power", f"{task.statistics['GPU平均功率(W)']:.4f}")
                    

                # 创建能耗趋势图
                st.markdown("#### Energy Consumption Trends")
                
                # 添加零值修复选项
                fix_zeros = st.checkbox("Repair Zero Values in Energy Data", value=True, 
                                      help="Some questions may have a duration shorter than the update cycle of energy measurement, resulting in energy data being 0. Check this option to use nearby non-zero values to repair these data points",
                                      key="fix_zeros_en")
                
                # 创建累计能耗趋势线图
                st.markdown("##### Cumulative Energy Consumption")
                
                # 获取能耗数据并修复零值
                total_energy = task.data['total_incremental_energy']
                cpu_energy = task.data['cpu_incremental_energy']
                gpu_energy = task.data['gpu_incremental_energy']
                
                if fix_zeros:
                    total_energy = fix_zero_values(total_energy)
                    cpu_energy = fix_zero_values(cpu_energy)
                    gpu_energy = fix_zero_values(gpu_energy)
                
                trend_chart_data = pd.DataFrame({
                    'CPU Cumulative Energy': cpu_energy.cumsum(),
                    'GPU Cumulative Energy': gpu_energy.cumsum(), 
                    'Total Cumulative Energy': total_energy.cumsum()
                })
                st.line_chart(trend_chart_data)

                # 创建每次问答能耗柱状图
                st.markdown("##### Energy per Q&A")
                bar_chart_data = pd.DataFrame({
                    'CPU Energy per Time': cpu_energy,
                    'GPU Energy per Time': gpu_energy
                })
                st.bar_chart(bar_chart_data)

                # 显示能耗最高的问答记录
                st.markdown("#### Q&A Records with Highest Energy Consumption")
                high_energy_df = pd.DataFrame(task.statistics['能耗最高问答'])
                st.dataframe(high_energy_df[['question', 'total_incremental_energy', 'duration']])

                # 显示能耗最低的问答记录
                st.markdown("#### Q&A Records with Lowest Energy Consumption") 
                low_energy_df = pd.DataFrame(task.statistics['能耗最低问答'])
                st.dataframe(low_energy_df[['question', 'total_incremental_energy', 'duration']])

elif st.session_state.language == "Français":
    # 页面配置
    st.set_page_config(
        page_title="Tableau de Visualisation",
        page_icon=":material/palette:",
        layout="wide"
    )

    st.title("🎨 Tableau de Visualisation")
    ws: WorkSpace = None
    ws = st.session_state.get("workspace", None)

    def button_callback(task:Task):
        """
        Callback déclenché après un clic sur le bouton, définit la tâche de traçage actuelle
        """

        st.session_state.task_to_plot = task


    # 检查前序工作
    if 'workspace' not in st.session_state:
        st.warning("Veuillez d'abord initialiser le répertoire de travail dans la page de Gestion CSV.")
    else:
        if 'edited_task_showframe' not in st.session_state:
            st.warning("Veuillez d'abord sélectionner au moins un fichier CSV à analyser dans la page de Gestion CSV.")
        else:
            # 遍历sw.task_showframe，获取所有选中的任务名称
            selected_task_name = st.session_state.edited_task_showframe.query("is_selected == True")["name"]
            
            # 根据选中的任务名称，获取对应的任务对象,并添加到列表中
            selected_tasks = []
            for task_name in selected_task_name:
                selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
                selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
                selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
            
            # 构造侧边栏切换
            st.sidebar.title("Sélectionner une Tâche")
            with st.sidebar:
                current_index = None
                for task in selected_tasks:
                    st.sidebar.button(task.basic_info["name"], 
                                        key=task.basic_info["name"],
                                        on_click=button_callback,
                                        args=(task,))
            
            if "task_to_plot" not in st.session_state:
                st.markdown("### Veuillez cliquer sur une tâche à visualiser dans la barre latérale")
            else:
                task:Task
                task = st.session_state.task_to_plot
                task.analyse()
                st.markdown(f"### Nom de la Tâche: {task.basic_info['name']}")
                st.markdown(f"#### Chemin de la Tâche: {task.csv_filepath}")
                # 创建三列布局
                col1, col2, col3 = st.columns(3)
                
                # 第一列显示基本统计信息
                with col1:
                    st.markdown("#### Statistiques de Base")
                    col11, col12 = st.columns(2)
                    with col11:
                        st.metric("Total Q&R", f"{task.statistics['问答总数']} fois")
                        st.metric("Précision", f"{task.statistics['正确率']:.2%}")
                    with col12:
                        st.metric("Temps Moyen par Q&R", f"{task.statistics['平均每次问答时间(秒)']:.2f} secondes")
                        st.metric("Validité", f"{task.statistics['有效率']:.2%}")
                    st.metric("Durée Totale", f"{task.statistics['总持续时间(秒)']:.2f} secondes")
                    

                # 第二列显示能耗统计
                with col2:
                    st.markdown("#### Consommation d'Énergie (Wh)")
                    st.metric("Énergie Totale", f"{task.statistics['总能耗(Wh)']:.4f}")
                    st.metric("Énergie Totale CPU", f"{task.statistics['CPU总能耗(Wh)']:.4f}")
                    st.metric("Énergie Totale GPU", f"{task.statistics['GPU总能耗(Wh)']:.4f}")
                    

                # 第三列显示功率统计
                with col3:
                    st.markdown("#### Statistiques de Puissance (W)")
                    st.metric("Puissance Moyenne Totale", f"{task.statistics['总平均功率(W)']:.4f}")
                    st.metric("Puissance Moyenne CPU", f"{task.statistics['CPU平均功率(W)']:.4f}")
                    st.metric("Puissance Moyenne GPU", f"{task.statistics['GPU平均功率(W)']:.4f}")
                    

                # 创建能耗趋势图
                st.markdown("#### Tendances de Consommation d'Énergie")
                
                # 添加零值修复选项
                fix_zeros = st.checkbox("Réparer les valeurs d'énergie nulles", value=True, 
                                      help="Certaines questions peuvent avoir une durée inférieure à la période de mise à jour de la mesure d'énergie, ce qui peut entraîner des données d'énergie égales à 0. Cochez cette option pour utiliser des valeurs non nulles proches pour réparer ces points de données",
                                      key="fix_zeros_fr")
                
                # 创建累计能耗趋势线图
                st.markdown("##### Consommation d'Énergie Cumulée")
                
                # 获取能耗数据并修复零值
                total_energy = task.data['total_incremental_energy']
                cpu_energy = task.data['cpu_incremental_energy']
                gpu_energy = task.data['gpu_incremental_energy']
                
                if fix_zeros:
                    total_energy = fix_zero_values(total_energy)
                    cpu_energy = fix_zero_values(cpu_energy)
                    gpu_energy = fix_zero_values(gpu_energy)
                
                trend_chart_data = pd.DataFrame({
                    'Énergie Cumulée CPU': cpu_energy.cumsum(),
                    'Énergie Cumulée GPU': gpu_energy.cumsum(), 
                    'Énergie Cumulée Totale': total_energy.cumsum()
                })
                st.line_chart(trend_chart_data)

                # 创建每次问答能耗柱状图
                st.markdown("##### Énergie par Q&R")
                bar_chart_data = pd.DataFrame({
                    'Énergie CPU par Interaction': cpu_energy,
                    'Énergie GPU par Interaction': gpu_energy
                })
                st.bar_chart(bar_chart_data)

                # 显示能耗最高的问答记录
                st.markdown("#### Enregistrements Q&R avec la Plus Haute Consommation d'Énergie")
                high_energy_df = pd.DataFrame(task.statistics['能耗最高问答'])
                st.dataframe(high_energy_df[['question', 'total_incremental_energy', 'duration']])

                # 显示能耗最低的问答记录
                st.markdown("#### Enregistrements Q&R avec la Plus Basse Consommation d'Énergie") 
                low_energy_df = pd.DataFrame(task.statistics['能耗最低问答'])
                st.dataframe(low_energy_df[['question', 'total_incremental_energy', 'duration']])

# 重置激活页
st.session_state.current_page_index = 3