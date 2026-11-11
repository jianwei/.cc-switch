function loadTrainDetail() {
    var $orderBrief = $data.listBasic;
    // 统一从根级数据获取订单状态，保持状态判断数据来源一致
    var orderStatus = $data.listBasic.orderStatus || $orderBrief.status;

    if (orderStatus == 8 && $data.alipayEnterprisePayTimeoutClosedFlag) {
        showTimeoutClosed();
    }
}
