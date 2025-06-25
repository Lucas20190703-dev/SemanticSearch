import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: window
    width: 800
    height: 600
    visible: true
    flags: Qt.FramelessWindowHint | Qt.Window
    color: "#1e1e1e"

    property int border: 8
    property point dragStartPos: Qt.point(0, 0)

    // Content area (replace with your UI)
    Rectangle {
        anchors.fill: parent
        color: "#252526"
    }

    // --- Resize Edges and Corners ---

    // Top
    MouseArea {
        anchors.left: parent.left
        anchors.right: parent.right
        height: border
        cursorShape: Qt.SizeVerCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dy = mouseY - dragStartPos.y
            if (window.height - dy > 200) {
                window.y += dy
                window.height -= dy
            }
        }
    }

    // Bottom
    MouseArea {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: border
        cursorShape: Qt.SizeVerCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dy = mouseY - dragStartPos.y
            if (window.height + dy > 200) {
                window.height += dy
                dragStartPos.y = mouseY
            }
        }
    }

    // Left
    MouseArea {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: border
        cursorShape: Qt.SizeHorCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            if (window.width - dx > 300) {
                window.x += dx
                window.width -= dx
            }
        }
    }

    // Right
    MouseArea {
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: border
        cursorShape: Qt.SizeHorCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            if (window.width + dx > 300) {
                window.width += dx
                dragStartPos.x = mouseX
            }
        }
    }

    // Corners
    // Top-Left
    MouseArea {
        anchors.left: parent.left
        anchors.top: parent.top
        width: border
        height: border
        cursorShape: Qt.SizeFDiagCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            let dy = mouseY - dragStartPos.y
            if (window.width - dx > 300) {
                window.x += dx
                window.width -= dx
            }
            if (window.height - dy > 200) {
                window.y += dy
                window.height -= dy
            }
        }
    }

    // Top-Right
    MouseArea {
        anchors.right: parent.right
        anchors.top: parent.top
        width: border
        height: border
        cursorShape: Qt.SizeBDiagCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            let dy = mouseY - dragStartPos.y
            if (window.width + dx > 300) {
                window.width += dx
                dragStartPos.x = mouseX
            }
            if (window.height - dy > 200) {
                window.y += dy
                window.height -= dy
            }
        }
    }

    // Bottom-Left
    MouseArea {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        width: border
        height: border
        cursorShape: Qt.SizeBDiagCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            let dy = mouseY - dragStartPos.y
            if (window.width - dx > 300) {
                window.x += dx
                window.width -= dx
            }
            if (window.height + dy > 200) {
                window.height += dy
                dragStartPos.y = mouseY
            }
        }
    }

    // Bottom-Right
    MouseArea {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        width: border
        height: border
        cursorShape: Qt.SizeFDiagCursor
        onPressed: dragStart()
        onPositionChanged: {
            let dx = mouseX - dragStartPos.x
            let dy = mouseY - dragStartPos.y
            if (window.width + dx > 300) {
                window.width += dx
                dragStartPos.x = mouseX
            }
            if (window.height + dy > 200) {
                window.height += dy
                dragStartPos.y = mouseY
            }
        }
    }

    function dragStart() {
        dragStartPos = Qt.point(mouseX, mouseY)
    }
}
