var gridCell = 50 // 10 px = 1 cm

function coordToPx(coord) {
    return [parseInt(coord[0] * gridCell + $("#canvas").width() / 2.0), parseInt(coord[1] * gridCell + $("#canvas").height() / 2.0)]
}

function lenToPx(len){
    return gridCell * len
}

function toDegrees(angle){
  return angle * (180.0 / Math.PI);
}

var stage, robot, width, height

function setup(){
    stage = new createjs.Stage("canvas")
    width = $("#canvas").width()
    height = $("#canvas").height()

    var gridLines = new createjs.Shape();
    gridLines.graphics.setStrokeStyle(3);
    for(var x = gridCell; x < width; x += gridCell) {
        gridLines.graphics.beginStroke("black");
        gridLines.graphics.moveTo(x, 0);
        gridLines.graphics.lineTo(x, height);
        gridLines.graphics.endStroke();
    }

    for(var y = gridCell; y < height; y += gridCell) {
        gridLines.graphics.beginStroke("black");
        gridLines.graphics.moveTo(0, y);
        gridLines.graphics.lineTo(width, y);
        gridLines.graphics.endStroke();
    }

    stage.addChild(gridLines)
    stage.update()

    robot = new createjs.Shape()
    var widthPx = lenToPx(parseFloat(readDict["robotWidth"]))
    var heightPx = lenToPx(parseFloat(readDict["robotHeight"]))

    robot.graphics.beginFill("lightblue").drawRect(-0.5 * widthPx, -0.5 * heightPx, widthPx, heightPx)
    robot.graphics.beginFill("black").drawRect(-5, -0.5 * heightPx, 10, 10)
    [robot.x, robot.y] = coordToPx([0, 0])
    stage.addChild(robot)

    stage.update()
}

var ready = false

$(document).ready(() => {
    updateCallback = () => {
        if(!ready) {
            ready = true
            setup()
        }

        var robotPos = [parseFloat(readDict["robotX"]), parseFloat(readDict["robotY"])]
        var robotAngle = toDegrees(parseFloat(readDict["robotTheta"])) + 90
        var coords = coordToPx(robotPos)
        robot.x = coords[0]
        robot.y = coords[1]
        robot.rotation = robotAngle

        stage.update()

       /*var leftDist = (100 - parseInt(readDict["leftProx"]))
        var rightDist = (100 - parseInt(readDict["rightProx"]))
        var leftFloor = Math.min(100, parseInt(readDict["leftFloor"])) * 255.0 / 100.0
        var rightFloor = Math.min(100, parseInt(readDict["rightFloor"])) * 255.0 / 100.0

        left.graphics.clear().beginFill("green").drawRect(210, 200 - leftDist, 5, leftDist)
        right.graphics.clear().beginFill("green").drawRect(285, 200 - rightDist, 5, rightDist)
        floor1.graphics.clear().beginFill(`rgba(${leftFloor}, ${leftFloor}, ${leftFloor}, 1.0)`).drawRect(215, 210, 15, 10)
        floor2.graphics.clear().beginFill(`rgba(${rightFloor}, ${rightFloor}, ${rightFloor}, 1.0)`).drawRect(270, 210, 15, 10)

        stage.update()*/
    }
})
