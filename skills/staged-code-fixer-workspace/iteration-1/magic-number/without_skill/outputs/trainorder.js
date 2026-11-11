// 订单已取消状态码，用于替代魔法数字 8
var ORDER_STATUS_CANCELED = 8;

function loadTrainDetail() {
    var $orderBrief = $data.listBasic;

    if ($orderBrief.status === ORDER_STATUS_CANCELED) {
        showTimeoutClosed();
    }
}
