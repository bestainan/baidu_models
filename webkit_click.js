function dispatch(c, b) {
    try {
        var a = document.createEvent("Event");
        a.initEvent(b, true, true);
        c.dispatchEvent(a)
    } catch (d) {
        alert(d)
    }
};
