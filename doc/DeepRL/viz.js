var gridCell = 30 // 10 px = 1 cm

function coordToPx(coord) {
    return [parseInt(Math.round(coord[0] * gridCell + $("#canvas").width() / 2.0)), parseInt(Math.round(coord[1] * gridCell + $("#canvas").height() / 2.0))]
}

function lenToPx(len){
    return gridCell * len
}

function toDegrees(angle){
  return angle * (180.0 / Math.PI);
}

var stage, robot, width, height, obstacles, sensorLines

function setup(){
    stage = new createjs.Stage("canvas")
    width = $("#canvas").width()
    height = $("#canvas").height()

    var gridLines = new createjs.Shape();
    gridLines.graphics.setStrokeStyle(1);
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

    gridLines.graphics.setStrokeStyle(3);
    gridLines.graphics.beginStroke("black");
    gridLines.graphics.moveTo(0, height / 2.0);
    gridLines.graphics.lineTo(width, height / 2.0);
    gridLines.graphics.endStroke();

    gridLines.graphics.beginStroke("black");
    gridLines.graphics.moveTo(width / 2.0, 0);
    gridLines.graphics.lineTo(width / 2.0, height);
    gridLines.graphics.endStroke();

    stage.addChild(gridLines)
    stage.update()

    robot = new createjs.Shape()
    var widthPx = lenToPx(parseFloat(readDict["robotWidth"]))
    var heightPx = lenToPx(parseFloat(readDict["robotHeight"]))

    robot.graphics.beginFill("lightblue").drawRect(-0.5 * widthPx, -0.5 * heightPx, widthPx, heightPx)
    robot.graphics.beginFill("black").drawRect(-5, -0.5 * heightPx, 10, 10)
    robot.graphics.beginFill("black").drawRect(-0.5 * widthPx + 3, -0.15 * heightPx, 5, 0.4 * heightPx)
    robot.graphics.beginFill("black").drawRect(0.5 * widthPx - 8, -0.15 * heightPx, 5, 0.4 * heightPx)
    [robot.x, robot.y] = coordToPx([0, 0])
    stage.addChild(robot)

    obstacles = new createjs.Shape()
    sensorLines = new createjs.Shape()
    stage.addChild(sensorLines)
    stage.addChild(obstacles)

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

        var obsArr = readDict["obstacles"]
        obstacles.graphics.clear()
        for(var i = 0; i < obsArr.length; i++) {
            var o = obsArr[i]
            var [x, y] = coordToPx([o["x"], o["y"]])
            var w = lenToPx(o["w"])
            var h = lenToPx(o["h"])
            obstacles.graphics.beginFill("lightgrey").drawRect(x - w / 2.0, y - h / 2.0, w, h)
        }

        sensorLines.graphics.clear()

        leftSensorPos = readDict["robotLeftSensorPos"]        
        leftSensorPoint = readDict["pointL"]

        if(leftSensorPos && leftSensorPoint) {
            leftSensorPos = coordToPx([leftSensorPos["x"], leftSensorPos["y"]])
            leftSensorPoint = coordToPx([leftSensorPoint["x"], leftSensorPoint["y"]])

            sensorLines.graphics.setStrokeStyle(2);
            sensorLines.graphics.beginStroke("red");
            sensorLines.graphics.moveTo(leftSensorPos[0], leftSensorPos[1]);
            sensorLines.graphics.lineTo(leftSensorPoint[0], leftSensorPoint[1]);
            sensorLines.graphics.endStroke();
        }

        rightSensorPos = readDict["robotRightSensorPos"]        
        rightSensorPoint = readDict["pointR"]

        if(rightSensorPos && rightSensorPoint) {
            rightSensorPos = coordToPx([rightSensorPos["x"], rightSensorPos["y"]])
            rightSensorPoint = coordToPx([rightSensorPoint["x"], rightSensorPoint["y"]])

            sensorLines.graphics.setStrokeStyle(2);
            sensorLines.graphics.beginStroke("red");
            sensorLines.graphics.moveTo(rightSensorPos[0], rightSensorPos[1]);
            sensorLines.graphics.lineTo(rightSensorPoint[0], rightSensorPoint[1]);
            sensorLines.graphics.endStroke();
        }

        stage.update()

        $("#leftDist").html(parseFloat(readDict["proxL"]).toFixed(2))
        $("#rightDist").html(parseFloat(readDict["proxR"]).toFixed(2))

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

var cmdLeft, cmdRight;

$(document).keypress(function(event){
    var key = String.fromCharCode(event.which).toLowerCase()
    if(key == "w") {
        var x = 0
        var y = 1
    }

    else if(key == "s") {
        var x = 0
        var y = -1
    }

    else if(key == "a") {
        var x = -1 
        var y = 0 
    }

    else if(key == "d") {
        var x = 1
        var y = 0
    }

    else {
        var x = 0
        var y = 0
    }

    cmdLeft = parseInt(4.0 * (y + x))
    cmdRight = parseInt(4.0 * (y - x))

    writeDict = {l: cmdLeft, r: cmdRight}
});
