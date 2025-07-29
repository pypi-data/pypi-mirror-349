import streamlit as st


st.session_state.language = st.session_state.get("language_button", "中文")
# 中文界面
if st.session_state.language == "中文":
    st.set_page_config(
        page_title="欢迎/帮助",
        page_icon="🏠",
        layout="centered"
    )
    # 添加语言切换按钮
    with st.sidebar:
        st.write("🌐 Choose Language")
        st.segmented_control(
            label="选择语言 / Language / Langue", 
            options=["中文", "English", "Français"],
            key="language_button",
            help="切换界面语言 / Switch interface language",
        )

    st.title("🎉 欢迎使用CSV Viz! 🏠")
    st.markdown(
        """
        ### 本项目为Energy Tracker的子项目, 用于可视化能耗追踪服务日志
        ### 使用说明
        - 请使用左侧侧边栏切换至对应功能页面。
        - 在各功能页面，根据提示输入或选择参数，页面将自动渲染结果。
        - 目前支持csv日志管理, 单个日志可视化和多日志对比。

        ### 快捷操作
        - Windows: `Ctrl+R` 重载页面
        - macOS: `⌘+R` 重载页面

        ### 联系方式
        有任何问题，请联系：philippe.qu@outlook.com
        """
    )
    st.info("当前为欢迎/帮助页面，可在侧边栏选择其他页面。")

# 英语界面
elif st.session_state.language == "English":
    st.set_page_config(
        page_title="Welcome/Help",
        page_icon="🏠",
        layout="centered"
    )
    # 添加语言切换按钮
    with st.sidebar:
        st.write("🌐 Choose Language")
        st.segmented_control(
            label="选择语言 / Language / Langue", 
            options=["中文", "English", "Français"],
            key="language_button",
            help="切换界面语言 / Switch interface language",
        )

    st.title("🎉 Welcome to CSV Viz! 🏠")
    st.markdown(
        """
        ### This project is a subproject of Energy Tracker, used for visualizing energy consumption tracking service logs
        ### Instructions
        - Please use the sidebar on the left to switch to the corresponding feature page.
        - On each feature page, enter or select parameters according to the prompts, and the page will automatically render the results.
        - Currently supports CSV log management, single log visualization, and multi-log comparison.

        ### Shortcuts
        - Windows: `Ctrl+R` Reload page
        - macOS: `⌘+R` Reload page

        ### Contact
        If you have any questions, please contact: philippe.qu@outlook.com
        """
    )
    st.info("This is the welcome/help page. You can select other pages in the sidebar.")

# 法语界面
elif st.session_state.language == "Français":

    st.set_page_config(
        page_title="Bienvenue/Aide",
        page_icon="🏠",
        layout="centered"
    )
    # 添加语言切换按钮
    with st.sidebar:
        st.write("🌐 Choose Language")
        st.segmented_control(
            label="选择语言 / Language / Langue", 
            options=["中文", "English", "Français"],
            key="language_button",
            help="切换界面语言 / Switch interface language",
        )

    st.title("🎉 Bienvenue sur CSV Viz! 🏠")
    st.markdown(
        """
        ### Ce projet est un sous-projet d'Energy Tracker, utilisé pour visualiser les journaux de service de suivi de la consommation d'énergie
        ### Instructions
        - Veuillez utiliser la barre latérale à gauche pour passer à la page de fonctionnalité correspondante.
        - Sur chaque page de fonctionnalité, saisissez ou sélectionnez les paramètres selon les instructions, et la page affichera automatiquement les résultats.
        - Prend actuellement en charge la gestion des journaux CSV, la visualisation d'un seul journal et la comparaison de plusieurs journaux.

        ### Raccourcis
        - Windows: `Ctrl+R` Recharger la page
        - macOS: `⌘+R` Recharger la page

        ### Contact
        Si vous avez des questions, veuillez contacter: philippe.qu@outlook.com
        """
    )
    st.info("Vous êtes sur la page Bienvenue/Aide. Vous pouvez sélectionner d'autres pages dans la barre latérale.")


st.session_state.current_page_index = 1
