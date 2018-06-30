$(document).ready(() => {
        var stage = new createjs.Stage("canvas")

        var robot = new createjs.Shape()
        robot.graphics.beginFill("lightblue").drawRect(0, 0, 100, 100)
        robot.x = 200
        robot.y = 200
        stage.addChild(robot)

        var left = new createjs.Shape()
        stage.addChild(left)

        var right = new createjs.Shape()
        stage.addChild(right)

        var floor1 = new createjs.Shape()
        stage.addChild(floor1)

        var floor2 = new createjs.Shape()
        stage.addChild(floor2)

        stage.update()

    updateCallback = () => {
        var leftDist = (100 - parseInt(readDict["leftProx"]))
        var rightDist = (100 - parseInt(readDict["rightProx"]))
        var leftFloor = Math.min(100, parseInt(readDict["leftFloor"])) * 255.0 / 100.0
        var rightFloor = Math.min(100, parseInt(readDict["rightFloor"])) * 255.0 / 100.0

        left.graphics.clear().beginFill("green").drawRect(210, 200 - leftDist, 5, leftDist)
        right.graphics.clear().beginFill("green").drawRect(285, 200 - rightDist, 5, rightDist)
        floor1.graphics.clear().beginFill(`rgba(${leftFloor}, ${leftFloor}, ${leftFloor}, 1.0)`).drawRect(215, 210, 15, 10)
        floor2.graphics.clear().beginFill(`rgba(${rightFloor}, ${rightFloor}, ${rightFloor}, 1.0)`).drawRect(270, 210, 15, 10)

        stage.update()
    }
})
