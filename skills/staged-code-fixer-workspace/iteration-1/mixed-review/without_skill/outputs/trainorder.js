// @author Claude Code (kimi-3)

// 订单已取消状态
var ORDER_STATUS_CANCELED = 8;

/**
 * 加载火车订单详情，处理超时关闭等状态展示
 *
 * @author Claude Code (kimi-3)
 */
function loadTrainDetail() {
    var $orderBrief = $data.listBasic;
    // 统一从 $data 中提取订单状态，保持状态判断的数据来源一致
    var orderStatus = $data.listBasic.orderStatus || $orderBrief.status;

    if (orderStatus === ORDER_STATUS_CANCELED && $data.alipayEnterprisePayTimeoutClosedFlag) {
        showTimeoutClosed();
    }
}
