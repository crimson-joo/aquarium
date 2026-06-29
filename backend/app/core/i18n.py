from app.domain.contracts import Locale

MESSAGES = {
    Locale.KO: {
        "research_heading": "# 조사 보고서",
        "simulation_heading": "# 시뮬레이션 보고서",
        "caveat": "이 결과는 실제 예측 확률이 아니라 입력 문서와 가정에 기반한 시뮬레이션 관찰입니다.",
        "chat_prefix": "시뮬레이션 기준으로 보면",
        "ensemble_heading": "## 앙상블 빈도",
        "ensemble_note": "- 기준/낙관/제약 분기를 실제 확률이 아닌 앙상블 빈도로 비교합니다.",
        "single_heading": "## 단일 해류",
        "single_note": "- 이 단일 run은 예측이 아니라 기준 시뮬레이션 경로입니다.",
    },
    Locale.ZH: {
        "research_heading": "# 研究报告",
        "simulation_heading": "# 模拟报告",
        "caveat": "该结果不是实际预测概率，而是基于输入文档和假设的模拟观察。",
        "chat_prefix": "从模拟结果来看",
        "ensemble_heading": "## 集成频率",
        "ensemble_note": "- 基准、乐观、约束分支以集成频率比较，而不是实际概率。",
        "single_heading": "## 单一水流",
        "single_note": "- 该单次运行不是预测，而是基准模拟轨迹。",
    },
    Locale.EN: {
        "research_heading": "# Research Report",
        "simulation_heading": "# Simulation Report",
        "caveat": "This result is not a prediction probability; it is a simulation observation based on the input document and assumptions.",
        "chat_prefix": "From the simulation results",
        "ensemble_heading": "## Ensemble Frequency",
        "ensemble_note": "- baseline/optimistic/constraint branches are compared as ensemble frequency, not probability.",
        "single_heading": "## Single Current",
        "single_note": "- This single run is not a prediction; it is a baseline simulation trace.",
    },
}


def msg(locale: Locale, key: str) -> str:
    return MESSAGES[locale][key]
