import streamlit as st
from pathlib import Path
from energy_tracker_core.Visulization.workspace_task import WorkSpace
from energy_tracker_core.GlobalConfig import DATA_DIR
import time
import pandas as pd

st.session_state.language = st.session_state.get("language", "中文")
if st.session_state.language == "中文":
    # 页面配置
    st.set_page_config(
        page_title="CSV 文件管理",
        page_icon="📂",
        layout="wide"
    )

    st.title("📂 CSV 文件管理")
    st.markdown("### 工作目录")

    # 输入并确认 workspace 目录
    col1, col2, col3 = st.columns([8, 1, 1], vertical_alignment="bottom")
    with col1:
        dir_input = st.text_input(
            "请输入包含 CSV 文件的工作目录绝对路径, 默认路径为项目data目录", value=st.session_state.get("workspace_dirpath", DATA_DIR.as_posix()),
            help="日志文件默认放在项目根目录的log文件夹下",
            label_visibility='visible'
        )
    with col2:
        confirm_click = st.button("确认", help='确认新路径',key="confirm_dir",use_container_width=True)

    with col3:
        update_click = st.button("更新", help='重新扫描当前路径',key="rescan_dir",use_container_width=True)

    if confirm_click:
        try:
            ws = WorkSpace(dir_input)
            ws.scan()
            st.session_state.workspace = ws
            st.success("Workspace 初始化成功，已扫描目录中的 CSV 文件。")
        except Exception as e:
            st.error(f"初始化失败：{e}")
    if update_click:
        if "workspace" in st.session_state:
            ws = st.session_state.workspace
            try:
                ws.scan()
                st.success("Workspace 更新成功，已重新扫描目录中的 CSV 文件。")
            except Exception as e:
                st.error(f"更新失败：{e}")
        else:
            st.warning("请先初始化 Workspace。")
        
    # 如果已初始化 workspace，则展示文件列表和基本信息
    if "workspace" in st.session_state:
        if st.session_state.current_page_index != 2:
            st.session_state.current_page_index = 2
            st.session_state.workspace.task_showframe = st.session_state.edited_task_showframe.copy()
            st.rerun()
        with st.form(key="file_selection_form"):
            st.session_state.edited_task_showframe = st.data_editor(st.session_state.workspace.task_showframe)
            is_submitted = st.form_submit_button(label="提交",use_container_width=True)
        if is_submitted:
            st.success("已提交选择")
    
elif st.session_state.language == "English":
    # 页面配置
    st.set_page_config(
        page_title="CSV File Management",
        page_icon="📂",
        layout="wide"
    )


    st.title("📂 CSV File Management")
    st.markdown("### Working Directory")


    # 输入并确认 workspace 目录
    col1, col2, col3 = st.columns([8, 1, 1], vertical_alignment="bottom")
    with col1:
        dir_input = st.text_input(
            "Enter the absolute path of the working directory containing CSV files, default path is the project data directory", 
            value=st.session_state.get("workspace_dirpath", DATA_DIR.as_posix()),
            help="Log files are stored in the log folder under the project root directory by default",
            label_visibility='visible'
        )
    with col2:
        confirm_click = st.button("Confirm", help='Confirm new path', key="confirm_dir", use_container_width=True)

    with col3:
        update_click = st.button("Update", help='Rescan current path', key="rescan_dir", use_container_width=True)

    if confirm_click:
        try:
            ws = WorkSpace(dir_input)
            ws.scan()
            st.session_state.workspace = ws
            st.success("Workspace initialized successfully, CSV files in the directory have been scanned.")
        except Exception as e:
            st.error(f"Initialization failed: {e}")
    if update_click:
        if "workspace" in st.session_state:
            ws = st.session_state.workspace
            try:
                ws.scan()
                st.success("Workspace updated successfully, CSV files in the directory have been rescanned.")
            except Exception as e:
                st.error(f"Update failed: {e}")
        else:
            st.warning("Please initialize the Workspace first.")
        
    # 如果已初始化 workspace，则展示文件列表和基本信息
    if "workspace" in st.session_state:
        if st.session_state.current_page_index != 2:
            st.session_state.current_page_index = 2
            st.session_state.workspace.task_showframe = st.session_state.edited_task_showframe.copy()
            st.rerun()
        with st.form(key="file_selection_form"):
            st.session_state.edited_task_showframe = st.data_editor(st.session_state.workspace.task_showframe)
            is_submitted = st.form_submit_button(label="Submit", use_container_width=True)
        if is_submitted:
            st.success("Selection submitted")

elif st.session_state.language == "Français":
    # 页面配置
    st.set_page_config(
        page_title="Gestion des Fichiers CSV",
        page_icon="📂",
        layout="wide"
    )


    st.title("📂 Gestion des Fichiers CSV")
    st.markdown("### Répertoire de Travail")


    # 输入并确认 workspace 目录
    col1, col2, col3 = st.columns([6, 1, 1], vertical_alignment="bottom")
    with col1:
        dir_input = st.text_input(
            "Entrez le chemin absolu du répertoire de travail contenant les fichiers CSV, le chemin par défaut est le répertoire de données du projet", 
            value=st.session_state.get("workspace_dirpath", DATA_DIR.as_posix()),
            help="Les fichiers journaux sont stockés dans le dossier log sous le répertoire racine du projet par défaut",
            label_visibility='visible'
        )
    with col2:
        confirm_click = st.button("Confirmer", help='Confirmer le nouveau chemin', key="confirm_dir", use_container_width=True)

    with col3:
        update_click = st.button("Actualiser", help='Rescanner le chemin actuel', key="rescan_dir", use_container_width=True)

    if confirm_click:
        try:
            ws = WorkSpace(dir_input)
            ws.scan()
            st.session_state.workspace = ws
            st.success("Espace de travail initialisé avec succès, les fichiers CSV du répertoire ont été scannés.")
        except Exception as e:
            st.error(f"Échec de l'initialisation: {e}")
    if update_click:
        if "workspace" in st.session_state:
            ws = st.session_state.workspace
            try:
                ws.scan()
                st.success("Espace de travail mis à jour avec succès, les fichiers CSV du répertoire ont été rescannés.")
            except Exception as e:
                st.error(f"Échec de la mise à jour: {e}")
        else:
            st.warning("Veuillez d'abord initialiser l'espace de travail.")
        
    # 如果已初始化 workspace，则展示文件列表和基本信息
    if "workspace" in st.session_state:
        if st.session_state.current_page_index != 2:
            st.session_state.current_page_index = 2
            st.session_state.workspace.task_showframe = st.session_state.edited_task_showframe.copy()
            st.rerun()
        with st.form(key="file_selection_form"):
            st.session_state.edited_task_showframe = st.data_editor(st.session_state.workspace.task_showframe)
            is_submitted = st.form_submit_button(label="Soumettre", use_container_width=True)
        if is_submitted:
            st.success("Sélection soumise")
            
# 重置激活页
st.session_state.current_page_index = 2