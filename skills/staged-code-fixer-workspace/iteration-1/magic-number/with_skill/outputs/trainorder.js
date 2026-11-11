// 订单已取消状态
var ORDER_STATUS_CANCELED = 8;

/**
 * 加载火车订单详情，处理订单超时关闭等状态
 *
 * @author Claude Code (kimi-3)
 */
function loadTrainDetail() {
    var $orderBrief = $data.listBasic;

    if ($orderBrief.status == ORDER_STATUS_CANCELED) {
        showTimeoutClosed();
    }
}
