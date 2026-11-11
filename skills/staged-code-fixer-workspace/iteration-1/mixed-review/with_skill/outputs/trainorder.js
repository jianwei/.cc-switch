// @author Claude Code (kimi-3)

// 订单已取消状态
var ORDER_STATUS_CANCELED = 8;

/**
 * 加载列车订单详情
 *
 * @author Claude Code (kimi-3)
 */
function loadTrainDetail() {
    // 统一从根级数据获取订单状态，保持状态判断数据来源一致
    var $orderBrief = $data.listBasic;
    var orderStatus = $data.listBasic.orderStatus || $orderBrief.status;

    if (orderStatus == ORDER_STATUS_CANCELED && $data.alipayEnterprisePayTimeoutClosedFlag) {
        showTimeoutClosed();
    }
}
