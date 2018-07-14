var readDict = {}
var writeDict = {}

var updateCallback = () => {}

function event(eventType) {
    $.get("/event?eventType="+eventType, () => {})
}

$(document).ready(() => {
    setInterval(() => {
        $.get("/update?data="+JSON.stringify(writeDict), (output) => {
            readDict = JSON.parse(output)
            updateCallback()
        })
    }, 30);

    $("[data-event]").each(function() {
        $(this).click(function() {
            event($(this).data("event"))
        })
    });
})

