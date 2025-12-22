from __future__ import annotations

from autotestgen.models import TestPoint


def autosar_nm_test_points() -> list[TestPoint]:
    """
    最小知识库：AUTOSAR Network Management（NM）常见测试点模板。
    说明：不区分 Classic/Adaptive，不区分 NM 变体（CanNm/FrNm/EthNm），统一抽象到“NM 支持”层面。
    """
    return [
        TestPoint(
            id="NM-FUNC-001",
            category="功能",
            title="支持 NM 报文发送/接收",
            description="ECU 能正确发送 NM 报文，且能解析并响应来自网络的 NM 报文。",
            tags=["AUTOSAR", "NM"],
        ),
        TestPoint(
            id="NM-STATE-001",
            category="状态机",
            title="NM 状态机基本转换（Normal/ReadySleep/BusSleep 等）",
            description="满足触发条件时进入对应状态，且转换顺序与时序符合配置/规范。",
            tags=["AUTOSAR", "NM", "StateMachine"],
        ),
        TestPoint(
            id="NM-TIM-001",
            category="时序",
            title="NM 周期、超时与抖动容忍",
            description="周期性发送、超时检测、丢包/抖动场景下行为符合预期。",
            tags=["AUTOSAR", "NM", "Timing"],
        ),
        TestPoint(
            id="NM-WKP-001",
            category="唤醒/睡眠",
            title="本地/远程唤醒触发与处理",
            description="本地请求网络、本地唤醒源、远程 NM 唤醒均能正确唤醒并进入工作状态。",
            tags=["AUTOSAR", "NM", "Wakeup"],
        ),
        TestPoint(
            id="NM-SLP-001",
            category="唤醒/睡眠",
            title="网络释放与总线休眠进入",
            description="释放网络后进入准备睡眠/总线睡眠，且不会误唤醒/反复切换。",
            tags=["AUTOSAR", "NM", "Sleep"],
        ),
        TestPoint(
            id="NM-ERR-001",
            category="异常处理",
            title="总线异常（Bus-Off/链路中断）下的 NM 行为",
            description="总线故障时 NM 进入降级/恢复流程，故障恢复后能重新加入网络管理。",
            tags=["AUTOSAR", "NM", "Robustness"],
        ),
        TestPoint(
            id="NM-CFG-001",
            category="配置/兼容性",
            title="与配置项一致（NM PDU ID、Node ID、周期等）",
            description="NM 相关配置生效且与网络其余节点兼容，版本/布局一致。",
            tags=["AUTOSAR", "NM", "Config"],
        ),
        TestPoint(
            id="NM-DIAG-001",
            category="诊断/可观测性",
            title="NM 关键事件可观测（日志/诊断码/测量点）",
            description="状态切换、超时、异常可通过诊断或日志进行定位。",
            tags=["AUTOSAR", "NM", "Diagnostics"],
        ),
    ]


def generic_support_test_points() -> list[TestPoint]:
    """通用“支持某能力”的最小测试点集合。"""
    return [
        TestPoint(
            id="GEN-FUNC-001",
            category="功能",
            title="能力可启用并按预期工作（正向）",
            description="能力开关/配置正确时，主流程功能可用。",
            tags=["Generic"],
        ),
        TestPoint(
            id="GEN-NEG-001",
            category="异常处理",
            title="异常输入/异常环境下的鲁棒性",
            description="参数非法、资源不足、依赖缺失时的错误处理与回退。",
            tags=["Generic", "Robustness"],
        ),
        TestPoint(
            id="GEN-COMP-001",
            category="兼容性",
            title="与外部依赖/接口兼容",
            description="对外接口版本、对端实现差异下仍能互通或给出明确错误。",
            tags=["Generic", "Compatibility"],
        ),
        TestPoint(
            id="GEN-PERF-001",
            category="性能",
            title="性能与资源占用满足基本预期",
            description="CPU/内存/带宽占用与响应时间在可接受范围。",
            tags=["Generic", "Performance"],
        ),
    ]


def choose_test_points(requirement_text: str) -> tuple[str, list[str], list[TestPoint]]:
    """
    返回 (domain, assumptions, test_points)。
    最小实现：关键词路由到 AUTOSAR NM，否则回退通用模板。
    """
    text_upper = requirement_text.upper()
    assumptions: list[str] = []

    is_autosar = "AUTOSAR" in text_upper
    is_nm = ("网络管理" in requirement_text) or ("NETWORK MANAGEMENT" in text_upper) or (" NM" in text_upper) or text_upper.endswith("NM")

    if is_autosar and is_nm:
        assumptions.extend(
            [
                "未明确总线类型，默认覆盖 CAN/Ethernet 等常见 NM 场景的抽象测试点。",
                "未明确 Classic/Adaptive，默认按 AUTOSAR NM 通用规范进行测试设计。",
                "未提供网络/节点配置，测试用例以“可配置/可观测”为前置。",
            ]
        )
        return "autosar_nm", assumptions, autosar_nm_test_points()

    assumptions.append("需求较短且缺少上下文，已按通用“支持能力”模板生成测试点。")
    return "generic", assumptions, generic_support_test_points()
