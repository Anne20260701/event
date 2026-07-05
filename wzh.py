
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="脑震荡保险反欺诈筛查系统",
    page_icon="",
    layout="wide"
)

# ========== 侧边栏导航 ==========
st.sidebar.title("神积脑盾")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "导航",
    ["项目概览", "分析流水线演示", "AI-Risk评分卡模拟", "文献支撑"]
)

# ========== 页面1：项目概览 ==========
if page == "项目概览":
    st.title("神积脑盾")
    st.subheader("基于ERP的脑震荡保险反欺诈智能筛查系统")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 核心逻辑：行为-神经不匹配

        **场景一：假装发病**
        主诉严重脑震荡 → ERP正常+主诉严重 → **不匹配** → 欺诈警报

        **场景二：夸大病情**
        主诉极度严重 → ERP轻度异常+主诉极度严重 → **不匹配程度过高** → 人工复核

        **场景三：多次脑震荡风险分层**
        3次以上脑震荡史 → 后续风险为无史者**3倍** → 告知+ERP客观检测
        
        """)

    with col2:
        st.markdown("""
        ### 项目定位

        > "在理赔场景中，ERP提供的客观神经功能指标，与主诉症状进行交叉验证，能够以可接受的成本提高可疑案件的筛出率。"

        **三个场景的商业价值**

        | 场景 | 证据强度 | 商业价值 | 落地难度 |
        |------|---------|---------|----------|
        | 假装发病 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
        | 夸大病情 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
        | 风险分层 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
        
        """)

    st.markdown("---")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("保险欺诈占赔付支出", "3%-5%", "部分险种超10%")
    with col4:
        st.metric("脑震荡未被检测/报告", "50%", "UPMC 2023")
    with col5:
        st.metric("3次以上脑震荡后续风险", "RR=3.0", "Guskiewicz 2003")

# ========== 页面2：分析流水线演示 ==========
elif page == "分析流水线演示":
    st.title("分析流水线演示")
    st.markdown("从原始EEG到ERP提取到风险评分的完整流程")


    # 生成模拟ERP波形
    def generate_erp(amplitude, latency, noise=0.5):
        t = np.linspace(-100, 600, 700)
        # P300波形：使用高斯函数模拟
        p300 = amplitude * np.exp(-((t - latency) ** 2) / (2 * 50 ** 2))
        # 添加N100和P200
        n100 = -amplitude * 0.6 * np.exp(-((t - 100) ** 2) / (2 * 30 ** 2))
        p200 = amplitude * 0.4 * np.exp(-((t - 200) ** 2) / (2 * 40 ** 2))
        noise_signal = np.random.normal(0, noise, len(t))
        return t, p300 + n100 + p200 + noise_signal


    # 三种状态
    st.subheader("三种状态的ERP波形对比")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**健康人**")
        t, erp_healthy = generate_erp(20, 300, 0.3)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, erp_healthy, 'b-', linewidth=2)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=300, color='gray', linestyle='--', linewidth=0.5, label='P300峰值')
        ax.set_xlabel('时间 (ms)')
        ax.set_ylabel('振幅 (μV)')
        ax.set_title('正常P300：振幅~20μV，潜伏期~300ms')
        ax.legend()
        st.pyplot(fig)
        st.caption("P300振幅正常 → 神经功能正常")

    with col2:
        st.markdown("**脑震荡患者**")
        t, erp_concussed = generate_erp(14, 330, 0.5)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, erp_concussed, 'r-', linewidth=2)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=330, color='gray', linestyle='--', linewidth=0.5, label='P300峰值')
        ax.set_xlabel('时间 (ms)')
        ax.set_ylabel('振幅 (μV)')
        ax.set_title('脑震荡：振幅降低~14μV，潜伏期延长~330ms')
        ax.legend()
        st.pyplot(fig)
        st.caption("P300振幅降低+潜伏期延长 → 神经功能异常")

    with col3:
        st.markdown("**装病者（假装）**")
        t, erp_malinger = generate_erp(19, 305, 0.4)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, erp_malinger, 'g-', linewidth=2)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=305, color='gray', linestyle='--', linewidth=0.5, label='P300峰值')
        ax.set_xlabel('时间 (ms)')
        ax.set_ylabel('振幅 (μV)')
        ax.set_title('装病者：P300正常（无法伪造异常）')
        ax.legend()
        st.pyplot(fig)
        st.caption("装病者无法产生真正的TBI患者才有的P300异常模式")

    st.info(
        "💡 **关键洞察**：装病者可以'说'自己头晕、健忘，但无法'制造'出真正的脑损伤患者才有的ERP异常。这就是'行为-神经不匹配'的神经科学基础。")

# ========== 页面3：AI-Risk评分卡模拟 ==========
elif page == "AI-Risk评分卡模拟":
    st.title("AI-Risk评分卡模拟")
    st.markdown("调整主诉严重程度，观察AI-Fraud Score的变化")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("输入参数")

        # 主诉严重程度
        complaint_severity = st.slider(
            "主诉严重程度（0-100）",
            min_value=0, max_value=100, value=80,
            help="0=无症状，100=极度严重（剧烈头痛、严重失忆等）"
        )

        # 模拟ERP检测结果
        st.markdown("**ERP检测结果**")

        # 根据主诉程度模拟ERP结果（但加入随机因素，模拟真实场景）
        np.random.seed(42)

        # P300振幅：正常情况下20μV，脑震荡降低
        base_amplitude = 20 - (complaint_severity / 100) * 8 + np.random.normal(0, 1.5)
        p300_amplitude = max(8, min(22, base_amplitude))

        # P300潜伏期：正常情况下300ms，脑震荡延长
        base_latency = 300 + (complaint_severity / 100) * 40 + np.random.normal(0, 8)
        p300_latency = max(280, min(360, base_latency))

        # Alpha不对称性：正常0.05，异常升高
        alpha_asymmetry = 0.05 + (complaint_severity / 100) * 0.15 + np.random.normal(0, 0.02)
        alpha_asymmetry = max(0.01, min(0.25, alpha_asymmetry))

        st.metric("P300振幅", f"{p300_amplitude:.1f} μV",
                  delta=f"{p300_amplitude - 20:.1f}" if p300_amplitude < 20 else None,
                  delta_color="inverse")
        st.metric("P300潜伏期", f"{p300_latency:.0f} ms",
                  delta=f"+{p300_latency - 300:.0f}" if p300_latency > 300 else None,
                  delta_color="inverse")
        st.metric("Alpha不对称性", f"{alpha_asymmetry:.3f}")

    with col2:
        st.subheader("评分结果")

        # 计算行为-神经不匹配指数
        # 逻辑：主诉严重但ERP正常 → 不匹配度高
        erp_abnormality = 0
        if p300_amplitude < 16:
            erp_abnormality += 30
        if p300_latency > 320:
            erp_abnormality += 30
        if alpha_asymmetry > 0.12:
            erp_abnormality += 20

        # 不匹配指数 = 主诉严重程度 - ERP异常程度（归一化）
        mismatch_score = max(0, (complaint_severity / 100) * 100 - erp_abnormality * 0.6)

        # AI-Fraud Score = 不匹配指数 * 10（0-1000分）
        fraud_score = min(1000, mismatch_score * 10 + np.random.normal(0, 20))
        fraud_score = max(0, min(1000, fraud_score))

        # 显示评分
        st.metric("AI-Fraud Score", f"{fraud_score:.0f} / 1000")

        # 决策建议
        if fraud_score > 850:
            st.error("**自动拒赔** — 移交法务反欺诈部门")
            st.progress(1.0)
        elif fraud_score > 600:
            st.warning("**分期给付** — 首期赔付 + 3个月随访EEG")
            st.progress(0.75)
        else:
            st.success("**极速闪赔** — 建立品牌口碑")
            st.progress(0.3)

        # 显示不匹配指数
        st.markdown("---")
        st.caption(f"行为-神经不匹配指数：{mismatch_score:.0f}/100")
        if mismatch_score > 60:
            st.caption("🔴 主诉与客观指标严重不匹配，建议深度调查")
        elif mismatch_score > 30:
            st.caption("🟡 主诉与客观指标存在差异，建议人工复核")
        else:
            st.caption("🟢 主诉与客观指标基本一致")

    # 显示完整评分卡
    st.markdown("---")
    st.subheader("完整评分卡")

    score_data = {
        "指标": ["P300振幅", "P300潜伏期", "Alpha不对称性", "行为-神经不匹配指数"],
        "检测值": [f"{p300_amplitude:.1f} μV", f"{p300_latency:.0f} ms", f"{alpha_asymmetry:.3f}",
                   f"{mismatch_score:.0f}/100"],
        "正常参考范围": ["18-22 μV", "280-320 ms", "< 0.10", "< 30/100"],
        "状态": [
            "✅ 正常" if p300_amplitude >= 16 else "⚠️ 异常",
            "✅ 正常" if p300_latency <= 320 else "⚠️ 异常",
            "✅ 正常" if alpha_asymmetry <= 0.12 else "⚠️ 异常",
            "✅ 匹配" if mismatch_score <= 30 else "⚠️ 不匹配"
        ]
    }
    st.table(pd.DataFrame(score_data))

# ========== 页面4：文献支撑 ==========
else:
    st.title("文献支撑")

    st.markdown("""
    | 证据层级 | 核心发现 | 来源 |
    |----------|----------|------|
    | 流行病学 | 3次以上脑震荡史→后续风险**RR=3.0** | Guskiewicz等，2003，*JAMA* |
    | 流行病学 | 3次以上史→严重标志出现概率**9.3倍** | Collins等，2002，*Neurosurgery* |
    | 电生理 | 多次脑震荡者P300振幅**长期降低** | De Beaumont等，2007 |
    | 电生理 | P300异常在**常规认知测试正常时仍存在** | Broglio等，2009 |
    | 电生理 | 3次以上脑震荡者SPCN振幅降低，**行为表现正常** | Thériault等，2011 |
    | 装病检测 | 装病者**无法产生**真正的TBI患者P3a反应 | Hoover等，2014 |
    | 装病检测 | ERP+行为反应时组合分类准确率**82%** | Tardif等，2002 |
    | 深度学习 | 静息态EEG脑震荡分类**AUC=0.904** | McLeod等，2025 |
    | 系统综述 | P300是**最有前景**的EEG生物标志物 | Corbin-Berrigan等，2023 |
    """)

    st.markdown("---")
    st.markdown("""
    ### 关键证据解读

    **Hoover等（2014）** ：装病者无法产生真正的TBI患者才有的P3a反应模式。P3a是相对自动化的、不受主观意图显著影响的神经反应。

    **Guskiewicz等（2003）** ：3次以上既往脑震荡史者，后续脑震荡风险为无既往史者的**3倍**（RR=3.0, 95% CI 1.6-5.6）。

    **McLeod等（2025）** ：使用深度学习从5分钟静息态EEG中分类脑震荡的**AUC达到0.904**，证明EEG-based的客观脑功能评估技术已成熟到可商业化应用。

    ### 权威指南

    - **ACOEM 2017**：推荐ERP用于TBI诊断，已被**加州法规正式采纳**
    - **ACRM 2023**：明确定义mTBI的可观察临床体征（意识丧失、顺行性遗忘等）
    - **Tenney 2021（ACNS）** ：qEEG目前定位为"研究性工具"
    """)

    st.info(
        "💡 **项目定位**：本项目并非声称'ERP能诊断脑震荡'，而是定位为'内部风控工具'——提供客观神经功能指标，与主诉交叉验证，触发人工复核。这一定位**证据充分、逻辑自洽、有现实对标**。")


