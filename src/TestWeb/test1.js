$(document).ready(() => {
    setInterval(() => {
        writeDict = {slider: parseInt($("#rangeSlider").val())} 
    }, 20)
})

updateCallback = () => {
    $("#dataSpan").html("Value: "+readDict["time"])
}
