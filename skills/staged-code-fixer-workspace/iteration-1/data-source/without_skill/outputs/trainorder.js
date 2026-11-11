function loadTrainDetail() {
    var $orderBrief = $data.listBasic;
    var orderStatus = $data.listBasic.orderStatus || $orderBrief.status;

    if (orderStatus == 8 && $data.alipayEnterprisePayTimeoutClosedFlag) {
        showTimeoutClosed();
    }
}
